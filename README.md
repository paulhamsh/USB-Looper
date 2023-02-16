# USB-Looper
A guitar looper pedal which uses a USB audio connection to an amplifier for audio looping.    
No direct guitar input - only via the amp USB audio interface.     
The benefit is that you can record the output of the amp into each track, which is processed with any effects the amp has activated at that point. In this way each track can have different effects.    

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Setup.jpg">

The amp must send processed guitar to the looper pedal over USB and receive audio back from the looper pedal over USB.   

Examples of amps that can do this are:   
- Spark Mini
- Boss Katana

(The Spark 40 amp has a strange pitch-shift issue with USB which makes it unusable for USB audio)   

The pedal is more like a 4 track recorder than a looper - you don't overdub, you record on to new tracks.   
Tracks are not stored on SD card in this version.    

The amp must be capable of USB out and USB in simultaneously.   

The pedal is based on a Raspberry Pi Zero W.  This is because USB host audio is required, and I can't find a microcontroller (ESP32 / Pi 2040 / Arduino / Teensy) that has USB host audio. The TinyUSB library doesn't support it yet. But the Pi, being a Linux machine, has full USB Host capability.  The only downside is slow boot times which can be partially fixed by not running via systemd - see the boot time improvement section later.   

It also needs a USB OTG cable plugged into the 'USB' input of the Pi Zero - to act as the USB host connection.    

This build uses an Adafruit Proto Bonnet to do the wiring for the switches, rotary controller and OLED.   

**Currently the rotary controller doesn't do anything**

# How to use the pedal

Plug in the amp into the OTG cable (before turning on)    
Turn on the pedal by plugging in USB power cable.      

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Control3.jpg" >

