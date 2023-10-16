// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include <qp.h>
#include "monaco130c16.qgf.h"
// #include "fma.qgf.h"
#include "qp_st77xx_opcodes.h"
#include "qp_comms.h"
#include "color.h"

// painter_device_t qp_st7735_make_spi_device(uint16_t 130, uint16_t 161, pin_t chip_select_pin, pin_t dc_pin, pin_t reset_pin, uint16_t spi_divisor, int spi_mode);
// painter_device_t display = painter_device_t qp_st7735_make_spi_device(130, 161, chip_select_pin, GP16, reset_pin, 0, 3);


static painter_device_t display = NULL;
static painter_image_handle_t image = NULL;
bool qp_st7735_init(painter_device_t device, painter_rotation_t rotation) {
    // clang-format off
    const uint8_t st7735_init_sequence[] = {
        // Command,                 Delay, N, Data[N]
        ST77XX_CMD_RESET,            120,  0,
        ST77XX_CMD_SLEEP_OFF,          5,  0,
        ST77XX_CMD_INVERT_OFF,          0,  0,
        ST77XX_SET_PIX_FMT,            0,  1, 0x55,
        ST77XX_CMD_NORMAL_ON,          0,  0,
        ST77XX_CMD_DISPLAY_ON,        20,  0
    };
    // clang-format on
    qp_comms_bulk_command_sequence(device, st7735_init_sequence, sizeof(st7735_init_sequence));

    // Configure the rotation (i.e. the ordering and direction of memory writes in GRAM)
    const uint8_t madctl[] = {
        [QP_ROTATION_0]   = ST77XX_MADCTL_RGB,
        [QP_ROTATION_90]  = ST77XX_MADCTL_RGB | ST77XX_MADCTL_MX | ST77XX_MADCTL_MV,
        [QP_ROTATION_180] = ST77XX_MADCTL_RGB | ST77XX_MADCTL_MX | ST77XX_MADCTL_MY,
        [QP_ROTATION_270] = ST77XX_MADCTL_RGB | ST77XX_MADCTL_MV | ST77XX_MADCTL_MY,
    };
    qp_comms_command_databyte(device, ST77XX_SET_MADCTL, madctl[rotation]);

    return true;
}
// when KB starts running, set things up
void keyboard_post_init_user(void) {
    setPinOutput(GP29);
    writePinHigh(GP29);
    debug_enable = true;
    display = qp_st7735_make_spi_device(130, 161, GP18, GP16, GP17, 0, 3);
    qp_init(display, QP_ROTATION_180);
    qp_rect(display, 0,0,130, 161, HSV_BLACK, true);
    image = qp_load_image_mem(gfx_monaco130c16);
    qp_animate(display, 0, 0, image);
}
int i = 0;
bool process_record_user(uint16_t keycode, keyrecord_t * record) {
    if (record->event.pressed) {

    }

    return true;
}


const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

    [0] = LAYOUT_ortho_1x1(
        KC_W
    )
};
