# How to wire
## How to connect your Raspberry Pi Model B with the RFID RC522.

| Name on RFID Chip | Pin # | Pin name on Raspberry |
|:------:|:-------:|:------------:|
| IRQ  | None  | None       |
| SDA/NSS  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| GND  | Any   | Any Ground |
| RST  | 22    | GPIO25     |
| 3.3V/VCC | 1     | 3V3        |

You can use [this website](http://raspberrypi.ws/) as reference for the pins on the Raspberry Pi.
