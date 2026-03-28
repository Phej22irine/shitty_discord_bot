import pydirectinput
import time
import pygetwindow as gw

# Focus on game window.
def game_window():
    window_list = gw.getAllTitles()
    for x in window_list:
        if "mGBA" in x:
            target_window = str(x)
            break
    try:
        window = gw.getWindowsWithTitle(target_window)[0]
        window.activate()
    except:
        print("window not found.")
        return False    
    time.sleep(.1)
    
    return True

# Translate discord commands to control emulators and (potentially) games.
def game_input(raw_input):
    window_active = game_window()
    translate_input = raw_input.split()
    
    try:
        translate_input[1] = int(translate_input[1])
    except IndexError: pass
    
    input = translate_input[0]
    
    while window_active:
        window_active = game_window()
        print(translate_input)
        
        match input.lower():
            case 'a'      : pydirectinput.press('x')
            case 'b'      : pydirectinput.press('z')
            case "select" : pydirectinput.press('q')
            case "start"  : pydirectinput.press('w')
            case "up"     : pydirectinput.press('up')
            case "down"   : pydirectinput.press('down')
            case "left"   : pydirectinput.press('left')
            case "right"  : pydirectinput.press('right')
            case "r"      : pydirectinput.press('a')
            case "l"      : pydirectinput.press('s')
        try:
            if translate_input[1] > 0:
                translate_input[1] -= 1
                continue
        except: pass
        return