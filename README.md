# Huawei P30 lite vendor files

Vendor and ODM configuration and Linux 6.12 overlays for LineageOS 24.0 (Android 17).

Source firmware: **MAR-LGRP2-OVS 9.1.0.399**, C431 (VNDK 28 hardware base).

Run `device/huawei/marie/extract-files.py` from a LineageOS checkout with a
folder containing the stock `vendor.img` and `odm.img`. `firmware.json` records
their sizes and SHA-256 checksums.

## Linux 6.12 + Mali-G51 Panfrost + SELinux Enforcing Overlays

The `overlay/` directory contains the open-source vendor overlays required on
top of the stock EMUI 9 vendor base for full SELinux Enforcing Android 17 boot
on Linux 6.12:

- **`overlay/etc/selinux/vendor_sepolicy_marie612.cil`**: `secilc`-verified
  SELinux Enforcing rules for Mali-G51 Panfrost (`/dev/dri/*`), HWC3/minigbm
  (`hal_graphics_allocator_client`), `/dev/ashmem` (`ashmem_libcutils_device`),
  backlight `sysfs_leds` (`genfscon sysfs /devices/virtual/leds/lcd_backlight0`),
  and EMUI 9 vendor HAL compatibility.
- **`overlay/etc/selinux/vendor_service_contexts`** &
  **`overlay/etc/selinux/vendor_file_contexts.extra`**: Registers
  `mapper/minigbm` (`hal_graphics_mapper_service`) and labels Mesa Panfrost,
  minigbm, and `vendor_service_contexts` (`vendor_service_contexts_file`).
- **`overlay/etc/seccomp_policy/configstore@1.1.policy`**: Adds Android 17
  Bionic syscalls (`gettid`, `getpid`, `tgkill`, `fcntl`, `sendto`) for
  `vendor.configstore-hal`.
- **`overlay/etc/init/marie-panfrost.rc`**: Sets `persist.graphics.egl=mesa`
  and `drm.gpu.vendor_name=panfrost` at `early-init`.

Additional required binary updates when repacking `/vendor` for Android 17:
1. Replace stock EMUI 9 `/vendor/lib{,64}/libminijail.so` with LineageOS 24's
   built vendor `libminijail.so` (fixes `@include` nesting abort in
   `vendor.media.omx`, which otherwise deadlocks `StorageManagerService`).
2. Run `patchelf --add-needed libwifi_fdsan_compat.so` on
   `/vendor/bin/hw/vendor.huawei.hardware.wifi@1.1-service` so the `fdsan` shim
   loads under SELinux Enforcing (`AT_SECURE=1` strips `LD_PRELOAD`).
3. Include Mesa 24.3.4 Gallium Panfrost (`libgallium_dri.so`, `libglapi.so`,
   `egl/libEGL_mesa.so`, `egl/libGLESv1_CM_mesa.so`, `egl/libGLESv2_mesa.so`),
   `hwc3-service.drm`, and `minigbm` allocator/mapper HALs.
