from smbus2 import SMBusWrapper
from time import sleep
SDA = 0x08
sleep(2)
while True:
    try:
        with SMBusWrapper(1) as bus:
            data = bus.read_i2c_block_data(SDA,99,2)
            print('Offset {}, data {}'.format(data[0], data[1]))
    except:
        print("error")
    sleep(0.0005)