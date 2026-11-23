# Huawei P30 lite (marie) vendor tree

Vendor build definitions and Mesa 24.3.4 Gallium Panfrost libraries for
LineageOS 24.0 (Android 17) on Linux 6.12.

Source firmware: **MAR-LGRP2-OVS 9.1.0.399** (C431).

## Setup

Proprietary Huawei blobs are not stored in this repository (`proprietary/` is
gitignored). Populate them from an extracted EMUI 9.1.0.399 vendor dump with:

```sh
cd device/huawei/marie
./extract-files.py /path/to/vendor_dump
```

`extract-files.py` extracts the EMUI 9 vendor binaries, patches
`vendor.huawei.hardware.wifi@1.1-service` (`DT_NEEDED` for
`libwifi_fdsan_compat.so`), strips the legacy HIDL graphics entries from
`vintf/manifest.xml`, appends the Linux 6.12 / Panfrost / SELinux Enforcing
rules to `vendor_sepolicy.cil`, and generates `Android.bp`, `Android.mk`, and
`marie-vendor.mk`.

During `mka vendorimage`, LineageOS compiles HWC3 (`drm_hwcomposer`), `minigbm`
allocator/mapper, `libminijail`, and the AIDL Power HAL from source and isolates
their Android 17 library dependencies from Huawei's VNDK 28 HALs automatically
via `device/huawei/marie/graphics/isolate-vndk28.py`.

## Mesa Panfrost

`mesa/` contains stripped arm64 and arm32 builds of open-source MIT-licensed
Mesa 24.3.4 Gallium Panfrost (`libgallium_dri.so`, `libglapi.so`,
`egl/lib{EGL,GLESv1_CM,GLESv2}_mesa.so`). They can be rebuilt reproducibly from
upstream Mesa source using `device/huawei/marie/graphics/build-mesa-panfrost.sh`.
