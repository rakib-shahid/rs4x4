// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include <qp.h>
#include "sanacut.qgf.h"
#include "monacosquare.qgf.h"
#include "scp.qff.h"
#include "qp_st77xx_opcodes.h"
#include "qp_st7735_opcodes.h"
#include "qp_comms.h"
#include "color.h"
#include "raw_hid.h"

static painter_device_t display = NULL;
static painter_image_handle_t image = NULL;
static painter_font_handle_t my_font;

static char textArr[50];
static char test[] = "Initial";

// uint8_t framebuffer[SURFACE_REQUIRED_BUFFER_BYTE_SIZE(WIDTH, HEIGHT, 16)] = {0}; // this is where your image data is stored 
// painter_device_t surface = qp_make_rgb565_surface(WIDTH, HEIGHT, (void *)framebuffer);


static deferred_token my_anim;
static bool animating = false;

// storage for arguments passed to the executor
// typedef struct {
//     painter_device_t device;
//     uint16_t x;
//     uint16_t y;
//     painter_font_handle_t font;
//     char *text;
//     uint8_t delay_ms;
//     // colors too?
// } periodic_drawtext_args_t;

// executor logic
// uint32_t drawtext_callback(uint32_t trigger_time, void *cb_arg) {
//     // periodic_drawtext_args_t args = *(periodic_drawtext_args_t *)cb_arg;

//     bool ret = qp_drawtext(display, 0, 0, my_font, textArr);
    
//     if (ret) {
//         return 17;
//     }
    
//     // stop repeating if function failed to draw
//     free(textArr);
//     return 0;
// }




// void toggleAnimation(bool animating){
//     if (!animating){
//         my_anim = qp_animate(display, 0, 10, image);
//         animating = true;
//     }
//     else {
//         qp_stop_animation(my_anim);
//         animating = false;
//     }
// }

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
    if (last_input_activity_elapsed() > 60000){
        // turn animation off on timeout
        if (animating){
            setPinOutput(GP29);
            writePinLow(GP29);
            qp_stop_animation(my_anim);
            animating = false;
        }
        qp_rect(display, 0,0,130, 161, HSV_BLACK, true);
        
    }
    else {
        // turn animation back on
        if (!animating){
            setPinOutput(GP29);
            writePinHigh(GP29);
            my_anim = qp_animate(display, 0, 0, image);
            animating = true;
        }
    }
    if (strstr(textArr,"TWICE") != NULL){
        if (qp_close_image(image)){
            image = qp_load_image_mem(gfx_sanacut);
        }
    }
    else{
        image = qp_load_image_mem(gfx_monacosquare);
    }

    
    
    // lvgl testing
    // if (qp_lvgl_attach(display)){
    //     lv_obj_t * label = lv_label_create(lv_scr_act()); /*Add a label to the screen*/
    //     lv_label_set_text(label, "Hello world");                     /*Set the labels text*/
    //     lv_obj_align(label, LV_ALIGN_CENTER, 0, 0);
    // }
}

// hid function
void raw_hid_receive(uint8_t *data, uint8_t length) {
    uint8_t response[length];
    memset(response, 0, length);
    char testString[] = "Responded";
    for (int i = 0; i < sizeof(testString)/sizeof(testString[0]);i++){
        response[i] = testString[i];
    }
    raw_hid_send(response, length);
    // textArr = data;
    strcpy(textArr,(char *)data);
    // textArr = ;
    qp_rect(display, 0,131,130, 161, HSV_BLACK, true);
    qp_drawtext(display, 2, 138, my_font, textArr);

}


// when KB starts running, set things up
void keyboard_post_init_user(void) {
    // backlight
    setPinOutput(GP29);
    writePinHigh(GP29);

    // debug_enable = true;

    
    
    // create display
    display = qp_st7735_make_spi_device(130, 161, GP18, GP16, GP17, 0, 3);
    qp_init(display, QP_ROTATION_180);
    qp_rect(display, 0,0,130, 161, HSV_BLACK, true);

    // load image
    image = qp_load_image_mem(gfx_monacosquare);
    // image = qp_load_image_mem(gfx_sanacut);

    // periodic_drawtext_args_t args = {display, 2, 2, my_font, textArr,100};
    // defer_exec(100, drawtext_callback, NULL);
    strcpy(textArr, test);
    textArr[sizeof(textArr) - 1] = '\0';

    // animate image
    my_anim = qp_animate(display, 0, 0, image);
    animating = true;

    // load font
    my_font = qp_load_font_mem(font_scp);
    qp_drawtext(display, 2, 138, my_font, textArr);

    
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
