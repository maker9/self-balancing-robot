#!/usr/bin/python 
from rrb3 import * 
import time 
rr = RRB3(11, 11) 
 
def motor_forward(speed): 
    if speed > 1: 
        speed = 1 
    if speed < 0: 
        speed = 0 
    rr.set_motors(speed, 0, speed, 0) 
 
def motor_reverse(speed): 
    if speed > 1: 
        speed = 1 
    if speed < 0: 
        speed = 0 
    rr.set_motors(speed, 1, speed, 1) 
 
def motor_stop(): 
    rr.set_motors(0, 0, 0, 0)