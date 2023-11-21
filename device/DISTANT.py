from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=15, trigger=14)

# return distance by centimeter
def getDistance():
    return sensor.distance * 100
