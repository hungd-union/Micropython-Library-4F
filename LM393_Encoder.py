'''
    Micropython library for LM393 Optical Speed Encoder and TT Hobby Gearmotor
'''

from machine import Pin, time_pulse_us
import time

class Encoder():
    
    def __init__ (self, Digital_pin, PPR, max_window = 8):
        ''' Assign D0 Pin of encoder and encoder wheel PPR'''
        self.ppr = PPR
        self.pin = Pin(Digital_pin, Pin.IN)
    
        self.window = max_window
        self.readings = [0] * max_window
        self.moving_index = 0
    
    def get_period (self):
        ''' Get period between each pulse'''
        period = time_pulse_us(self.pin, 1, 50000)
        if period <= 0:
            return 0
        else:
            return period
    
    def get_raw_RPM (self):
        ''' Calculate raw, instantaneous RPM of motor'''
        P = self.get_period()
        if P == 0:
            return 0
        else:
            inst_RPM = 30000000/(P*self.ppr)
            if inst_RPM > 1000: return 0
            return round(inst_RPM, 4)
        
    def get_RPM (self):
        '''Calculate the average RPM of motor'''
        current_raw = self.get_raw_RPM()
        self.readings[self.moving_index] = current_raw
        
        self.moving_index += 1
        if self.moving_index >= self.window:
            self.moving_index = 0
        
        avg_RPM = sum(self.readings) / self.window
        return round (avg_RPM, 2)
        

if __name__ == "__main__":
    Left_encoder = Encoder(34, 20)
    while True:
        print (Left_encoder.get_RPM())
        time.sleep_us(100)
            
        
