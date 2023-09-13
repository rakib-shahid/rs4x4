// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H

#ifdef OLED_ENABLE

#define FRAME_DURATION 333

uint32_t timer = 0;
uint8_t current_frame = 0;

static void render_animation(void){
    // '1bw', 128x64px
    static const  char frames1bw [] PROGMEM = {
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x1f, 0xef, 
        0xdf, 0xdf, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x0f, 0xf0, 0xf0, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xfe, 0xfe, 0xf9, 0xc7, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 
        0xcf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0x7f, 0xbf, 0xcf, 0xcf, 0xf7, 0x0f, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x3f, 0xdf, 
        0xdf, 0xe7, 0xe7, 0xe7, 0xe7, 0xe7, 0xe7, 0xe7, 0xdb, 0x9c, 0x9c, 0x7f, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfb, 0xfb, 0xfb, 0xfc, 0xfc, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfd, 0xfd, 0xfd, 0xfd, 0xf3, 0xf3, 0xf3, 
        0xf3, 0xef, 0xef, 0xef, 0xef, 0x9f, 0x9f, 0x9f, 0x9f, 0x9f, 0x7f, 0x7f, 0x03, 0x03, 0xfc, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x03, 0x03, 0xff, 0xff, 
        0xe3, 0xe3, 0xe3, 0xff, 0xff, 0xff, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0xfe, 0xe1, 0x1f, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 0xbf, 0xcf, 0xcf, 0xcf, 0xcf, 0x3f, 0x3f, 0xbe, 0xbe, 
        0xbe, 0x7e, 0x79, 0x79, 0x79, 0xf9, 0xf7, 0xf7, 0xf7, 0xf7, 0xf7, 0xcf, 0xcf, 0xcf, 0xc0, 0xbf, 
        0xbf, 0xbf, 0xbf, 0x7f, 0x7f, 0x7f, 0x7f, 0xfe, 0xfe, 0xf9, 0xfe, 0xfe, 0xf9, 0xf7, 0xf7, 0xf9, 
        0xfe, 0xff, 0xff, 0xff, 0xf8, 0xf8, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0xf0, 0x8f, 0x7f, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0x1f, 0x07, 0x1b, 0x1b, 0x1d, 0x3e, 0x3e, 0x1f, 0x27, 0x27, 0xfb, 0xfd, 0x3e, 0x3e, 0xdf, 0xe7, 
        0xe7, 0xfa, 0x3c, 0x3c, 0xde, 0xe5, 0xf9, 0xf9, 0x3d, 0xdb, 0xdb, 0xe3, 0xfb, 0xfb, 0x27, 0xc7, 
        0xe7, 0xe7, 0xdf, 0x1e, 0x1e, 0xde, 0x3e, 0x3d, 0x3d, 0x3d, 0xfd, 0xfd, 0xfb, 0xfb, 0xfb, 0xfb, 
        0xe7, 0xe7, 0xe7, 0x27, 0xdf, 0xdf, 0xe7, 0xfb, 0xfb, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xfe, 0xfc, 0xfc, 0xfc, 0xfc, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xe0, 0xe0, 0xe0, 0xe0, 0x81, 0x81, 
        0x81, 0x80, 0x03, 0x03, 0x03, 0x01, 0x0e, 0x0e, 0x0f, 0x03, 0x03, 0x1d, 0x1e, 0x1e, 0x0f, 0x73, 
        0x7d, 0x7d, 0x1e, 0xef, 0xef, 0xf3, 0x7d, 0x9e, 0x9e, 0xef, 0xf2, 0xf2, 0x7c, 0x9e, 0x9e, 0x81, 
        0x7d, 0xfe, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 
        0x7f, 0x1f, 0x1f, 0x1f, 0xef, 0xf3, 0xf3, 0xf3, 0xf3, 0xf3, 0xef, 0xee, 0xe1, 0xe1, 0x9f, 0x9f, 
        0x9f, 0x9f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfc, 0xfc, 0xfc, 0xf8, 0xf8, 0xf8, 0xf8, 0xf0, 
        0xf0, 0xf0, 0xf0, 0xc0, 0xc0, 0xc0, 0xc0, 0x83, 0x83, 0x83, 0x80, 0x80, 0x07, 0x07, 0x07, 0x03, 
        0x0c, 0x0b, 0x0b, 0x03, 0x37, 0x37, 0x37, 0x07, 0x07, 0x73, 0x7b, 0x7c, 0x7c, 0x3c, 0x0f, 0x0f, 
        0x87, 0xc3, 0xf0, 0xf0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfc, 0xfc, 0xfc, 0xfb, 0xfb, 0xfb, 0xfb, 0xf7, 
        0xf7, 0xf7, 0xf7, 0xcf, 0xcf, 0xcf, 0xcf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xff, 0xff, 0xff, 0xff
    };
    // '2bw', 128x64px
    static const  char frames2bw [] PROGMEM = {
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x1f, 0xef, 
        0xdf, 0xdf, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x0f, 0xf0, 0xf0, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xfe, 0xfe, 0xf9, 0xc7, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 
        0xcf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0x7f, 0xbf, 0xcf, 0xcf, 0xf7, 0x0f, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0x7f, 0x9f, 0xe7, 0xe7, 0xfb, 0xfc, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfb, 0xfb, 0xfb, 0xfc, 0xfc, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfd, 0xfd, 0xfd, 0xfd, 0xf3, 0xf3, 0xf3, 
        0xf3, 0xef, 0xef, 0xef, 0xef, 0x9f, 0x9f, 0x9f, 0x9f, 0x9f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0x1f, 
        0x1f, 0xe3, 0xfd, 0xfd, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xe3, 0xe3, 0xe3, 0xff, 0xff, 0xff, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 
        0x7f, 0x7f, 0xff, 0xff, 0xff, 0xfe, 0xfe, 0xe1, 0x1f, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0x7f, 0x7f, 0xbf, 0xcf, 0xcf, 0xcf, 0xcf, 0x3f, 0x3f, 0xc0, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x7f, 0xbf, 
        0xbf, 0xbf, 0xbf, 0x7f, 0x7f, 0x7f, 0x7f, 0xfe, 0xfe, 0xf9, 0xfe, 0xfe, 0xf9, 0xf7, 0xf7, 0xf9, 
        0xfe, 0xff, 0xff, 0xff, 0xf8, 0xf8, 0xf8, 0x3f, 0x3f, 0xc1, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xfe, 0xfe, 0xf8, 0xc7, 0xc7, 0xff, 0xf0, 0xf0, 0x8f, 0x7f, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0x1f, 0x07, 0x1b, 0x1b, 0x1d, 0x3e, 0x3e, 0x1f, 0x27, 0x27, 0xfb, 0xfd, 0x38, 0x38, 0xc7, 0xdf, 
        0xdf, 0xdf, 0x1f, 0x1f, 0xdf, 0xe7, 0xe7, 0xe7, 0x3b, 0xdb, 0xdb, 0xe1, 0xf9, 0xf9, 0x26, 0xc7, 
        0xe7, 0xe7, 0xdf, 0x1e, 0x1e, 0xde, 0x3e, 0x3d, 0x3d, 0x3d, 0xfd, 0xfd, 0xfb, 0xfb, 0xfb, 0xfb, 
        0xe7, 0xe7, 0xe7, 0xe7, 0xdf, 0xdf, 0xc3, 0xdc, 0xdc, 0x3f, 0x3f, 0x3f, 0x3f, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xfe, 0xfc, 0xfc, 0xfc, 0xfc, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xe0, 0xe0, 0xe0, 0xe0, 0x81, 0x81, 
        0x81, 0x80, 0x03, 0x03, 0x03, 0x01, 0x0e, 0x0e, 0x0f, 0x03, 0x03, 0x1d, 0x1e, 0x1e, 0x0f, 0x73, 
        0x7d, 0x7d, 0x1e, 0xef, 0xef, 0xf3, 0x7d, 0x9e, 0x9e, 0xef, 0xf2, 0xf2, 0x7c, 0x9e, 0x9e, 0xed, 
        0xf1, 0x7d, 0x7d, 0x93, 0xe3, 0xe3, 0xf3, 0x6f, 0x6f, 0x8f, 0xef, 0x9f, 0x9f, 0x1e, 0x9e, 0x9e, 
        0x7e, 0x7d, 0x7d, 0x7d, 0xfd, 0xf3, 0xf3, 0xf3, 0xf3, 0xf3, 0xef, 0xee, 0xe1, 0xe1, 0x9f, 0x9f, 
        0x9f, 0x9f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfc, 0xfc, 0xfc, 0xf8, 0xf8, 0xf8, 0xf8, 0xf0, 
        0xf0, 0xf0, 0xf0, 0xc0, 0xc0, 0xc0, 0xc0, 0x83, 0x83, 0x83, 0x80, 0x80, 0x07, 0x07, 0x07, 0x03, 
        0x0c, 0x0f, 0x0f, 0x07, 0x3b, 0x3b, 0x3c, 0x0f, 0x0f, 0x77, 0x7b, 0x7c, 0x7c, 0x3f, 0x0f, 0x0f, 
        0x87, 0xc3, 0xf0, 0xf0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xfc, 0xfc, 0xfc, 0xfc, 0xfb, 0xfb, 0xfb, 0xfb, 0xf7, 
        0xf7, 0xf7, 0xf7, 0xcf, 0xcf, 0xcf, 0xcf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xff, 0xff, 0xff, 0xff
    };

    // Array of all bitmaps for convenience. (Total bytes used to store images in PROGMEM = 2080)
    const  char* framesallArray[2] = {
        frames1bw,
        frames2bw
    };



    uint16_t frame_sizes[2] = {
        sizeof(frames1bw),
        sizeof(frames2bw)
    };
    // if (timer_elapsed(timer) > FRAME_DURATION){
    //     timer = timer_read();

    current_frame = (current_frame + 1) % (sizeof(framesallArray) / sizeof(framesallArray[0]));

    oled_write_raw_P(framesallArray[current_frame], frame_sizes[current_frame]);
    // }

}
bool process_record_user(uint16_t keycode, keyrecord_t * record) {
    if (record->event.pressed) {
        render_animation();
    }
    return true;
}

bool oled_task_user(void) {
    
    // oled_write_P(PSTR("Hello world"), false);
    // render_animation();
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
    [0] = LAYOUT_ortho_1x1(
        KC_F
    )
};