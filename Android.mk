#
# Automatically generated file. DO NOT MODIFY
#

LOCAL_PATH := $(call my-dir)

# The OEM modules are installed below or by marie-vendor.mk.
ETC.marie-vendor-manifest.OVERRIDES += \
    android.hardware.audio.effect@4.0-impl \
    android.hardware.audio@4.0-impl \
    android.hardware.bluetooth@1.0-impl \
    android.hardware.bluetooth@1.0-service \
    android.hardware.camera.provider@2.4-impl \
    android.hardware.cas@1.0-service \
    android.hardware.cas@1.2-service \
    android.hardware.drm@1.0-impl \
    android.hardware.drm@1.0-service \
    android.hardware.gatekeeper@1.0-impl \
    android.hardware.gatekeeper@1.0-service \
    android.hardware.keymaster@3.0-impl \
    android.hardware.keymaster@3.0-service \
    android.hardware.media.omx@1.0-service \
    android.hardware.renderscript@1.0-impl \
    android.hardware.secure_element@1.0-service \
    android.hardware.thermal@1.0-impl \
    android.hardware.thermal@1.0-service \
    android.hardware.usb@1.0-service \
    audio.r_submix.default \
    audio.usb.default \
    boringssl_self_test_vendor \
    camera.device@1.0-impl \
    camera.device@3.2-impl \
    camera.device@3.3-impl \
    camera.device@3.4-external-impl \
    camera.device@3.4-impl \
    cplay \
    gralloc.default \
    libLLVM_android.vendor \
    libalsautils.vendor \
    libavservices_minijail_vendor \
    libbcc.vendor \
    libclearkeycasplugin \
    libdrmclearkeyplugin \
    libdynproc \
    libeffectproxy \
    libeffects \
    libeffectsconfig.vendor \
    libhwc2on1adapter \
    libhwc2onfbadapter \
    libhwminijail \
    libkeymaster3device.vendor \
    libldnhncr \
    libmockcasplugin \
    libnbaio_mono \
    libreference-ril \
    libril \
    librilutils \
    libtinycompress \
    libvisualizer \
    libwpa_client \
    local_time.default \
    power.default \
    rild \
    vibrator.default \
    wpa_cli

marie_legacy_vendor_files := \
    etc/init/android.hardware.drm@1.1-service.clearkey.rc \
    etc/init/android.hardware.drm@1.1-service.widevine.rc \
    etc/init/aptouch_daemon.rc \
    etc/init/charger/init.charger.rc \
    etc/init/connectivity/init.connectivity.gps.rc \
    etc/init/connectivity/init.connectivity.hi1102.rc \
    etc/init/hinetmanager.rc \
    etc/init/hw/init.kirin710.rc \
    etc/init/init.manufacture.rc \
    etc/init/init.platform.rc \
    etc/init/modemchr_service.rc \
    etc/init/modemlog_service.rc \
    etc/init/recovery/init.recovery.huawei.rc \
    etc/init/vendor.huawei.hardware.audio@4.0-service.rc \
    etc/init/vendor.huawei.hardware.biometrics.hwfacerecognize@1.1-service.rc \
    etc/init/vendor.huawei.hardware.dolby.dms@1.0-service.rc \
    etc/init/vendor.huawei.hardware.fm@1.0-service.rc \
    etc/init/vendor.huawei.hardware.hwupdate@1.0-service.rc \
    etc/init/vendor.huawei.hardware.kds@1.0-service.rc \
    etc/init/vendor.huawei.hardware.tp@1.0-service.rc \
    etc/initi/connectivity/init.connectivity.gps.rc \
    etc/modemConfig/observe_config_encryt.xml \
    etc/native_packages.xml \
    bin/hw/android.hardware.media.omx@1.0-service \
    default.prop \
    etc/vintf/compatibility_matrix.xml \
    bin/awk \
    bin/grep \
    bin/sh \
    bin/toolbox \
    bin/toybox_vendor \
    bin/vndservice \
    bin/vndservicemanager

$(foreach script,$(marie_legacy_vendor_files), \
    $(eval marie_legacy_src := $(LOCAL_PATH)/proprietary/vendor/$(script)) \
    $(eval marie_legacy_dst := $(TARGET_OUT_VENDOR)/$(script)) \
    $(eval $(call copy-one-file,$(marie_legacy_src),$(marie_legacy_dst))) \
    $(eval ALL_DEFAULT_INSTALLED_MODULES += $(marie_legacy_dst)))
