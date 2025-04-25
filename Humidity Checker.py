# Andrew Willard
# 20250415
# Humidity Checker
# MIS310


"""
base logic is:
if the humidity is below 40%, turn on the high-intensity misting system, waits 3 minutes, checks the humidity again.
If the humidity is  40% - 50%, turn on the low-intensity misting system, waits 3 minutes, checks the humidity again.
If the humidity above 50%, waits 10 minutes, checks the humidity again.
"""

# we have replaced the gardener with automation.

# Go buy an Adafruit HTS221 - Temperature & Humidity Sensor - https://www.adafruit.com/product/4535
# https://learn.adafruit.com/adafruit-hts221-temperature-humidity-sensor
# https://docs.circuitpython.org/projects/hts221/en/latest/api.html

# or a Nano 33 BLE Sense Rev2 - https://docs.arduino.cc/hardware/nano-33-ble-sense-rev2/
# https://docs.arduino.cc/resources/datasheets/REN_HS300x-Datasheet_DST.pdf
# https://docs.arduino.cc/libraries/arduino_hts221/

# Flash it to run CircuitPython and add the following code to the board:
# https://www.adafruit.com/circuitpython


"""
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
# this code allows the relays connected to the pins to get power.

# get two relays like this - https://www.adafruit.com/product/3191
# connect them to a misting system... 
# I already learned more than I planned to going into this about misting systems, zip drip, and wet bulb index...
# I trust you to google misting system and to buy something under $50.

# Flag to skip the 10-minute wait the first time
first_run = True

# program loop. goes for ever and ever.
while True:
    humidity = sensor.relative_humidity
    #print("Humidity:", humidity)

    if humidity < 40:
        #print("HIGH misting") #debug
        mist_high.value = True
        time.sleep(180)
        mist_high.value = False

    elif humidity < 50:
        #print("LOW misting") #debug
        mist_low.value = True
        time.sleep(180)
        mist_low.value = False
    else:
        #print("Humidity good — waiting 10 mins") #debug
        if not first_run:
            #print("not the first rodeo") #debug
            time.sleep(600)  # Wait 10 minutes *after* first run
        # else: skip sleep on first run

    # Update flag after first loop
    first_run = False
"""

# add a floating toilet valve to your water tank to get it to refill when the water level is low,
# and you don't even need to pay someone to check the level of the tank.

# you can be fancy with a display that can put those print statements to use...
# https://www.adafruit.com/product/4650


# of course, you could just drop $300 and go get a Mist king along with the appropriate Thermometer sensor and control.
# https://www.amazon.com/Mist-King-MKSMS5-125-50-Generation-Applications/dp/B086V3Q5BP/142-9018408-6947652
# https://www.amazon.com/MistKing-Hygrostat-Thermometer-Humidity-Control/dp/B074HLXM46?ref_=ast_sto_dp


print("if you are reading this it means you just ran the code and didn't read anything that this code does.")