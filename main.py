#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import AnalogSensor, UARTDevice
import utime
import serial

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()
button = TouchSensor(Port.S1)
filename = "down5"
f = open(filename + ".txt", "w")
s=serial.Serial("/dev/ttyACM0",9600)
f.write("xaccel, yaccel, zaccel, xgyro, ygyro, zgyro\n")

while True:
     justpressed = False
     lastMotion = []
     
     while button.pressed():
          wait(5)
          data=s.read(s.inWaiting()).decode("utf-8")
          print('size = %d, buffer = %d' % (len(data),s.inWaiting()))
          #wait(1)
          data = data.splitlines()
          imu = data[-2].split(',')
          #f.write(d.join(imu) + '\n')
          #print(imu)
          lastMotion.append(imu)
          justpressed = True

     if justpressed == True:
          leng = len(lastMotion)
          d = ', '
          if leng % 3 != 0:
               blockSize = int(leng/3)+1
          else:
               blockSize = int(leng/3)
          print(blockSize)
          for i in range(2):
               sumFun = [0, 0, 0, 0, 0, 0]

               for j in range(blockSize):
                    for k in range(6):
                         print("i: ", i, "j: ", j, "k: ", k)
                         sumFun[k] += float(lastMotion[blockSize*i+j][k])
               for k in range(6):
                    sumFun[k] = str(sumFun[k] / 3)
               f.write(d.join(sumFun) + "\n") # add average to file
          
          for j in range(leng % blockSize):
               sumFun = [0, 0, 0, 0, 0, 0]
               for k in range(6):
                    print("k is: ", k, "j is: ", j)
                    sumFun[k] += float(lastMotion[blockSize*2+j ][k])
               for k in range(6):
                    sumFun[k] = str(sumFun[k] / 3)
               f.write(d.join(sumFun) + "\n") # add average to file


          f.write("---\n")
          justpressed = False

     

     