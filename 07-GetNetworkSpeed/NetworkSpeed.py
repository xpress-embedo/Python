#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  NetworkSpeed.py
#  
#  Copyright 2025  <xpress_embedo@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# For Environment Variable Thing, check the following link
# https://www.raspberrypi.com/documentation/computers/os.html
# Use the following command to create a virtual environment in a hidden folder in the current user’s home directory:
# python -m venv ~/.env
# Run the following command from any directory to start using the virtual environment:
# source ~/.env/bin/activate
# You should then see a prompt similar to the following:
# (.env) $
# To leave the virtual environment, run the following command from any directory:
# (.env) $ deactivate
# 
#

import time
import speedtest
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# In normal scenario's this information shouldn't be added to the git commit, but I am adding
token = "Be13Srx_erjZ4qMxJG9et7_gSJrYMm9wB7a012RZEusyR_uJTL_P83zfSFeRFppFwPRASrcF3wjp3xcyqMiBCg=="
org = "Embedded Laboratory"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "ESP32"			# Bucket Name is ESP32, because my Grafan is configured to read from the database which has name ESP32

client = InfluxDBClient(url=url, token=token, org=org)
writeAPI = client.write_api(write_options=SYNCHRONOUS)

st = speedtest.Speedtest(secure=True)

def main(args):
    
    while True:
        print ("Getting Download Speed....")
        downloadSpeed = st.download()
        downloadSpeed = downloadSpeed/1024		# in Killo Bits
        downloadSpeed = downloadSpeed/1024		# in Mega Bits
        print ("Getting Upload Speed.....")
        # uploadSpeed = 0
        uploadSpeed = st.upload()
        uploadSpeed = uploadSpeed/1024
        uploadSpeed = uploadSpeed/1024
        print (f"Download Speed = {downloadSpeed}, Upload Speed = {uploadSpeed}")
        writeAPI.write(bucket, org, [f"NetworkSpeed,device_id=1 download={downloadSpeed},upload={uploadSpeed}"])
        time.sleep(30)
        

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
