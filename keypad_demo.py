import RPi.GPIO as GPIO
import time

import doorControl

GPIO.setmode(GPIO.BOARD)
def checkkeypad(length):
    MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D']]
    ROW = [7,11,13,15]
    COL = [12,16,18,22]
    result = []
    # COL set HIGH
    for j in range(4):
        GPIO.setup(COL[j],GPIO.OUT)
        GPIO.output(COL[j],1)
    # ROW set HIGH
    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    while(True):
        for j in range(4):
            # set COL LOW
            GPIO.output(COL[j],0)    
            # Check inputs
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    print(MATRIX[i][j])
                    result.append(MATRIX[i][j])
                    while(GPIO.input(ROW[i]) == 0):
                        time.sleep(0.5)
            GPIO.output(COL[j], 1)
            if len(result) >= length:
                return result
def checkpassword():
    password = [1,2,3,'A']
    length = len(password)
    print("Please enter password:")
    result = checkkeypad(length)
    if result == password:
        doorControl.door().unlock()
        print("Door Unlocked")
        time.sleep(10)
        doorControl.door().lock()
        print("Door ReLocked")
    else:
        doorControl.door().lock()
        print("Password failed")
try:
    while(True):
        checkpassword()
except KeyboardInterrupt:
    GPIO.cleanup()
