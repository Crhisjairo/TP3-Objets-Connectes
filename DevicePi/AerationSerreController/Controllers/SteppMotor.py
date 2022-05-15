import string
import threading
import RPi.GPIO as GPIO
import time
import Data

class SteppMotor:

    motorPins = (12, 16, 18, 22)  # define pins connected to four phase ABCD of stepper motor
    CCWStep = (0x01, 0x02, 0x04, 0x08)  # define power supply order for rotating anticlockwise
    CWStep = (0x08, 0x04, 0x02, 0x01)  # define power supply order for rotating clockwise
    
    state: string

    old_temp = 0
    old_user_door_distance = 0
    
    def __init__(self) -> None:
        self.setup()


    def setup(self):
        GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
        for pin in self.motorPins:
            GPIO.setup(pin, GPIO.OUT)


    # as for four phase stepping motor, four steps is a cycle. the function is used to drive the stepping motor clockwise or anticlockwise to take four steps
    def moveOnePeriod(self, direction, ms):
        for j in range(0, 4, 1):  # cycle for power supply order
            for i in range(0, 4, 1):  # assign to each pin
                if (direction == 1):  # power supply order clockwise
                    GPIO.output(self.motorPins[i], ((self.CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
                    Data.motor_direction = 'Droite'
                else:  # power supply order anticlockwise
                    GPIO.output(self.motorPins[i], ((self.CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
                    Data.motor_direction = 'Gauche'
            if (ms < 3):  # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
                ms = 3
            time.sleep(ms * 0.001)
            Data.motor_direction = 'Arrêté'

        # continuous rotation function, the parameter steps specifies the rotation cycles, every four steps is a cycle


    def moveSteps(self, direction, ms, steps):
        cycles = steps / 4
        Data.motor_speed = str(cycles) + ' tours/min'

        for i in range(steps):
            self.moveOnePeriod(direction, ms)


    # function used to stop motor
    def motorStop(self):
        for i in range(0, 4, 1):
            GPIO.output(self.motorPins[i], GPIO.LOW)


    def run(self):
        self.motor_thread = threading.Thread(target=self.loop, daemon=True)
        self.motor_thread.start()

    def loop(self):
        while True:
            if(Data.state == 'automatic'):
                self.operatesAutomatic()
            else:
                self.operatesManual()

    def operatesAutomatic(self):
        new_temp = Data.current_temp
        new_distance = Data.distance

        if(new_temp > self.old_temp and new_temp <= Data.MAX_TEMPERATURE):
            #door up
            if(Data.distance >= Data.MAX_DISTANCE):
                return

            Data.open_door_percentage = 6.67 * Data.current_temp + (-133.33)

            # door down
            self.moveSteps(0, 3, 64) # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
            #512 full clockwise
            
            self.old_temp = new_temp
            print("icitte down")
        
        elif (new_temp < self.old_temp and new_temp >= Data.MIN_TEMPERATURE):
            if(Data.distance <= Data.MIN_DISTANCE):
                return
            
            Data.open_door_percentage = 6.67 * Data.current_temp + (-133.33)

            # door up
            self.moveSteps(1, 3, 64) # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
            #512 full clockwise
            
            self.old_temp = new_temp
            print("icitte up")

    def operatesManual(self):
        user_door_distance = 0

        
        user_door_distance = Data.MAX_DISTANCE * (Data.manual_open_door_percentage / 100)

        current_distance = Data.distance

        print('user distance: ' + str(user_door_distance))
        print('current distance: ' + str(current_distance))

        if(user_door_distance > self.old_user_door_distance):
            #going down
            while(current_distance + 0.5 <= user_door_distance):
                self.moveSteps(0, 3, 64)  # rotating 360 deg anticlockwise
                current_distance = Data.distance
                user_door_distance = Data.MAX_DISTANCE * (Data.manual_open_door_percentage / 100)
                Data.open_door_percentage =  100 * (current_distance / Data.MAX_DISTANCE)
                
                print('up')
                print('user distance: ' + str(user_door_distance))
                print('current distance: ' + str(current_distance))

                if(Data.distance <= Data.MIN_DISTANCE): # max dist and min dist
                    return


            self.old_user_door_distance = current_distance
        else:
            #going up
            while(current_distance - 0.5 >= user_door_distance):
                self.moveSteps(1, 3, 64)  # rotating 360 deg clockwise
                current_distance = Data.distance
                user_door_distance = 15 * (Data.manual_open_door_percentage / 100)
                Data.open_door_percentage = Data.MAX_DISTANCE * (current_distance / 100)
                print('down')
                print('user distance: ' + str(user_door_distance))
                print('current distance: ' + str(current_distance))

                if(Data.distance >= Data.MAX_DISTANCE): # max dist and min dist
                    return


            self.old_user_door_distance = current_distance

        #if we add percentage
            

    def set_state(self, newState: string):
        self.state = newState

    def destroy(self):
        GPIO.cleanup()  # Release resource
