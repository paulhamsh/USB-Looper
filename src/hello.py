
# SSD1306 IMPORTS

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/home/paul/looper/Ubuntu-Bold.ttf", 20, 0)
draw.text((10, 10), "LOOPER",  font=font, fill = 255)
        
disp.image(image)
disp.display()       
