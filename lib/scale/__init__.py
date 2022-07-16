import time
import lib.pump as pump
from lib.hx711 import HX711

referenceUnit = 403
glassWeight = 104
maxWeight = glassWeight + 30
weight = 0

hx = HX711(5,6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

def getWeight():
    weight = max(0, int(hx.get_weight(5)))

    hx.power_down()
    time.sleep(.1)
    hx.power_up()

    return weight

def init(shotRequested):

    print("\nAdd shot glass now...")

    while shotRequested:
        weight = getWeight()
        print(weight,"g")

        while weight in range(glassWeight, maxWeight):
            weight = getWeight()
            print(weight,"g")
            pump.togglePump(1)

        if maxWeight < weight:
            pump.togglePump(0)
            print('Shot poured!')
            shotRequested = False