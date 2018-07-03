run:
	mkdir -p logs
	sudo -E python3 run.py

configure:
	mkdir -p logs
	python3 setup.py

install:
	sudo apt-get install -y python-smbus i2c-tools
	sudo pip3 install -r requirements.txt
	mkdir -p component/components/lib
	curl --silent https://raw.githubusercontent.com/mxgxw/MFRC522-python/master/MFRC522.py > component/components/lib/MFRC522.py
	cd component/components/lib && wget http://tutorials-raspberrypi.de/wp-content/uploads/scripts/hd44780_i2c.zip -O temp.zip; unzip -o temp.zip; rm temp.zip
	sed -i -e 's/import i2c_lib/from component.components.lib import i2c_lib/g' component/components/lib/lcddriver.py
	2to3 -w component/components/lib/MFRC522.py
	sudo sed -i -e 's/\#dtparam=spi=on/dtparam=spi=on/g' /boot/config.txt
	sudo echo 'i2c-bcm2708' >> modules
	sudo echo 'i2c-dev' >> modules
	sudo cp modules /etc/modules
	echo "Configure IC2 now."
	sudo raspi-config
	echo "Restarting server..."
	sleep 10
	sudo reboot
