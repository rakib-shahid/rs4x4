// Copyright 2023 Rakib Shahid (@rakib-shahid)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#define OLED_DISPLAY_128X64

#define I2C1_SCL_PIN        GP5
#define I2C1_SDA_PIN        GP4
#define I2C_DRIVER I2CD0
#define VIAL_KEYBOARD_UID {0x0A, 0x06, 0x79, 0xE5, 0x2F, 0x50, 0xAE, 0x24}

#define WS2812_DI_PIN GP23
#define RGBLED_NUM 1
#define RGBLIGHT_LAYERS
#define NOP_FUDGE 0.4