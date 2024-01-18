import spidev
import time

# Определение настроек для SPI0
spi0 = spidev.SpiDev()
spi0.open(0, 0)  # Открываем SPI0 CE0
spi0.mode = 0
spi0.max_speed_hz = 5000000

# Определение настроек для SPI1
spi1 = spidev.SpiDev()
spi1.open(1, 1)  # Открываем SPI1 CE1
spi1.mode = 0
spi1.max_speed_hz = 5000000

# Команда чтения температуры из MAX31855
cmd = [0b00000001, 0b00000000, 0b00000000, 0b00000000]

# Функция чтения температуры с датчика MAX31855
def read_temp(spi0):
    
    resp_1 = spi0.xfer2(cmd)
    temp1 = ((resp_1[0] << 8) | resp_1[1]) >> 2  # Преобразование полученных данных в температуру
    if temp1 & 0x8000:
        temp1 -= 0x10000
    return temp1 * 0.25


def read_temp1(spi1):
    
    resp_2 = spi1.xfer2(cmd)
    temp2 = ((resp_2[0] << 8) | resp_2[1]) >> 2 # Преобразование полученных данных в температуру
    if temp2 & 0x8000:
        temp2 -= 0x10000
    return temp2 * 0.25
