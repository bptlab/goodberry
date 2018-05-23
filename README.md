# Goodberry
This service implements multiple IoT sensors and actuators on a Raspberry Pi. The event data is sent to an arbitrary webservice.
* Button (Observer)
* Pi-Camera (Action)	
* Display (segmented) (Action)	
* NFC (Action + Observer)	
* Binary (called vibration) (Observer)

## Requirements
* Raspberry Pi with possibility to connect a GPIO board and [Raspbian](https://www.raspberrypi.org/downloads/raspbian/). The image must be flashed onto a microSD card.
* Minimal development environment. To install this, execute 
```
curl --silent https://raw.githubusercontent.com/tommartensen/raspbian-minimal-dev/master/raspbian-setup.sh | sh
```

## Installation
1. Clone this repository onto your Raspberry Pi. 
1. Run `make install` to install dependencies. 
   **WARNING**: This reboots the Raspberry as needed for activation of SPI.
1. Run `source berry.env` after you filled in the necessary information.

## Acknowledgements
* [mxgxw](https://github.com/mxgxw/MFRC522-python/blob/master/LICENSE.txt) for the NFC reader module
* [MaximilianV](https://github.com/MaximilianV/thingberry/blob/master/LICENSE) for the basic Thingberry
* [tutorials-raspberrypi.de](https://tutorials-raspberrypi.de/hd44780-lcd-display-per-i2c-mit-dem-raspberry-pi-ansteuern/)
