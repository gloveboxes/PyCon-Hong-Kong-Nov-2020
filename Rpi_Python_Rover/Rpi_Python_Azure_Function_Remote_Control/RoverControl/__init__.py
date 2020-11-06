import logging

import azure.functions as func
from azure.iot.hub import DigitalTwinClient
import json

iothub_connection_str = os.getenv("IOTHUB_CONNECTION_STRING")
device_id = os.getenv("IOTHUB_DEVICE_ID")
command_name = os.getenv("IOTHUB_COMMAND_NAME")

connect_timeout_in_seconds = 3
response_timeout_in_seconds = 7  # Must be within 5-300


def main(req: func.HttpRequest) -> func.HttpResponse:
    cmd = req.params.get('cmd')
    if not cmd:
        return func.HttpResponse("This HTTP triggered function executed successfully. Pass a command in the query string.", status_code=200)

    if cmd:

        digital_twin_client = DigitalTwinClient(iothub_connection_str)

        telemetry = {
            "Direction": cmd,
        }

        json_object = json.dumps(telemetry)

        invoke_command_result = digital_twin_client.invoke_command(
            device_id, command_name, json_object, connect_timeout_in_seconds, response_timeout_in_seconds)

        return func.HttpResponse(f"Hello, {cmd}. This HTTP triggered function executed successfully.")
