# Huawei P30 lite vendor files

Stock vendor and ODM images for the initial LineageOS 24.0 bring-up.

Source firmware: **MAR-LGRP2-OVS 9.1.0.399**, C431.

Run `device/huawei/marie/extract-files.py` from a LineageOS checkout with a
folder containing the two images. `firmware.json` records their sizes and
SHA-256 checksums. The images are stored locally under `proprietary/`.

These are Android 9 / VNDK 28 images. Their compatibility with Android 17
has not been established. HAL extraction, compatibility libraries and
source replacements remain work in progress.