The footswitches are labelled STOP, then Tracks 1 to 4. (STOP currently doesn't do anything)      

The OLED will now show the following info.   
Each track has a play and record icon. 
If both are unfilled, then the track is empty.   
If the record icon shows then that track is recording.   
If the play icon shows then that track is playing.   

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Pic1.jpg" width="400" >

Press footswich Track 1 to start track 1 recording.  
The record icon for Track 1 will change to filled.   

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Pic2.jpg" width="400" >

Press footswitch Track 1 again to stop track 1 recording and start playback.   
The Track 1 icons will switch to play.   

The overall loop length is dictated by the length of loop 1.   
The bar at the bottom shows progress in playing back loop 1 - so showing how long the loop is for any other tracks.   

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Pic3.jpg" width="400" >

Press footswitch Track 2 to start track 2 recording...and so on.   

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Pic4.jpg" width="400" >

A long press on footswitch Track 1 to Track 4 will delete the contents of that track.   
 
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Flow.jpg" >

Pressing the STOP footswitch will stop all playback and reset to the start of all tracks.  
Another press on STOP will start playback.   
A long press on STOP will clear all tracks.   

# Hardware build
      
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Top.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Edge.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside%20Pi.jpg" width="400" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside%20OLED.jpg" width="400" >

The wiring schematic.   

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Proto%20Bonnet.jpg" width="500" >

# Installation

Run all this as root - so ```sudo bash``` each time you log in or reboot.   

Create an SD Card with Raspberry Pi OS Lite 32 bit (follow the instructions on the Raspberry Pi website).   
Boot your Pi.    

In the config screen:   
- Create your user: {user} {password}    
- Set locale    
Exit config    

Log in   

Set up a new config using ```raspi-config```    
We need this to have SSH activated as it will be headless once in a pedal.   

```
sudo bash
raspi-config
```

And set the following:   

```
1 System Options   
- S1 Wireless Lan - set SSID and passphrase   

3 Interface options   
- I2 SSH - activate   
- I5 I2C - activate   
- I6 Serial Port - activate   
```

Edit the config.txt file   

```
vi /boot/config.txt
```

Find dtparam=i2c_arm=on and add 

```
dtparam=i2c_arm=on, i2c_arm_baudrate=1000000
```

Get the IP address for later SSH work   

```
ifconfig
```

Update the whole system   

```
apt update
apt full-upgrade
```

At this point you can unplug any monitor and use the Pi headless via SSH - log in via something like PuTTY, using the IP address you captured.   
Also you can use a serial terminal if you prefer.   

Install the required i2c tools     

```
apt-get install i2c-tools
i2cdetect -y 1
```

Should show ```3c```   

Install SSD1306 for Python   
```
apt install python3-pip 
python -m pip install --upgrade pip setuptools wheel
```

This will take a long time    

```
pip3 install Adafruit-SSD1306
pip3 install Adafruit-GPIO
```

Install sound libraries and modules    


```
pip3 install sounddevice soundfile numpy

apt-get install libportaudio2 
apt-get install libasound2-dev
apt-get install libsndfile1
```

Get this code from github.   

```
apt install git

git clone https://github.com/paulhamsh/USB-Looper
mkdir /opt/looper
cp USB-Looper/src/looper8.py /opt/looper/looper.py
cp USB-Looper/src/Ubuntu-Bold.ttf /opt/looper/Ubuntu-Bold.ttf

```

Run the looper program

```
sudo python /opt/looper/looper.py
```


# Boot time reduction

Edit config.txt   

```
vi /boot/config.txt
disable_splash=1
boot_delay=0
```

Edit cmdline.txt - to remove the tty output and adding quiet. Use your own root=PARTUUID not the one below.   

```
vi /boot/cmdline.txt
console=serial0,115200 root=PARTUUID=3b65aa5f-02 rw rootfstype=ext4 fsck.repair=yes quiet rootwait
```

Re-point init from systemd to busybox.   

```
sudo bash
rm /usr/sbin/init
ln -s /usr/bin/busybox /usr/sbin/init
```

And create a new inittab.   

```
vi /etc/inittab
```


```
::sysinit:/bin/mount -t proc proc /proc
::sysinit:/bin/mount -t sysfs sysfs /sys
::sysinit:/bin/mount -o rw /dev/mmcblk0p1 /boot
::sysinit:/usr/sbin/modprobe i2c_bcm2835
::sysinit:/usr/sbin/modprobe i2c_dev
::sysinit:/usr/sbin/modprobe snd-usb-audio
::sysinit:/usr/sbin/modprobe brcmfmac
console::respawn:-/bin/sh
console::once:echo WELCOME TO LOOPER
console::once:/usr/bin/python /opt/looper/looper.py
::shutdown:/bin/umount -a -r
::restart:/sbin/init
::ctrlaltdel:/sbin/reboot
```

# If boot times aren't an issue

You can always add a systemd service as follows.   

Create a shell script to run the looper.   

```
sudo bash
vi /opt/looper/start.sh
```

```
#!/bin/bash
python /opt/looper/looper.py
```

```
chmod a+x /opt/looper/start.sh
```

```
vi /etc/systemd/service/looper.service
```

```
[Unit]
Description=Reboot looper systemd service.

[Service]
Type=simple
ExecStart=/bin/bash /opt/looper/start.sh

[Install]
WantedBy=multi-user.target
```

```
chmod chmod u=rw,g=rw,o=r /etc/systemd/system/looper.service
systemctl enable looper.service
```


# Use FT232 USB to Serial for connection to Pi Zero

```
FT232 Connection

FT232                   Pi 
---- GND  -----------  GND ---- 14         13	
---- CTS                   ---- 12 (18)    11
---- VCC       /-----  RX  ---- 10 (15)    9
---- TX   ----/  /---  TX  ---- 8  (14)    7
---- RX   ------/      GND ---- 6          5
---- DTR               5v  ---- 4          3
                       5v  ---- 2          1

RX (FT232) connects to TX (Pi)
```

# C OLED library

```
# BCM library first
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz 
tar xvfz bcm2835-1.71.tar.gz
cd bcm2835-1.71                       
./configure                   
make  
sudo make install

# Then C OLED library
git clone https://github.com/gavinlyonsrepo/SSD1306_OLED_RPI
cd SSD1306_OLED_RPI
sudo make

# Make my code:
cd splash
make
# And check it works
sudo bin/splash
```


# Base install for Banana Pi M2 Zero


Download Armbian 22.11.0-trunk image
Right click and use Disk Image Write to write to USB

root
1234

```
sudo bash
Set up i2c in armbian-config hardware menu
select    i2c-0 i2c-1 i2c-2

apt update
apt upgrade 

apt install python3-dev python3-pip

For pillow:
apt install zlib1g-dev libjpeg62-turbo-dev libfreetype6-dev
pip3 install Pillow


pip3 install Adafruit-Blinka
pip3 install adafruit-circuitpython-ssd1306
apt-get install libgpiod2 python3-libgpiod gpiod
```

```
cat hello.py
```

```
import busio
import board

import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None

i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

draw.text((10, 10), "LOOPER",  font=font, fill = 255)
        
disp.image(image)
disp.show()
