# pip install sounddevice soundfile numpy keyboard
# pip3 install sounddevice soundfile numpy keyboard


# sudo python -m pip install --upgrade pip setuptools wheel
# sudo pip install Adafruit-SSD1306

# sudo python -m pip install --upgrade pip setuptools wheel
# git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
# cd Adafruit_Python_SSD1306
# sudo python setup.py install

# SSD1306 IMPORTS

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None

# SOUND IMPORTS

import numpy as np
import sounddevice as sd
import soundfile as sf

# GPIO IMPORTS

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# General imports

from time import time, sleep

# Classes

class Button:
    
    NO_PRESS = 1
    SHORT_PRESS = 2
    LONG_PRESS = 3
    
    def __init__(self, pin):
        self.gpio = pin
        self.debounce_duration = 0.03
        self.long_hold_duration = 0.75

        self.in_press = False
        self.press_time = 0
        self.release_time = 0
        self.last_update = 0
        self.status = Button.NO_PRESS
        
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    def update(self):
        time_now = time()
        if time_now - self.last_update > 0.01:
            self.last_update = time_now
            if self.in_press == False and GPIO.input(self.gpio) == 0:
                if time_now - self.release_time > self.debounce_duration:
                    self.in_press = True
                    self.press_time = time_now
                    
            if self.in_press == True and GPIO.input(self.gpio) == 1:
                pressed_duration = time_now - self.press_time
                if pressed_duration > self.long_hold_duration:
                    self.in_press = False
                    self.release_time = time_now
                    self.status = Button.LONG_PRESS
                elif pressed_duration > self.debounce_duration:
                    self.in_press = False
                    self.release_time = time_now
                    self.status = Button.SHORT_PRESS
                
    def clear(self):
        self.status = Button.NO_PRESS
        

