"""
20 April 2019

The Absolute Tinkerer
"""

# """
from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO

RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 5
RECEIVE_PIN = 11  # 16
TRANSMIT_PIN = 7  # 8

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    cumulative_time = 0
    beginning_time = datetime.now()
    print('**Started recording**')
    # GPIO.output(TRANSMIT_PIN, GPIO.LOW)
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    print('**Ended recording**')
    print('%s samples recorded' % len(RECEIVED_SIGNAL[0]))
    GPIO.cleanup()

    print('**Processing results**')
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    print('**Plotting results**')
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
# """



"""
from RxTx import RxTx
import time

if __name__ == '__main__':
    rxtx = RxTx()

    print(rxtx.sniffCode())

    rxtx.cleanup()
"""

"""
from DataRW import DataRW

if __name__ == '__main__':
    data = DataRW()

    data.addData(1, 2, 3, 4, 5, 6)
"""
