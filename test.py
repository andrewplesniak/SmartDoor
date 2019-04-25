import doorControl
import time

global door
door = doorControl.door()

if __name__ == "__main__":
    door.lock()
    time.sleep(3)
    door.unlock()
    time.sleep(3)
    door.lock()