class Display:

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.x = [0, 44, 64, 84, 104]
        self.y = [0, 10, 28, 42, 56]
        
        self.bar_size = 6
        self.im_size = 10
        self.half_im_size = self.im_size / 2

    def show(self):
        self.disp.image(self.image)
        self.disp.display()       

    def draw_background(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
    def draw_icons(self, num, is_play, is_rec):
        self.draw.ellipse((self.x[num], self.y[3] , 
                           self.x[num] + self.im_size,
                           self.y[3] + self.im_size), 
                           outline=255, 
                           fill = 255 if is_rec else 0)
        self.draw.polygon([(self.x[num], self.y[2]), 
                           (self.x[num], self.y[2] + self.im_size), 
                           (self.x[num] + self.im_size, self.y[2] + self.half_im_size)], 
                           outline = 255, 
                           fill = 255 if is_play else 0)

    def draw_box(self, is_stop):
        self.draw.rectangle((self.x[0], self.y[3], 
                             self.x[0] + self.im_size, self.y[3] + self.im_size), 
                             outline = 255, fill = 255 if is_stop else 0)

    def draw_bar(self, amount):
        fill_width = int(self.width * amount / 100)
        self.draw.rectangle((0, self.y[4], fill_width, 
                             self.y[4] + self.bar_size), 
                             outline = 255, fill = 255)
        self.draw.rectangle((fill_width, self.y[4], 
                             self.width - 1, self.y[4] + self.bar_size), 
                             outline = 255, fill = 0)
      
    def draw_device(self, dev):
        self.font = ImageFont.truetype("/home/paul/looper/Ubuntu-Bold.ttf", 10, 0)
        self.draw.text((self.x[1], self.y[0]), dev,  font=self.font, fill = 255)

    def draw_numbers(self):
        self.font = ImageFont.truetype("/home/paul/looper/Ubuntu-Bold.ttf", 16, 0)
        for num in range(1, 5):
            self.draw.text((self.x[num], self.y[1]), str(num),  
                            font=self.font, fill = 255)

    def draw_bignum(self, num):
        self.font = ImageFont.truetype("/home/paul/looper/Ubuntu-Bold.ttf", 32, 0)
        self.draw.rectangle((self.x[0], self.y[0] - 1, self.x[1] - 1, 
                             self.y[1] - 1), outline = 0, fill = 0)
        self.draw.text((self.x[0], self.y[0]), str(num),  
                        font=self.font, fill = 255)

screen = Display()
screen.draw_background()
for num in range(1,5):
    screen.draw_icons(num, False, False)
screen.draw_numbers()
screen.draw_box(False)
screen.draw_bar(0)
screen.draw_bignum(1)
screen.show()

# Initialise buttons
stop_button = Button(5)
buttons = [Button(6), Button(13), Button(19), Button(26)]

# Initialise sound
devs = sd.query_devices()
while not devs:
    print("NO SOUND DEVICE FOUND")
    screen.draw_device("NO DEVICE")
    screen.show()
    sleep(1)
    devs = sd.query_devices()

print(devs)

dev = sd.query_devices(device = 0)
name = dev['name']
name_split = name.split(":")
short_name = name_split[0]
samplerate = int(dev['default_samplerate'])
max_in_channels = dev['max_input_channels']
max_out_channels = dev['max_output_channels']
print(short_name, samplerate, max_in_channels, max_out_channels)

screen.draw_device(short_name)
screen.show()
blocksize = 1000
duration = 80
in_channels = max_in_channels 
out_channels = max_out_channels
dtype = 'float32'

max_frames = int(duration * samplerate / blocksize) + 1
data_size = max_frames * blocksize

recs = np.zeros((4, data_size, in_channels), dtype)

do_rec = [False, False, False, False]

high_frames = 0
frame = 0


def callback_pr(indata, outdata, frames, time, status):
    global recs, do_rec, frame, max_frame
    if status:
        print(status)
     
    start = frame * blocksize
    end = start + blocksize
    slice = recs[:, start : end, :]
    outdata[:] = slice.sum(axis = 0)
    #outdata[:] = recs[0][start : end] + recs[1][start : end] + recs[2][start : end] + recs[3][start : end]

    for i in range(0,4):
        if do_rec[i]:
            recs[i][start : end] = indata[:blocksize]

    frame += 1
    # If we reach end of the buffer
    if frame >= max_frames:
        frame = 0
   

last_disp = time()
  
with sd.Stream(channels=in_channels, samplerate = samplerate, blocksize = blocksize, callback=callback_pr):
    while True:
        # If we reach end of the loop    
        if high_frames > 0 and frame > high_frames:
            frame = 0
            print("Loop")
           
        if time() - last_disp > 0.5:
            last_disp = time()
            if high_frames > 0:
                perc = int(100 * frame / high_frames)
            else:
                perc = int(100 * frame / max_frames)
            screen.draw_bar(perc) 
            screen.show()

        for i in range(0, 4):
            buttons[i].update()    
        
            b_status = buttons[i].status        
            if b_status != Button.NO_PRESS:
                buttons[i].clear()
                if b_status == Button.LONG_PRESS:
                    print ("Clear recording " + str(i+1))
                    recs[i].fill(0)
                    if i == 0:
                        high_frames = 0
                    do_rec[i] = False
                    screen.draw_icons(i+1, False, False)
                    screen.show()
                elif b_status == Button.SHORT_PRESS:
                    if do_rec[i]:
                        print("Stop recording " + str(i+1))
                        do_rec[i] = False
                        if i == 0: # only change for track 1
                            high_frames = frame
                            frame = 0
                            print(high_frames)
                        screen.draw_icons(i+1, True, False)
                        screen.show()
                        # SAVE THE FILE NOW?????
                    else:
                        print("Start recording " + str(i+1))
                        do_rec[i] = True
                        if i == 0: # only change for track 1
                            high_frames = 0
                            frame = 0    
                        screen.draw_icons(i+1, False, True)
                        screen.show()
            
