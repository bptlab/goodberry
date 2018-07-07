# How to wire
You can use [this website](http://raspberrypi.ws/) as reference for the pins on the Raspberry Pi.

## How to connect your Raspberry Pi Model B with the RFID RC522.

| Name on RFID Chip | Pin # | Pin name on Raspberry |
|:------:|:-------:|:------------:|
| IRQ  | None  | None       |
| SDA/NSS  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| GND  |    | Any Ground |
| RST  | 22    | GPIO25     |
| 3.3V/VCC | 1     | 3V3        |

## How to connect your Raspberry Pi Model B with the HD44780 display with I2C adapter.

| Name on I2C adapter | Pin # | Pin name on Raspberry |
|:------:|:-------:|:------------:|
| SCC  | 2  | 5V                  |
| GND  | 6  | GND                 |
| SDA  | 3  | GPIO2/SDA           |
| SCL | 5   | GPIO3/SCL           |
