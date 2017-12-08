#!/usr/bin/python 
import smbus 
import math 
import time 
from mpu6050 import MPU6050 
from PID import PID 
from motor import * 
gyro_scale = 131.0 
accel_scale = 16384.0 
RAD_TO_DEG = 57.29578 
M_PI = 3.14159265358979323846 
address = 0x68 
bus = smbus.SMBus(1) 
now = time.time() 
K = 0.98 
K1 = 1 - K 
time_diff = 0.01 
sensor = MPU6050(bus, address, "MPU6050") 
sensor.read_raw_data() 
rate_gyroX = 0.0 
rate_gyroY = 0.0 
rate_gyroZ = 0.0 
gyroAngleX = 0.0 
gyroAngleY = 0.0 
gyroAngleZ = 0.0 
raw_accX = 0.0 
raw_accY = 0.0 
raw_accZ = 0.0 
rate_accX = 0.0 
rate_accY = 0.0 
rate_accZ = 0.0 
accAngX1 = 0.0 
CFangleX1 = 0.0 
FIX = -12.89 
def dist(a, b): 
    return math.sqrt((a * a) + (b * b)) 
 
def get_y_rotation(x,y,z): 
    radians = math.atan2(x, dist(y,z)) 
    return -math.degrees(radians) 
 
def get_x_rotation(x,y,z): 
    radians = math.atan2(y, dist(x,z)) 
    return math.degrees(radians) 
 
p=PID(1.0,-0.04,0.0) 
p.setPoint(0.0) 
for i in range(0, int(300.0 / time_diff)): 
    time.sleep(time_diff - 0.005) 
    sensor.read_raw_data() 
    rate_gyroX = sensor.read_scaled_gyro_x() 
    rate_gyroY = sensor.read_scaled_gyro_y() 
    rate_gyroZ = sensor.read_scaled_gyro_z() 
    gyroAngleX += rate_gyroX * time_diff 
    gyroAngleY += rate_gyroY * time_diff 
    gyroAngleZ += rate_gyroZ * time_diff 
    raw_accX = sensor.read_raw_accel_x() 
    raw_accY = sensor.read_raw_accel_y() 
    raw_accZ = sensor.read_raw_accel_z() 
    rate_accX = sensor.read_scaled_accel_x() 
    rate_accY = sensor.read_scaled_accel_y() 
    rate_accZ = sensor.read_scaled_accel_z() 
    accAngX1 = get_x_rotation(rate_accX, rate_accY, rate_accX) 
    CFangleX1 = ( K * ( CFangleX1 + rate_gyroX * time_diff) + (1 - K) * accAngX1 ) 
 
    pid = (p.update(CFangleX1)) 
    speed = pid/10.0 
    print CFangleX1 
    print speed 
 
    if(pid > 0): 
        motor_forward(speed) 
    elif(pid < 0): 
        motor_reverse( abs(speed) ) 
    else: 
        motor_stop()