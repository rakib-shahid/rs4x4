

QUANTUM_PAINTER_ENABLE 		= yes
QUANTUM_PAINTER_DRIVERS 	+= st7735_spi
QUANTUM_PAINTER_NUM_IMAGES	= 1
QUANTUM_LIB_SRC += spi_master.c

SRC += monaco130.qgf.c
SRC += aovel.qff.c
# SRC += sanacut.qgf.c


EXTRALDFLAGS = -Wl,--defsym,FLASH_LEN=8192k
RAW_ENABLE = yes
# CONSOLE_ENABLE = yes