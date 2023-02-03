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

**Currently the rotary controller and footswitch STOP don't do anything**

# How to use the pedal

Plug in the amp into the OTG cable (before turning on)    
Turn on the pedal by plugging in USB power cable.      

<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Control3.jpg" >

The footswitches are labelled STOP, then Tracks 1 to 4. (STOP currently doesn't do anything)      

The OLED will now show the following info.   
Each track has a play and record icon. 
If the icon is filled then that is currently active. 
If both are unfilled, then the track is empty.   

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
cp USB-Looper/src/looper7.py /opt/looper/looper.py
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

