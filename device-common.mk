#
# Copyright (C) 2023 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

COMMON_PATH := device/samsung/universal9830-common

# Boot animation
TARGET_BOOTANIMATION_PRELOAD := true
TARGET_BOOTANIMATION_TEXTURE_CACHE := true

# DRM
PRODUCT_PACKAGES += \
    android.hardware.drm@1.3.vendor:32

# Dynamic Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# GNSS
PRODUCT_PACKAGES += \
    android.hardware.gnss@2.1.vendor:64 \
    init.gps.rc

# Init
PRODUCT_PACKAGES += \
    fstab.exynos990 \
    fstab.exynos990.ramdisk \
    init.exynos990.rc.recovery \
    init.exynos990.rc \
    ueventd.exynos990.rc

# Neuralnetworks
PRODUCT_PACKAGES += \
    android.hardware.neuralnetworks@1.3.vendor \
    android.hidl.allocator@1.0.vendor \
    libtextclassifier_hash.vendor \
    libhidlmemory.vendor

# Power
PRODUCT_PACKAGES += \
    android.hardware.power@1.0.vendor:64

# Recovery
PRODUCT_PACKAGES += \
    init.recovery.exynos990.rc

# RIL
PRODUCT_PACKAGES += \
    cass.rc \
    android.hardware.radio@1.4.vendor:64 \
    android.hardware.radio.config@1.2.vendor:64 \
    android.hardware.radio.deprecated@1.0.vendor:64 \
    libdsms_vendor:64
    init.baseband.rc \
    init.vendor.rilchip.rc \
    init.vendor.rilcommon.rc

# Secure Element
PRODUCT_PACKAGES += \
    android.hardware.secure_element@1.2.vendor:64

# Sensors
PRODUCT_PACKAGES += \
    android.hardware.contexthub@1.0.vendor:64

# Shipping API level
PRODUCT_SHIPPING_API_LEVEL := 29

# Soong namespace
PRODUCT_SOONG_NAMESPACES += $(COMMON_PATH)

# TUI
PRODUCT_PACKAGES += \
    teegris_v4.rc \
    pa_daemon_teegris.rc

# USB
PRODUCT_PACKAGES += \
    init.exynos990.usb.rc

# Vaultkeeper
PRODUCT_PACKAGES += \
    vaultkeeper_common.rc

# Setup dalvik vm configs
$(call inherit-product, frameworks/native/build/phone-xhdpi-6144-dalvik-heap.mk)

# Call Samsung LSI board support package makefiles
include hardware/samsung_slsi-linaro/config/BoardConfig9830.mk
$(call inherit-product, hardware/samsung_slsi-linaro/graphics/base/hwcomposer_property.mk)
$(call inherit-product, hardware/samsung_slsi-linaro/config/config.mk)

# Call the proprietary setup
$(call inherit-product, vendor/samsung/universal9830-common/universal9830-common-vendor.mk)
