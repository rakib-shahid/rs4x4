// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H
#include "planets.c"
#include "print.h"
// #include "raw_hid.h"

#define KC_CUT LCTL(KC_X)
#define KC_COPY LCTL(KC_C)
#define KC_PASTE LCTL(KC_V)

#ifdef OLED_ENABLE

static char textArr[31];

enum layer_names{
    _NUMPAD,
    _MEDIA,
    _LAYER3,
    _LAYER4
};

void raw_hid_receive_kb(uint8_t *data, uint8_t length) {
    uint8_t *command_id = &(data[0]);
    if (data[0] == 0xFF){
        if (strncmp(textArr,(char *)(data+1),strlen(textArr)-1) != 0){
            strcpy(textArr,"\0");
            strcpy(textArr,(char *)(data+1));
            uprintf("new hid message received: %s\n",textArr);
        }
    }
    if (data[0] == 0xCC){
        uprintf("Image data received!\n");
    }
    
    // oled_set_cursor(0, 1);
    // oled_write(textArr, false);
    *command_id         = id_unhandled;
}

bool process_record_user(uint16_t keycode, keyrecord_t * record) {
    if (record->event.pressed) {
        // nothing yet
    }
    return true;
}

void keyboard_post_init_user(void) {
    // nothing yet
    debug_enable = true;
}

bool oled_task_user(void) {
    if (last_input_activity_elapsed() > OLED_TIMEOUT && last_led_activity_elapsed() > OLED_TIMEOUT) {
        // turn off screen
        oled_off();
        // turn off rgb light
        sethsv(0,0,0, (LED_TYPE *)&led[0]);
        rgblight_set();
        return false;
    }

    // animate
    render_big_animation();


    
    // caps lock light
    bool caps_on = host_keyboard_led_state().caps_lock;
    if (caps_on) {
        sethsv(0,0,30, (LED_TYPE *)&led[0]);
        rgblight_set();
    }

    oled_set_cursor(0, 7);
    switch(get_highest_layer(layer_state)){
        case    _NUMPAD:
            oled_write("Numpad Layer", false);
            if (!caps_on) {
                sethsv(127,255,30, (LED_TYPE *)&led[0]);
                rgblight_set();
            }
            break;
        case    _MEDIA:
            oled_write("Media Layer", false);
            if (!caps_on) {
                sethsv(201,255,30, (LED_TYPE *)&led[0]);
                rgblight_set();
            }
            break;
        case    _LAYER3:
            oled_write("Navigation Layer", false);
            if (!caps_on) {
                sethsv(85,255,30, (LED_TYPE *)&led[0]);
                rgblight_set();
            }
            break;
        case    _LAYER4:
            oled_write("Macro Layer", false);
            if (!caps_on) {
                sethsv(21,255,30, (LED_TYPE *)&led[0]);
                rgblight_set();
            }
            break;
    }

    oled_set_cursor(0, 0);
    oled_write(textArr, false);
    return false;
}
#endif

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌───┬───┬───┬───┐
     * │ 7 │ 8 │ 9 │ / │
     * ├───┼───┼───┼───┤
     * │ 4 │ 5 │ 6 │ * │
     * ├───┼───┼───┼───┤
     * │ 1 │ 2 │ 3 │ - │
     * ├───┼───┼───┼───┤
     * │ 0 │ . │Ent│ + │
     * └───┴───┴───┴───┘
     */
    //  NUMPAD
    [0] = LAYOUT_ortho_4x4(
        KC_KP_7,    KC_KP_8,    KC_KP_9,    KC_KP_MINUS,
        KC_KP_4,    KC_KP_5,    KC_KP_6,    KC_KP_PLUS,
        KC_KP_1,    KC_KP_2,    KC_KP_3,    KC_KP_ASTERISK,
        TO(1),      KC_KP_0,    KC_KP_DOT,  KC_KP_SLASH
    ),
    // MEDIA KEYS
    [1] = LAYOUT_ortho_4x4(
        KC_FIND,                KC_CAPS_LOCK,                KC_WH_U,                KC_AUDIO_MUTE,
        KC_MEDIA_PREV_TRACK,    KC_MPLY,    KC_MEDIA_NEXT_TRACK,    KC_AUDIO_VOL_UP,
        KC_CALC,                KC_MYCM,                KC_WH_D,                KC_AUDIO_VOL_DOWN,
        TO(2),                  KC_CUT,                 KC_COPY,                KC_PASTE
    ),
    // NAVIGATION KEYS
    [2] = LAYOUT_ortho_4x4(
        KC_INSERT,      KC_HOME,    KC_PGUP,        KC_PSCR,
        KC_DELETE,      KC_END,     KC_PGDN,        KC_SCROLL_LOCK,
        KC_COPY,        KC_PASTE,    KC_UP,          KC_PAUSE,
        TO(3),          KC_LEFT,    KC_DOWN,        KC_RIGHT
    ),
    // blank for now
    [3] = LAYOUT_ortho_4x4(
        KC_NO,      KC_NO,      KC_NO,      KC_NO,
        KC_NO,      KC_NO,      KC_NO,      KC_NO,
        KC_NO ,     KC_NO,      KC_NO,      KC_NO,
        TO(0),      KC_NO,      KC_NO,      KC_NO
    )
};