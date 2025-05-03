# Andrew Willard
# 20250503
# Humidity Checker
# MIS310

"""
base logic is:
if the humidity is below 40%, turn on the high-intensity misting system, waits 3 minutes, checks the humidity again.
If the humidity is  40% - 50%, turn on the low-intensity misting system, waits 3 minutes, checks the humidity again.
If the humidity above 50%, waits 10 minutes, checks the humidity again.
"""

# libs
import time
import random
import webbrowser

# adds a real typing style to a string
def realistic_typing(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(0.05, 0.1))
    print()

# check yes or no
def ask_yes_no(question):
    while True:
        answer = input(question).strip().lower()
        if answer in ("yes", "y"): return True
        elif answer in ("no", "n"): return False
        elif answer == "": realistic_typing("Oh, I see what you did there. No, read the line before you just press enter this time.")
        else: realistic_typing("It's a yes or no question...")

# I couldn't resist...
def open_link_and_prompt(url):
    webbrowser.open(url)
    input(f"The link has been opened in your browser: {url}\nPress [ENTER] when you're ready to continue. ")

# Narration section 1
narration1 = [
    "ok. so here is the thing...",
    "In order to get this program to do what we want it to do,",
    "there are a few things we need to do first.",
    "first and foremost, are you ok with this fun and fancy automation thing?",
    "or perhaps you'd prefer pressing enter at every line in the boring old fashion......"
]

for msg in narration1: realistic_typing(msg); time.sleep(1)

# Ask user about automation
manual = ask_yes_no("Would you rather manually advance the messages? (yes/no): ")

narration2 = ["testing...", "1...", "2...", "3."]
for msg in narration2:
    if manual: print(msg); input("[Press ENTER to continue]")
    else: realistic_typing(msg); time.sleep(1)

# Narration section 3
narration3 = [
    "We have replaced the gardener with automation.",
    "Go buy an Adafruit HTS221 - Temperature & Humidity Sensor.",
    "https://www.adafruit.com/product/4535",
    "Alternate Link...",
    "https://learn.adafruit.com/adafruit-hts221-temperature-humidity-sensor",
    "The Documentation... ",
    "https://docs.circuitpython.org/projects/hts221/en/latest/api.html",
    "or an arduino Nano 33 BLE Sense Rev2.",
    "https://docs.arduino.cc/hardware/nano-33-ble-sense-rev2/",
    "Guess what? more datasheets... ",
    "https://docs.arduino.cc/resources/datasheets/REN_HS300x-Datasheet_DST.pdf",
    "arduino hts221 specifications... ",
    "https://docs.arduino.cc/libraries/arduino_hts221/",
    "Flash it to run CircuitPython ",
    "https://www.adafruit.com/circuitpython",
    "Then add the following code to the board:",
    '''
        
    # added for dwell time.
    import time 
    # used to interact with the micro controller and the pin outs.
    import board   # https://learn.adafruit.com/arduino-to-circuitpython/the-board-module
    import digitalio   # https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/
    # Include the library for the built-in HTS221 temperature and humidity sensor
    import adafruit_hts221   # https://www.adafruit.com/product/4535
    
    # Set up I2C and the sensor to work with our board...
    i2c = board.I2C()
    sensor = adafruit_hts221.HTS221(i2c)
    
    # Set up relays...
    mist_high = digitalio.DigitalInOut(board.D2)
    mist_high.direction = digitalio.Direction.OUTPUT
    mist_low = digitalio.DigitalInOut(board.D3)
    mist_low.direction = digitalio.Direction.OUTPUT
    
    # get two relays like this - https://www.adafruit.com/product/3191
    # connect them to a misting system... 
    # I already learned more than I planned to going into this about misting systems, zip drip, and wet bulb index...
    # I trust you to google misting system and to buy something under $50.
    
    # Flag to skip the 10-minute wait the first time
    first_run = True
    
    # program loop. goes for ever and ever.
    while True:
    humidity = sensor.relative_humidity

    if humidity < 40:
        mist_high.value = True
        time.sleep(180)
        mist_high.value = False

    elif humidity < 50:
        mist_low.value = True
        time.sleep(180)
        mist_low.value = False
    else:
        if not first_run:
            time.sleep(600)

    first_run = False ''',

    "add a floating toilet valve to your water tank to get it to refill when the water level is low,",
    "and you don't even need to pay someone to check the level of the tank.",
    "you can be fancy with a display that can put those print statements to use...",
    "https://www.adafruit.com/product/4650",
    "of course, you could just drop $300 and go get a Mist king along with the appropriate Thermometer sensor and control.",
    "https://www.amazon.com/Mist-King-MKSMS5-125-50-Generation-Applications/dp/B086V3Q5BP/142-9018408-6947652",
    "https://www.amazon.com/MistKing-Hygrostat-Thermometer-Humidity-Control/dp/B074HLXM46?ref_=ast_sto_dp"
]

# Ask user again about narration style
manual = ask_yes_no("So, are you happy with your choice? (yes/no): ")

for msg in narration3:
    if msg.strip().startswith("http"): open_link_and_prompt(msg.strip())
    else:
        if manual: print(msg); input("Press [ENTER] to continue...")
        else: realistic_typing(msg); time.sleep(1)

realistic_typing("well that was fun! let's do that again sometime.")

realistic_typing("And because I never promised I wouldn't use my powers for evil... ")
open_link_and_prompt("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
