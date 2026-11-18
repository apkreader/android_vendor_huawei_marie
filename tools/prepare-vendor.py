#!/usr/bin/env python3
# Copyright (C) 2026 apkreader
# SPDX-License-Identifier: Apache-2.0

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import tempfile


BLOCK_SIZE = 4096


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expand_sparse(source, target):
    with source.open("rb") as src, target.open("wb") as dst:
        header = src.read(28)
        magic, major, minor, header_size, chunk_header_size, block_size, blocks, chunks, checksum = \
            struct.unpack("<IHHHHIIII", header)
        assert magic == 0xed26ff3a and major == 1 and block_size == BLOCK_SIZE
        assert header_size >= 28 and chunk_header_size >= 12
        src.seek(header_size)
        for _ in range(chunks):
            kind, reserved, count, size = struct.unpack("<HHII", src.read(12))
            src.seek(chunk_header_size - 12, 1)
            length = count * block_size
            if kind == 0xcac1:
                assert size == chunk_header_size + length
                remaining = length
                while remaining:
                    data = src.read(min(remaining, 1024 * 1024))
                    assert data
                    dst.write(data)
                    remaining -= len(data)
            elif kind == 0xcac2:
                assert size == chunk_header_size + 4
                fill = src.read(4) * (block_size // 4)
                for _ in range(count):
                    dst.write(fill)
            elif kind == 0xcac3:
                assert size == chunk_header_size
                dst.seek(length, 1)
            elif kind == 0xcac4:
                assert size == chunk_header_size + 4
                src.read(4)
            else:
                raise ValueError("Unknown sparse chunk: " + hex(kind))
        assert dst.tell() == blocks * block_size
        dst.truncate()
        assert not src.read(1)


def decompress_lz4(data, length):
    output = bytearray()
    position = 0
    while len(output) < length:
        token = data[position]
        position += 1
        literal = token >> 4
        if literal == 15:
            while True:
                value = data[position]
                position += 1
                literal += value
                if value != 255:
                    break
        output.extend(data[position:position + literal])
        position += literal
        if len(output) >= length:
            break
        distance = struct.unpack_from("<H", data, position)[0]
        position += 2
        assert 0 < distance <= len(output)
        match = (token & 15) + 4
        if token & 15 == 15:
            while True:
                value = data[position]
                position += 1
                match += value
                if value != 255:
                    break
        for _ in range(match):
            output.append(output[-distance])
    return bytes(output[:length])


def read_policy(stream, metadata_block, nid):
    location = metadata_block * BLOCK_SIZE + nid * 32
    stream.seek(location)
    inode = bytearray(stream.read(32))
    layout, xattr_count, mode = struct.unpack_from("<HHH", inode)
    assert layout == 2 and mode == 0o100644
    length = struct.unpack_from("<I", inode, 8)[0]
    xattr_size = 12 + (xattr_count - 1) * 4 if xattr_count else 0
    stream.seek((location + 32 + xattr_size + 7) // 8 * 8 + 16)
    extents = {}
    for cluster in range((length + BLOCK_SIZE - 1) // BLOCK_SIZE):
        flags, offset, block = struct.unpack("<HHI", stream.read(8))
        assert flags & 3 == 3
        previous = offset // BLOCK_SIZE | ((flags >> 4 & 15) << 4)
        start = (cluster - previous) * BLOCK_SIZE + (offset & (BLOCK_SIZE - 1))
        assert 0 <= start < length
        assert start not in extents or extents[start] == block
        extents[start] = block
    starts = sorted(extents)
    assert starts[0] == 0
    output = bytearray()
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else length
        stream.seek(extents[start] * BLOCK_SIZE)
        output.extend(decompress_lz4(stream.read(BLOCK_SIZE), end - start))
    return location, inode, bytes(output)


def patch_policy(name, data, expected):
    assert hashlib.sha256(data).hexdigest() == expected["sha256"], name
    text = data.decode("utf-8")
    pattern = r"(\((?:capability2|cap2_userns)\s+\([^)]*)\bperf_event\b"
    text, count = re.subn(pattern, lambda match: match[1] + "perfmon", text)
    assert count == expected["capability_references"], (name, count)
    if name == "vendor_sepolicy.cil":
        # The platform now supplies fuseblk's genfs label. Its legacy vfat
        # permissions are retained by the device's 28.0 compatibility mapping.
        lines = text.splitlines(keepends=True)
        removed = [line for line in lines if line.startswith("(genfscon fuseblk / ")]
        assert len(removed) == 1 and "object_r vfat " in removed[0]
        text = "".join(line for line in lines if line not in removed)
    return text.encode("utf-8")


def prepare(source, destination, firmware):
    expected = next(item for item in firmware["images"] if item["name"] == "vendor.img")
    source_hash = sha256(source)
    if source_hash not in (expected["sha256"], expected["raw_sha256"]):
        raise ValueError("vendor.img does not match " + firmware["firmware"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
        temporary = Path(stream.name)
    try:
        if source_hash == expected["sha256"]:
            expand_sparse(source, temporary)
        else:
            shutil.copyfile(source, temporary)
        assert temporary.stat().st_size == expected["raw_size"]
        assert sha256(temporary) == expected["raw_sha256"]
        with temporary.open("r+b") as stream:
            stream.seek(1024)
            superblock = stream.read(128)
            assert struct.unpack_from("<III", superblock) == (0xe0f5e1e2, 0, 0)
            assert superblock[12] == 12
            blocks, metadata_block = struct.unpack_from("<II", superblock, 36)
            files = []
            for name, policy in firmware["selinux"].items():
                location, inode, data = read_policy(stream, metadata_block, policy["nid"])
                files.append((name, location, inode, patch_policy(name, data, policy)))

            # Keep Huawei's original compressed files and xattrs. The two new
            # policy files use plain extents after the existing filesystem.
            # The stock verification trailer no longer describes this image.
            stream.truncate(blocks * BLOCK_SIZE)
            report = {"source_sha256": source_hash, "stock_blocks": blocks, "policies": []}
            for name, location, inode, data in files:
                first_block = blocks
                padded = data + b"\0" * (-len(data) % BLOCK_SIZE)
                stream.seek(first_block * BLOCK_SIZE)
                stream.write(padded)
                struct.pack_into("<H", inode, 0, 0)
                struct.pack_into("<I", inode, 8, len(data))
                struct.pack_into("<I", inode, 16, first_block)
                stream.seek(location)
                stream.write(inode)
                blocks += len(padded) // BLOCK_SIZE
                report["policies"].append({"name": name, "bytes": len(data),
                                           "sha256": hashlib.sha256(data).hexdigest()})
            assert blocks * BLOCK_SIZE < expected["raw_size"]
            stream.seek(1024 + 36)
            stream.write(struct.pack("<I", blocks))
            stream.truncate(expected["raw_size"])
        report.update({"blocks": blocks, "bytes": temporary.stat().st_size,
                       "sha256": sha256(temporary)})
        assert report["sha256"] == expected["prepared_sha256"]
        temporary.replace(destination)
        destination.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
        return report
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Prepare the EMUI vendor image for LineageOS.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.source.resolve() == args.destination.resolve():
        parser.error("Source and destination must be different files")
    firmware = json.loads((Path(__file__).resolve().parents[1] / "firmware.json").read_text())
    print(json.dumps(prepare(args.source, args.destination, firmware), indent=2))


if __name__ == "__main__":
    main()
