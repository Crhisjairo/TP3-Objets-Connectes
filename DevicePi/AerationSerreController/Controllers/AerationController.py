import logging
import string
import time
from Controllers.SteppMotor import SteppMotor
from Controllers.Thermometer import Thermometer
from Controllers.Ultrasonic import Ultrasonic
from Controllers.MessageReceptor import MessageReceptor
import Data

import threading

class AerationController:

    def __init__(self, model, view, state: string):
        self.model = model
        self.view = view

        self.stepp_motor = SteppMotor()
        self.thermometer = Thermometer()
        self.ultrasonic = Ultrasonic()
        self.messageReceptor = MessageReceptor()
        
        self.set_state(state)
        self.start_sensors()

        self.view.set_user_percentage_input(Data.manual_open_door_percentage)

    def set_state(self, newState: string) -> None:
        print("Transitioning to state: " + newState)
        Data.state = newState

    def start_sensors(self):
        self.mainloop_thread = threading.Thread(target=self.mainloop, daemon=True)
        self.mainloop_thread.start()
        
        self.stepp_motor.run()
        self.thermometer.run()
        self.ultrasonic.run()
        self.messageReceptor.run()
        
    def mainloop(self):
        while True:
            self.update_view()
    

    def update_view(self):
        self.view.set_temp(Data.current_temp)
        self.view.set_distance(Data.distance)
        self.view.set_open_door_percentage(Data.open_door_percentage)
        self.view.set_motor_direction(Data.motor_direction)
        self.view.set_motor_speed(Data.motor_speed)

    def set_manual_percentage(self, percentage: float):
        Data.manual_open_door_percentage = percentage


    def log(self, message):
        """
        Save the email
        :param email:
        :return:
        """
        self.model.add_log(logging.DEBUG, message)
        pass

    def get_logs(self):
        return self.model.get_logs()
