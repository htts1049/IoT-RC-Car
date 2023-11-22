import asyncio
from gpiozero import DistanceSensor

forwardSensor = DistanceSensor(echo=15, trigger=14)
backwardSensor = DistanceSensor(echo=24, trigger=23)
rightSensor = DistanceSensor(echo=6, trigger=5)
leftSensor = DistanceSensor(echo=17, trigger=27)

# return distance by centimeter
async def forwardDistance():
    return forwardSensor.distance * 100

async def backwardDistance():
    return backwardSensor.distance * 100

async def leftDistance():
    return leftSensor.distance * 100

async def rightDistance():
    return rightSensor.distance * 100