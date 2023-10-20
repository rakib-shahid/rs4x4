// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include <qp.h>
// #include "testingimage.qgf.h"


// static painter_image_handle_t image;
// painter_device_t qp_st7735_make_spi_device(uint16_t 130, uint16_t 161, pin_t chip_select_pin, pin_t dc_pin, pin_t reset_pin, uint16_t spi_divisor, int spi_mode);
// painter_device_t display = painter_device_t qp_st7735_make_spi_device(130, 161, chip_select_pin, GP16, reset_pin, 0, 3);


static painter_device_t display = NULL;
// static painter_image_handle_t image = NULL;

// when KB starts running, set things up
void keyboard_post_init_user(void) {
    debug_enable = true;
    display = qp_st7735_make_spi_device(130, 161, GP18, GP16, GP17, 0, 3);
    // qp_set_viewport_offsets(display, 35, 0);
    qp_init(display, QP_ROTATION_0);
     // i like filling black on start

    // image = qp_load_image_mem(testingimage.qgf);
}

bool process_record_user(uint16_t keycode, keyrecord_t * record) {
    // this is a terrible idea btw, it is kinda slow drawing an image and you are doing it each time you press a key
    if (record->event.pressed) {
        qp_rect(display, 0,0,130, 161, 170, 255, 255, true);
        // qp_drawimage(display, (130 - image->width), (161 - image->height), image);
    }

    return true;
}


const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

    [0] = LAYOUT_ortho_1x1(
        KC_W
    )
};
