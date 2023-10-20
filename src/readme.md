# rs4x4

![rs4x4](https://github.com/rakib-shahid/rs4x4/blob/main/miscellaneousCode/imageManipulation/pic.jpg?raw=true)

A 4x4 macropad built with the YD-RP2040, has a 128x64 OLED display, and rgb lighting
[original animation source](https://gifer.com/en/1F4J)

* Keyboard Maintainer: [Rakib Shahid](https://github.com/rakib-shahid)
* Hardware Supported: YD-RP2040, 128x64 OLED
* Hardware Availability: [YD-RP2040](https://www.aliexpress.us/item/3256805028604606.html?spm=a2g0o.productlist.main.21.31d2ddc8WyBH13&algo_pvid=16302719-51e0-4493-adfe-9f8661a4c56f&algo_exp_id=16302719-51e0-4493-adfe-9f8661a4c56f-10&pdp_npi=4%40dis%21USD%211.69%211.39%21%21%211.69%21%21%402101c80016977784593405416e18ba%2112000032212849299%21sea%21US%212965339367%21&curPageLogUid=qeTmb6BkfQnN)

Make example for this keyboard (after setting up your build environment):

    make rs4x4:vial

Flashing example for this keyboard:

    hold boot button (BOOT or 7) and copy uf2

See the [build environment setup](https://docs.qmk.fm/#/getting_started_build_tools) and the [make instructions](https://docs.qmk.fm/#/getting_started_make_guide) for more information. Brand new to QMK? Start with our [Complete Newbs Guide](https://docs.qmk.fm/#/newbs).

## Bootloader

Enter the bootloader in 3 ways:

* **Bootmagic reset**: Hold down the key at (0,0) in the matrix (top left key or 7) and plug in the keyboard
* **Physical reset button**: Briefly press the button on the back of the PCB - some may have pads you must short instead
* **Keycode in layout**: Press the key mapped to `QK_BOOT` if it is available
