from gpiozero import Button

no_press = 1
short_press = 2
long_press = 3
    
Button.was_held = False
Button.state = no_press
Button.name = ""

def button_pressed(btn):
    btn.was_held = False
    
def button_released(btn):
    if btn.was_held:
        btn.state = long_press
    else:
        btn.state = short_press
    
def button_held(btn):
    btn.was_held = True
    

but1 = Button(23, hold_time = 0.5, bounce_time = 0.01)
but1.name = "1"
but1.when_pressed = button_pressed
but1.when_released = button_released
but1.when_held = button_held

but2 = Button(24, hold_time = 0.5, bounce_time = 0.01)
but2.name = "2"
but2.when_pressed = button_pressed
but2.when_released = button_released
but2.when_held = button_held

but3 = Button(25, hold_time = 0.5, bounce_time = 0.01)
but3.name = "3"
but3.when_pressed = button_pressed
but3.when_released = button_released
but3.when_held = button_held

but4 = Button(12, hold_time = 0.5, bounce_time = 0.01)
but4.name = "4"
but4.when_pressed = button_pressed
but4.when_released = button_released
but4.when_held = button_held


but0 = Button(13, hold_time = 0.5, bounce_time = 0.01)
but0.name = "S"
but0.when_pressed = button_pressed
but0.when_released = button_released
but0.when_held = button_held


butx = Button(4, hold_time = 0.5, bounce_time = 0.01)
butx.name = "X"
butx.when_pressed = button_pressed
butx.when_released = button_released
butx.when_held = button_held

while True:
    if but1.state == long_press:
        print(but1.name, "long press")
        but1.state = no_press
    elif but1.state == short_press:
        print(but1.name, "short press")
        but1.state = no_press
            
    if but2.state == long_press:
        print(but2.name, "long press")
        but2.state = no_press
    elif but2.state == short_press:
        but2.state = no_press
        print(but2.name, "short press")        


    if but3.state == long_press:
        print(but3.name, "long press")
        but3.state = no_press
    elif but3.state == short_press:
        print(but3.name, "short press")
        but3.state = no_press
    
    if but4.state == long_press:
        print(but4.name, "long press")
        but4.state = no_press
    elif but4.state == short_press:
        print(but4.name, "short press")
        but4.state = no_press


    if but0.state == long_press:
        print(but0.name, "long press")
        but0.state = no_press
    elif but0.state == short_press:
        print(but0.name, "short press")
        but0.state = no_press

    if butx.state == long_press:
        print(butx.name, "long press")
        butx.state = no_press
    elif butx.state == short_press:
        print(butx.name, "short press")
        butx.state = no_press
