# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
# import threading
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
import json
import explorerhat
import time

leftMotor = explorerhat.motor.one
rightMotor = explorerhat.motor.two


def stop():
    leftMotor.stop()
    rightMotor.stop()


def forward():
    leftMotor.forward()
    rightMotor.forward()


def backwards():
    leftMotor.backwards()
    rightMotor.backwards()


def left():
    leftMotor.forward()
    rightMotor.stop()


def right():
    leftMotor.stop()
    rightMotor.forward()


def circle_left():
    leftMotor.backwards()
    rightMotor.forward()


def circle_right():
    leftMotor.forward()
    rightMotor.backwards()

def motor(direction):
    switcher = {
        "Stop": stop,
        "Forward": forward,
        "LeftForward": left,
        "RightForward": right,
        "LeftForward": left,
        "Backward": backwards,
        "SharpLeft": circle_left,
        "SharpRight": circle_right
    }

    func = (switcher.get(direction))
    if func is not None:
        func()


async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = "HostName=glovebox-iothub.azure-devices.net;DeviceId=rpi-rover;SharedAccessKey=DKk5sr+bRHhKqdI5L8USRAmTKhN33Xg2muPdZN/N0tQ="

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    await device_client.connect()

    async def method_request_handler(method_request):

        if method_request.name == "Direction":
            payload = method_request.payload

            y = json.loads(payload)
            if y is not None:
                direction = y.get('Direction')
                if direction is not None:
                    motor(direction)

            status = 200  # set return status code
        else:

            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)
            

        
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)  # Send the response
        await device_client.send_method_response(method_response)

    
    device_client.on_method_request_received = method_request_handler   # Set the method request handler on the client

    # Define behavior for halting the application
    def stdin_listener():
        while True:
            time.sleep(10)


    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for method calls
    await user_finished

    # Finally, disconnect
    await device_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
