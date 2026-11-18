# Huawei P30 lite vendor files

Vendor and ODM images for the initial LineageOS 24.0 bring-up.

Source firmware: **MAR-LGRP2-OVS 9.1.0.399**, C431.

Run `device/huawei/marie/extract-files.py` from a LineageOS checkout with a
folder containing the two images. `firmware.json` records their sizes and
SHA-256 checksums. The prepared images are stored locally under `proprietary/`.

Vendor preparation keeps Huawei's EROFS layout and hardware libraries. It
renames the old `perf_event` capability permission to `perfmon` and removes
the duplicate `fuseblk` filesystem label from the vendor policy. The device
tree provides the corresponding Android 9 compatibility mapping.

The two policy files use plain extents; the remaining files and their
permissions, labels and capabilities are preserved. The stock verification
trailer is removed. The LineageOS fstab mounts vendor without AVB.

This is an Android 9 / VNDK 28 hardware base. Full Android 17 bring-up and
hardware testing remain work in progress.
