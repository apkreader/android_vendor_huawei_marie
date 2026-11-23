# Copyright (C) 2026 apkreader
# SPDX-License-Identifier: MIT

# Mesa 24.3.4 Gallium Panfrost (Mali-G51, arm64 + arm32)
# Rebuilt reproducibly via device/huawei/marie/graphics/build-mesa-panfrost.sh
PRODUCT_COPY_FILES += \
    vendor/huawei/marie/mesa/lib64/libgallium_dri.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libgallium_dri.so \
    vendor/huawei/marie/mesa/lib64/libglapi.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libglapi.so \
    vendor/huawei/marie/mesa/lib64/egl/libEGL_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib64/egl/libEGL_mesa.so \
    vendor/huawei/marie/mesa/lib64/egl/libGLESv1_CM_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib64/egl/libGLESv1_CM_mesa.so \
    vendor/huawei/marie/mesa/lib64/egl/libGLESv2_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib64/egl/libGLESv2_mesa.so \
    vendor/huawei/marie/mesa/lib/libgallium_dri.so:$(TARGET_COPY_OUT_VENDOR)/lib/libgallium_dri.so \
    vendor/huawei/marie/mesa/lib/libglapi.so:$(TARGET_COPY_OUT_VENDOR)/lib/libglapi.so \
    vendor/huawei/marie/mesa/lib/egl/libEGL_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib/egl/libEGL_mesa.so \
    vendor/huawei/marie/mesa/lib/egl/libGLESv1_CM_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib/egl/libGLESv1_CM_mesa.so \
    vendor/huawei/marie/mesa/lib/egl/libGLESv2_mesa.so:$(TARGET_COPY_OUT_VENDOR)/lib/egl/libGLESv2_mesa.so

PRODUCT_PACKAGES += \
    marie_mesa_libEGL_mali_64 \
    marie_mesa_libGLESv1_CM_mali_64 \
    marie_mesa_libGLESv2_mali_64 \
    marie_mesa_libEGL_mali_32 \
    marie_mesa_libGLESv1_CM_mali_32 \
    marie_mesa_libGLESv2_mali_32
