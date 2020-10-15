import serial
from pathlib import Path
import os
import pandas as pd
import time as time_lib
from datetime import datetime, date, time, timedelta

####################################################################################################################################################
class ARDUINO(object):
    ################################################################################################################################################
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial( 
            port = port,
            baudrate = baudrate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
            )
        if self.ser.isOpen(): self.ser.close()
        self.ser.open()                    
        time_lib.sleep(2)    
        return
    ################################################################################################################################################
    def read(self, scale=5/1024):
        # Use after start_recording
        self.vind = float(self.ser.readline().decode()) * scale 
        self.date_time += timedelta(seconds=self.delay_time)
        return 
    ################################################################################################################################################
    def start_recording(self):
        self.ser.write(('start').encode())
        self.date_time = datetime.now()

        # Read until reaches the "Recording" and get delayTime
        while True:
            if self.ser.readline().decode().strip() == 'Recording': 
                self.delay_time = float(float(self.ser.readline().decode())/1000 )        # Delay time that shows sampling time (s)
                break
        return
####################################################################################################################################################
def create_folder(file_path):
    # Create folder if it does not exist
    folder_path = str( Path(file_path).parents[0] )
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    return
####################################################################################################################################################

        


####################################################################################################################################################
if __name__ == '__main__':
    
    file_name = 'record_19'
    record_time = 35

    # Initialization
    arduino_file_path = './arduino/' + file_name + '.csv'
    create_folder(arduino_file_path)


    arduinos = [ARDUINO(port) for port in ['/dev/cu.usbserial-14210', '/dev/cu.usbserial-14220'] ] 
    data_df = pd.DataFrame()

    # Show when arduino starts recording
    print('Recording is Started')
    for arduino in arduinos: arduino.start_recording()
    time = arduinos[-1].date_time
    end_time = time + timedelta(seconds=record_time)

    # Recording loop
    while (end_time - time).total_seconds()>0:
        for arduino in arduinos:
            while arduino.date_time < time: 
                arduino.read()      
                data_df = data_df.append({
                    'port': arduino.ser.port,
                    'time':arduino.date_time.time(),
                    'vind':arduino.vind}, 
                    ignore_index=True)                      
            time = arduino.date_time

    print('Recording is Finished \n Wait for Saving ...')    
    data_df.to_csv(arduino_file_path, index=False)        
    print('Done!')           
################################################################################################################################################
