// Copyright 2023 rakib-shahid (@rakib-shahid)
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
#define SPI_MOSI_PIN GP7
#define SPI_SCK_PIN GP6
#define QUANTUM_PAINTER_DEBUG TRUE
// #define QUANTUM_PAINTER_SUPPORTS_NATIVE_COLORS TRUE
#define QUANTUM_PAINTER_SUPPORTS_256_PALETTE TRUE
#define RP2040_FLASH_W25Q080

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT
