import requests
import random
import time


class Telemetry():

    def get_cpu_temperature(self):
        temp = 0.0
        with open('/sys/class/thermal/thermal_zone0/temp') as temperaturefile:
            try:
                temp = float(temperaturefile.read()) / 1000
            except:
                print('Problem reading CPU Temperature')
        return temp

    def measure(self):
        

        # while retry < 2:
        #     try:
        #         response = requests.get('http://localhost:8080/telemetry')
        #         telemetry = response.json()
        #         break
        #     except:
        #         retry += 1

        # else:
        # print('Error connecting to telemetry services')
        telemetry = {
            "temperature": random.randrange(20, 25),
            "humidity": random.randrange(50, 90),
            "pressure": random.randrange(905, 1300),
            "timestamp": int(time.time()),
            "cputemperature": self.get_cpu_temperature(),
        }

        return telemetry.get('temperature'), telemetry.get('pressure'), telemetry.get('humidity'), telemetry.get('timestamp'), telemetry.get('cputemperature')
