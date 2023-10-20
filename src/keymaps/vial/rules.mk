# This file intentionally left blank
# MCU name
MCU = RP2040

# Bootloader selection
BOOTLOADER = rp2040

OLED_ENABLE = yes
LTO_ENABLE = yes

EXTRALDFLAGS = -Wl,--defsym,FLASH_LEN=8192k
VIA_ENABLE = yes
VIAL_ENABLE = yes
VIAL_INSECURE = yes
WS2812_DRIVER = vendor
RGBLIGHT_ENABLE = yes

