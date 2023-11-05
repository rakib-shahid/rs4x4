

QUANTUM_PAINTER_ENABLE 		= yes
QUANTUM_PAINTER_DRIVERS 	+= st7735_spi
# QUANTUM_PAINTER_DRIVERS += rgb565_surface
QUANTUM_PAINTER_NUM_IMAGES	= 1
QUANTUM_LIB_SRC += spi_master.c
# QUANTUM_PAINTER_LVGL_INTEGRATION = yes

# gifs
# SRC += monaco130.qgf.c
SRC += monacosquare.qgf.c
SRC += sanacut.qgf.c

# font
SRC += scp.qff.c



EXTRALDFLAGS = -Wl,--defsym,FLASH_LEN=8192k
# DEFERRED_EXEC_ENABLE = yes
RAW_ENABLE = yes
LTO_ENABLE = yes
# CONSOLE_ENABLE = yes