import keyboard
import sys
import pyautogui
from config import *
from functions.functions import use_uh, cast_spell, attack_next_slime, log

def start_loop():
    global loop_status
    loop_status = True
    log("STARTED!")

def end_loop():
    global loop_status
    loop_status = False
    log("PAUSED!")
    log("PRESS PAGE UP TO RESUME")

# register keys to turn on/off the trainer
keyboard.add_hotkey('page up', start_loop)
keyboard.add_hotkey('page down', end_loop)

slimes_counter = -1
loop_status = False

log("PRESS PAGE UP TO START THE TRAINER")

while True:
    if loop_status:
        slimes_counter = attack_next_slime(slimes_counter)
        use_uh()
        cast_spell("exura")
        
        battle = pyautogui.locateOnScreen(BATTLE_NAME_IMG, confidence=0.9, region=REGION_BATTLE_NAME)
        if not battle:
            log("Battle not found...")
            log("Exiting the trainer.")
            sys.exit()