
from cc2541 import CC2541

def get_data(sensor):

    name = sensor.get('name')
    mac = sensor.get('mac')

    data = []

    cc2541 = CC2541(mac)

    METRIC_STR = "%s.{0}.{0}" % name

    data.append((METRIC_STR.format(mac, "temperature"), cc2541.temperature))
    data.append((METRIC_STR.format(mac, "humidity"), cc2541.humidity))
    data.append((METRIC_STR.format(mac, "magnet"), cc2541.magnet))
    data.append((METRIC_STR.format(mac, "barometer"), cc2541.barometer))
    data.append((METRIC_STR.format(mac, "gyroscope"), cc2541.gyroscope))
    data.append((METRIC_STR.format(mac, "accelerometer"), cc2541.accelerometer))

    return data
