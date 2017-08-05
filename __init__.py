import esp
import gc
import time
import urequests
import ugfx
import wifi


def clear(color):
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()
    ugfx.clear(color)


def wait_wifi():
    clear(ugfx.BLACK)
    ugfx.string(50, 25, "STILL", "Roboto_BlackItalic24", ugfx.WHITE)
    ugfx.string(30, 50, "Connecting to wifi", "PermanentMarker22", ugfx.WHITE)
    len = ugfx.get_string_width("Connecting to wifi", "PermanentMarker22")
    ugfx.line(30, 72, 30 + 14 + len, 72, ugfx.WHITE)
    ugfx.string(140, 75, "Anyway", "Roboto_BlackItalic24", ugfx.WHITE)
    ugfx.flush()

    while not wifi.sta_if.isconnected():
        time.sleep(0.1)


def wait_sauna():
    clear(ugfx.BLACK)
    ugfx.string(50, 25, "STILL", "Roboto_BlackItalic24", ugfx.WHITE)
    ugfx.string(30, 50, "Connecting to sauna", "PermanentMarker22", ugfx.WHITE)
    len = ugfx.get_string_width("Connecting to sauna", "PermanentMarker22")
    ugfx.line(30, 72, 30 + 14 + len, 72, ugfx.WHITE)
    ugfx.string(140, 75, "Anyway", "Roboto_BlackItalic24", ugfx.WHITE)
    ugfx.flush()


def show_temp(temperature):
    clear(ugfx.BLACK)
    ugfx.string(50, 25, "Sauna Finland PRKL", "Roboto_BlackItalic24", ugfx.WHITE)
    ugfx.string(100, 50, str(temperature) + " C", "Roboto_BlackItalic24", ugfx.WHITE)

    if temperature < 50:
        ugfx.string(70, 75, "Good for Swedes", "Roboto_BlackItalic24", ugfx.WHITE)
    elif temperature > 50 and temperature < 70:
        ugfx.string(70, 75, "Heat is up!", "Roboto_BlackItalic24", ugfx.WHITE)
    else:
        ugfx.string(70, 75, "Good for Finns!", "Roboto_BlackItalic24", ugfx.WHITE)
        
    ugfx.flush()


ugfx.init()
wifi.init()
wait_wifi()

while True:
    try:
        r = urequests.get("http://www.tarlab.fi/sensors/temperature1")
    except:
        if not wifi.sta_if.isconnected():
            wifi.init()
            wait_wifi()
    else:
        if r.status_code == 200:
            gc.collect()
            try:
            	temperature = int(float(r.text))
            	r.close()
            except:
            	time.sleep(31)
            show_temp(temperature)
            time.sleep(60)
            continue
            
    wait_sauna()
    time.sleep(31)
