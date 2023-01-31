# USB-Looper
A guitar looper pedal which uses a USB audio connection to an amplifier.

The amp must send processed guitar to the looper pedal over USB and receive audio back from the looper pedal over USB.   

Examples of amps that can do this are:   
- Spark Mini
- Boss Katana

(The Spark 40 amp has a strange pitch-shift issue with USB which makes it unusable for UBS audio)   

The benefit is that you can record the processed audio, and when recording the next loop / overdub, you can use different effects.  Using a normal looper with a practice amp such as these means that the loops play back into the current amp effect setting.  

This is a diagram showing the setup - guitar into the amp, amp USB into the looper.   
The amp must be capable of USB out and USB in simultaneously.   

The pedal is based on a Raspberry Pi Zero.   This is because USB host audio is required, and I can't find a microcontroller (ESP32 / Pi 2040 / Arduino / Teensy) that has USB host audio. The TinyUSB library doesn't support it yet. But the Pi, being a Linux machine, has full USB Host capability.  The only downside is slow boot times which can be partially fixed by not running via systemd - see the boot time improvement section later.   

# Pictures

![bonnet wiring](https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Setup.jpg)

        
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Top.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Edge.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside%20Pi.jpg" width="800" >
<img src="https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Inside%20OLED.jpg" width="800" >

The wiring schematic.   

![bonnet wiring](https://github.com/paulhamsh/USB-Looper/blob/main/pictures/Proto%20Bonnet.jpg)

# Installation



# Boot time reduction



