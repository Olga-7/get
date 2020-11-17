import RPi.GPIO as GPIO
#from gpio import GPIO

import matplotlib.pyplot as plt
import numpy as np

from time import sleep
import time

import string
import math


GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

D=[26,19,13,6,5,11,9,10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

D1=[21,20,16,12,7,8,25,24]

GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)


def decToBinList(decNumber):
    binary = bin(decNumber) [2:]
    #print (binary)
    binary = binary [::-1]
    #print (binary)
    l = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range (0, len(binary)):
        l[i] = int(binary[i])
    #print (l)
    l.reverse()
    #print (l)
    return l

def lightNumber(pins, list_num):
    for n in range (0, 8):
        GPIO.output (pins[n], 0)
    for j in range (7, -1, -1):
        GPIO.output (pins[j], list_num[j])

def num2dac(pins, K):
    L = decToBinList(K)
    lightNumber(pins, L)

def adc():
    a = 0
    b = 255
    i = int((a + b) / 2)
    while True:
        num2dac(D, i)
        num2dac(D1, i)
        time.sleep (0.01)
        if b - a == 2 or i == 0:
            Volt = int((((int(i) * 3.3) / 256) * 100) / 100)
            print("Digital value: ", i , ", Analog Value: ", Volt, "V")
            return i
            break
        elif GPIO.input(4) == 1:
            a = i
            i = int((a + b) / 2)    
        elif GPIO.input(4) == 0:
            b = i
            i = int((a + b) / 2)


try:
    while adc() > 0:
        GPIO.output(17, 0) #разряжаем конденсатор
        print("000")
        time.sleep(1)
    
    t_start = time.time() #время начала эксперимента
    listT = [] #список измеренных времён
    listV = [] #список измеренных напряжений
    measure = [] #список измеренных кодов напряжений

    GPIO.output(17, 1) #заряжаем конденсатор
    while adc() < 252:
        listT.append(time.time() - t_start)
        measure.append(adc())
        listV.append((adc() * 3.3) / 256)
        time.sleep(0.01)
        print((adc() * 3.3) / 256)
        print("111")
        if adc() >= 252:
            break

    GPIO.output(17, 0) #заряжаем конденсатор
    while adc() > 0:
        listT.append(time.time() - t_start)
        measure.append(adc())
        listV.append((adc() * 3.3) / 256)
        time.sleep(0.01)
        print("000")
    
    plt.plot(measure, 'r-')
    plt.show()

    np.savetxt('data.txt', measure, fmt='%f')

    dT = 0
    for i in range (0, len(listT)-1):
        dT = dT + abs(listT[i+1] - listT[i])
    dT = dT / (len(listT) - 1)
    dV = 0
    for i in range (0, len(listV)-1):
        dV = dV + abs(listV[i+1] - listV[i])
    dV = dV / ((len(listV) - 1))
    X = [dT, dV]
    np.savetxt('settings.txt', X, fmt='%f')

    plt.plot(listT, listV, 'r-')
    plt.title ('Зависимость напряжения на обкладках конденсатора от времени')
    plt.xlabel ('Время, с')
    plt.ylabel ('Напряжение, В')
    plt.show()

finally:
    for i in range (7, -1, -1):
        GPIO.output(pins[i], 0)