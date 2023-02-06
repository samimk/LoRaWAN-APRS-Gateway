#!/usr/bin/python3
# 
# Copyright 2023 Samim Konjicija E74KS
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import paho.mqtt.client as mqtt
import json
import sys
import aprs

# Log File
# Path to log file, default lorawanaprsgateway.log in current folder 
logfile="lorawanaprsgateway.log"

# MQTT connection parameters
broker='eu1.cloud.thethings.network' # For TTN
mqtt_port = 1883
mqtt_clientid = 'mqtt_client_id' 
mqtt_user = 'MQTT_USER_TTN'                                   # app@tenant
mqtt_pw = 'MQTT_PASSWORD_TTN'      # NNSXS.??? - generated API key

# MQTT topic for acquisition of location data
# Message should contain latitude, longitude and altitude
topic="v3/APP_NAME@TENANT/devices/DEVICE_NAME/location/solved"    # Topic format for TTN v.3

# APRS-IS connection parameters
serverHost = 'euro.aprs2.net'
serverPort = 14580
aprsUser = 'CALLSIGN'          # Callsign used for login to APRS-IS
aprsPass = 'PASSWORD'          # Password generated from callsign

# APRS sender callsign
callsign = 'SENDER_CALLSIGN'

# APRS object
objcallsign = 'OBJ_CALLSIGN'     # Callsign of tracked object (9 characters long, padded with spaces)
table = '/'                   # Symbol table used
symbol = 'j'                  # Symbol of tracked object

# Custom text sent in APRS packet
message = ''

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server")
    client.subscribe(topic)
    print('Subscribed to %s'%topic)

def on_disconnect(client, userdata, flags, rc):
    print("Client disconnected from MQTT server")

def on_message(client, userdata, msg):
    try:
        m = json.loads(msg.payload)
        lat = m["location_solved"]["location"]["latitude"]
        lon = m["location_solved"]["location"]["longitude"]
        alt = m["location_solved"]["location"]["altitude"]
        if lat>=0:
            latside='N'
        else:
            latside='S'
            lat=abs(lat)
        if lon>=0:
            lonside='E'
        else:
            lonside='W'
            lon=abs(lon)
        log_file = open(logfile, "a")
        timestamp=time.localtime()    
        aprslat=str(int(lat))+'%.2f' % round(60*(lat-int(lat)),2)
        aprslon='0'+str(int(lon))+'%.2f' % round(60*(lon-int(lon)),2)       
        packet = callsign+">APRS,TCPIP*,qAC,WIDE1-1:;"+objcallsign+"*111111z"+aprslat+latside+table+aprslon+lonside+symbol+"ALT="+str(round(alt,2))+'m asl'+message
        a = aprs.TCP(aprsUser,aprsPass)
        a.start()
        frame = aprs.parse_frame(packet)
        a.send(frame)
        log_file.write(str(timestamp[0])+"-"+str(timestamp[1])+"-"+str(timestamp[2])+" "+str(timestamp[3])+":"+str(timestamp[4])+":"+str(timestamp[5])+"  "+packet)
        time.sleep(1)
        log_file.close()
        print(packet)
    except Exception as e:
        print(e)

# Connecting MQTT broker
client = mqtt.Client(client_id=mqtt_clientid)
client.username_pw_set(mqtt_user, mqtt_pw)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

while True:
    try:
        client.connect(broker,mqtt_port,60)
        client.loop_forever()
    except:
        print("Failed to connect to MQTT server")
        print("Retrying in 60 seconds ...")
        time.sleep(60)
