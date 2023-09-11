// Copyright 2023 Rakib Shahid (@rakib-shahid)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

/*
 * Feature disable options
 *  These options are also useful to firmware size reduction.
 */

/* disable debug print */
//#define NO_DEBUG
/* disable print */
//#define NO_PRINT
#define OLED_DISPLAY_128X64

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT
// #define I2C_DRIVER I2CD1
// #define I2C1_SCL_PIN GP5
// #define I2C1_SDA_PIN GP4
#define I2C_DRIVER I2CD0
#define I2C1_SDA_PIN GP4
#define I2C1_SCL_PIN GP5