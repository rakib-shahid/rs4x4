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
#define SPI_MOSI_PIN GP11
#define SPI_SCK_PIN GP10
#define QUANTUM_PAINTER_DEBUG TRUE

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT
