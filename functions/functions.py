import pyautogui
import keyboard
import time
import numpy as np
from config import *

def get_bar_percentage(region, threshold=0.45):
    """Calculate the filled percentage of a status bar based on a grayscale screenshot."""
    screenshot = pyautogui.screenshot(region=region).convert("L")  # convert to grayscale
    arr = np.array(screenshot)
    bw = arr >= int(threshold * 255)
    
    width = bw.shape[1]
    fill_width = sum(np.mean(bw[:, col]) > 0.5 for col in range(width))
    
    return (fill_width / width) * 100

def log(message):
    """Prints a log message with a timestamp."""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"{timestamp}: {message}")

def use_uh():
    """Uses an Ultimate Healing Rune if health is below HEAL_BELOW_HP."""
    health_percentage = get_bar_percentage(REGION_HEALTH, threshold=0.45)
    if health_percentage > HEAL_BELOW_HP:
        return
    
    log(f"Health: {health_percentage:.1f}% - Using one Ultimate Healing Rune...")
    pyautogui.moveTo(REGION_UH)
    pyautogui.click(REGION_UH, button='right')
    pyautogui.moveTo(REGION_PLAYER)
    pyautogui.click(REGION_PLAYER, button='left')
    time.sleep(1)

def cast_spell(spell_name):
    """Casts a spell if mana is above CAST_SPELL_ABOVE_MANA."""
    mana_percentage = get_bar_percentage(REGION_MANA, threshold=0.45)
    if mana_percentage < CAST_SPELL_ABOVE_MANA:
        return
    
    eat_food()
    spell_key = SPELLS.get(spell_name)

    log(f"Mana: {mana_percentage:.1f}% - Casting {spell_name}...")
    keyboard.press_and_release(spell_key)
    time.sleep(1)

def eat_food():
    """Eat food."""
    pyautogui.moveTo(REGION_FOOD)
    for _ in range(3):
        pyautogui.click(REGION_FOOD, button='right')

def attack_next_slime(slimes_counter):
    """Attacks the next slime if found in the battle region."""
    targeting_slime = pyautogui.locateOnScreen(TARGETING_SLIME_IMG, confidence=0.9, region=REGION_BATTLE)
    full_hp_slime = pyautogui.locateOnScreen(FULL_HP_SLIME_IMG, confidence=0.9, region=REGION_BATTLE)
    
    if full_hp_slime and not targeting_slime:
        time.sleep(2)
        pyautogui.click(REGION_SLIME_ON_BATTLE, button="left")
        time.sleep(0.5)
        eat_food()
        slimes_counter += 1
        log(f"Slimes killed: {slimes_counter}")
    
    return slimes_counter