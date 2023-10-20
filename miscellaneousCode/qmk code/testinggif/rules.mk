# MCU name
MCU = RP2040

# Bootloader selection
BOOTLOADER = rp2040
# Quantum Painter for ST7735 128x160
QUANTUM_PAINTER_ENABLE 		= yes
QUANTUM_PAINTER_DRIVERS 	+= st7735_spi
QUANTUM_PAINTER_NUM_IMAGES	= 1
QUANTUM_LIB_SRC += spi_master.c

# SRC += sana1.qgf.c

# SRC += sana128.qgf.c
SRC += monaco130c16.qgf.c
# SRC += sana240.qgf.c
EXTRALDFLAGS = -Wl,--defsym,FLASH_LEN=8192k
# SRC += fma.qgf.c
# CONSOLE_ENABLE = yes
# SRC += testingimage.qgf.c