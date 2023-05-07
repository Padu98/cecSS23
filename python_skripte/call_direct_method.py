#!/usr/bin/env python3
 
import sys
import os
import time
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
import base64
import json
 
 
iothub_connection_str = "HostName=ampaduHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=uFfYu1bp88xArQj/GLP1QMhOlf3y+7sfwDx0dQL+zH0="
device_id = "edgeDevice/modules/cameraCapture"
method_name = "classify"
method_payload = {}
images = ['Discocytes-Test/1033.png', 'Echinocytes-Test/1018.png', 
            'Discocytes-Test/20.png', 'Discocytes-Test/1033.png', 
            'Spherocytes-Test//10.png']

dis_count = 0
ech_count = 0
sph_count = 0

for image in images:
    with open('./Portraits_png/' + image, 'rb') as file:
        image_bytes = file.read()

    base64_bytes = base64.b64encode(image_bytes)
    base64_string = base64_bytes.decode('utf-8')
 
    try:
        registry_manager = IoTHubRegistryManager(iothub_connection_str)
        deviceMethod = CloudToDeviceMethod(method_name=method_name, payload=base64_string)
        response = registry_manager.invoke_device_method(device_id, deviceMethod)
        result = json.loads(response.payload['result'])
        predictions = result['predictions']
        print(str(predictions[0]['tagName']) + ': ' +str(predictions[0]['probability']) + ' | ' +
            str(predictions[1]['tagName']) + ': ' +str(predictions[1]['probability']) + ' | ' +
            str(predictions[2]['tagName']) + ': ' +str(predictions[1]['probability']))

        if predictions[0]['probability'] > 0.9:
            dis_count+=1
        elif predictions[1]['probability'] > 0.9:
            ech_count+=1
        else:
            sph_count+=1
    
    except Exception as ex:
        print("Unexpected error {0}".format(ex))
    except KeyboardInterrupt:
        print("iothub_registry_manager_sample stopped")

print('Diskozytes: ' + str(dis_count) + ' Echinozytes: ' + str(ech_count) + ' Sperocytes: ' + str(sph_count))

