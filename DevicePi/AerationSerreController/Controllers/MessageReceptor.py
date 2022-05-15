import threading
import time
from azure.iot.device import IoTHubDeviceClient

class MessageReceptor:

    def __init__(self) -> None:
        self.CONNECTION_STRING = "HostName=Crhisjairo-IoT.azure-devices.net;DeviceId=DoorSystemPi;SharedAccessKey=/2Igw1DAKVQIMek5DfKKarJK+W316rcyLjpT8h6ahH0="
        self.RECEIVED_MESSAGES = 0
        

    def message_handler(self, message):
        self.RECEIVED_MESSAGES += 1
        print("")
        print("Message received:")

        # print data from both system and application (custom) properties
        for property in vars(message).items():
            print ("    {}".format(property))

        print("Total calls received: {}".format(self.RECEIVED_MESSAGES))

    def run(self):
        self.receptor_thread = threading.Thread(target=self.start_receving, daemon=True)
        self.receptor_thread.start()

    def start_receving(self):
        print ("Starting the Python IoT Hub C2D Messaging device sample...")

        # Instantiate the client
        client = IoTHubDeviceClient.create_from_connection_string(self.CONNECTION_STRING)

        print ("Waiting for C2D messages, press Ctrl-C to exit")
        try:
            # Attach the handler to the client
            client.on_message_received = self.message_handler

            while True:
                time.sleep(1000)
        except KeyboardInterrupt:
            print("IoT Hub C2D Messaging device sample stopped")
        except Exception as e:
            print(e)
        finally:
            # Graceful exit
            print("Shutting down IoT Hub Client")
            client.shutdown()
