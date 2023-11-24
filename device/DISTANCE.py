import asyncio
from gpiozero import DistanceSensor

forwardSensor = DistanceSensor(echo=15, trigger=14)
backwardSensor = DistanceSensor(echo=24, trigger=23)

# return distance by centimeter
async def forwardDistance():
    return forwardSensor.distance * 100

async def backwardDistance():
    return backwardSensor.distance * 100
