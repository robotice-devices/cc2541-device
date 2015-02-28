
from .cc2541 import CC2541

METRIC_STR = "cc2541.{0}"


def get_data(sensor):

    results = []

    sensor = CC2541(sensor["address"])

    results.append((METRIC_STR.format("temperature"), sensor.temperature))
    results.append((METRIC_STR.format("humidity"), sensor.humidity))
    results.append((METRIC_STR.format("magnet"), sensor.magnet))
    results.append((METRIC_STR.format("barometer"), sensor.barometer))
    results.append((METRIC_STR.format("gyroscope"), sensor.gyroscope))
    results.append((METRIC_STR.format("accelerometer"), sensor.accelerometer))

    return results
