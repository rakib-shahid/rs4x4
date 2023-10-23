// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include <qp.h>
// #include "sanacut.qgf.h"
#include "monaco130.qgf.h"
#include "aovel.qff.h"
#include "qp_st77xx_opcodes.h"
#include "qp_st7735_opcodes.h"
#include "qp_comms.h"
#include "color.h"
#include "raw_hid.h"

static painter_device_t display = NULL;
static painter_image_handle_t image = NULL;

bool qp_st7735_init(painter_device_t device, painter_rotation_t rotation) {
    // clang-format off
    const uint8_t st7735_init_sequence[] = {
        // default
        // // Command,                 Delay, N, Data[N]
        ST77XX_CMD_RESET,            120,  0,          // SWRESET
        ST77XX_CMD_SLEEP_OFF,          5,  0,          // SLPOUT
        ST77XX_SET_PIX_FMT,            0,  1, 0x5,    // COLMOD (adafruit uses 0x5, but those bits look unused anyway)
        ST77XX_CMD_INVERT_OFF,         0,  0,          // _INVOFF
        ST77XX_CMD_NORMAL_ON,          0,  0,          // _NORON
        ST77XX_CMD_DISPLAY_ON,        20,  0,           // _DISPON

        // gamma fix (values copied from adafruit_st7735r)
        ST7735_SET_PGAMMA,           0,0x10,0x02,0x1c,0x07,0x12,0x37,0x32,0x29,0x2d,0x29,0x25,0x2B,0x39,0x00,0x01,0x03,0x10,
        ST7735_SET_NGAMMA,           0,0x10,0x03,0x1d,0x07,0x06,0x2E,0x2C,0x29,0x2D,0x2E,0x2E,0x37,0x3F,0x00,0x00,0x02,0x10

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


void housekeeping_task_user(void){
    if (last_input_activity_elapsed() > QUANTUM_PAINTER_DISPLAY_TIMEOUT){
        qp_rect(display, 0,0,130, 161, HSV_BLACK, true);
    }
}


// hid function
void raw_hid_receive(uint8_t *data, uint8_t length) {
    uint8_t response[length];
    memset(response, 0, length);
    response[0] = 'B';

    if(data[0] == 'A') {
        raw_hid_send(response, length);
    }
}

static painter_font_handle_t my_font;


// when KB starts running, set things up
void keyboard_post_init_user(void) {
    setPinOutput(GP27);
    writePinHigh(GP27);


    setPinOutput(GP29);
    writePinHigh(GP29);
    // debug_enable = true;
    display = qp_st7735_make_spi_device(130, 161, GP18, GP16, GP17, 0, 3);
    qp_init(display, QP_ROTATION_180);
    qp_rect(display, 0,0,130, 161, HSV_BLACK, true);
    image = qp_load_image_mem(gfx_monaco130);
    // image = qp_load_image_mem(gfx_sanacut);
    qp_animate(display, 0, 0, image);
    my_font = qp_load_font_mem(font_aovel);
    static const char *testText = "Hello from QMK!";
    qp_drawtext(display, 0, 0, my_font, testText);
}

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
