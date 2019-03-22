import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(5, 0)
    GPIO.output(3, 0)

def openLed():
    setup()
    GPIO.output(5, 1)
    GPIO.output(3, 0)
    time.sleep(5)
    GPIO.cleanup()

if __name__ == "__main__":
    openLed()
