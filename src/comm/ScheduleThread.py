"""
26 March 2020

The Absolute Tinkerer

This class is used to handle all of the device scheduling necessary
by using threading.

Starting the scheduling threading is as simple as instantiating this
class and calling the ScheduleThread.run() function. To terminate the
scheduling, call ScheduleThread.terminate() and the thread will complete.
"""

from threading import Thread
import time
from datetime import datetime

from ScheduleRW import ScheduleRW
from DataRW import DataRW
import keys
from suncalculator import SunCalculator

class ScheduleThread:
    def __init__(self, rxtx, scanInterval=180):
        """
        Constructor

        Parameters:
        -----------
        rxtx : RxTx
            The instance of the RxTx library so we don't have conflicting
            instances
        scanInterval : int
            The number of seconds between each schedule scan. Must be
            over 15 seconds to avoid excessive reads; default is 3 minutes
        """
        # Test the scanInterval for breaking rules
        if scanInterval < 15:
            s = 'The schedule scan interval must be 15 seconds or more!'
            raise Exception(s)

        # The class variables
        self._lastScan = time.time()
        self._scanInterval = scanInterval
        self._continue = True
        self._sunCalc = SunCalculator()
        self._rxtx = rxtx

        self._queue = self._scanSchedule()

        self._thread = Thread(target=self._run)

        # The _queue is a 2D list that's only populated when the
        # schedule scan shows an impending event (event before the
        # next scan occurs). The list populates as follows:
        # [[time,  [[device1, state], ]], ]
        # [[float, [[string,  bool ], ]], ]

    def run(self):
        """
        The public function used to start the scheduler thread
        """
        self._thread.start()
        print('*** Scheduler Thread Started ***')

    def terminate(self):
        """
        """
        self._continue = False

    def _run(self):
        """
        The private function that actually handles the scheduling; this
        is a threaded function

        Parameters:
        -----------
        Returns:
        --------
        """
        while self._continue:
            if len(self._queue) > 0:
                for i, (_time, devices) in enumerate(self._queue):
                    if time.time() > _time:
                        # Now trigger the devices
                        for device, state in devices:
                            if state:  # Turning on
                                c1, c2, c3, c4, c5, c6 = DataRW.getOnParameters(device)
                                self._rxtx.txCode(c1, c2, c3, c4, c5, c6)

                                DataRW.setState(device, keys.STATE_ON)
                            else:      # Turning off
                                c1, c2, c3, c4, c5, c6 = DataRW.getOffParameters(device)
                                self._rxtx.txCode(c1, c2, c3, c4, c5, c6)

                                DataRW.setState(device, keys.STATE_OFF)

                        # Now remove this from the queue and break from
                        # the for loop to prevent errors
                        del self._queue[i]
            else:
                # Sleep for 15 seconds so we're not overloading the pi
                # WARNING: If you don't do this, the pi will have a tough
                #          time trying to turn on/off devices on user input
                #          because it spends too much energy testing this
                #          conditional; This is where the 15 second minimum
                #          scan interval originates from
                time.sleep(15)

            # Handle the schedule scan
            if (time.time() - self._lastScan) > self._scanInterval:
                self._lastScan = time.time()
                self._queue = self._scanSchedule()

        print('*** Scheduler Thread Terminated ***')

    def _scanSchedule(self):
        """
        This private function is used to scan the schedule file using
        the ScheduleRW class. It will load the trigger queue with any
        impending schedule events

        Parameters:
        -----------

        Returns:
        --------
        <value> : 2D list
            This is the trigger queue, which is populated when the
            schedule scan shows an impending event (event before the
            next scan occurs). The list is populated as follows:
            [[time,  [[device1, state], ]], ]
            [[float, [[string,  bool ], ]], ]
        """
        rtn = []
        schedules = ScheduleRW.getSchedules()

        for schedule in schedules:
            # Compute the scheduled time from the relative or absolute
            # time string
            if len(schedule[4].split(' ')) == 4:  # This is relative time
                num, unit, side, sun = schedule[4].split(' ')
                num = int(num)

                if sun == 'Sunset':
                    schedTime = self._sunCalc.sunsetTime()
                else:
                    schedTime = self._sunCalc.sunriseTime()

                modTime = 60*num if 'Minute' in unit else 60*60*num
                modTime *= -1 if side == 'Before' else 1

                schedTime += modTime
            else:  # This is absolute time
                today = datetime.now()
                day, month, year = today.day, today.month, today.year
                toDT = schedule[4] + ' %s %s %s' % (month, day, year)
                schedTime = datetime.strptime(toDT, '%I:%M %p %m %d %Y').timestamp()

            if self._lastScan <= schedTime < self._lastScan + self._scanInterval:
                # We get the devices and states to add to the queue only
                # if this schedule element is enabled and today's day of week
                # is enabled; our indexing begins from Sunday, and weekday()
                # begins from Monday
                if schedule[1] and schedule[3][(datetime.now().weekday() + 1) % 7]:
                    # This is the list that will get appended to the
                    # return list
                    temp = [schedTime]

                    devices = []
                    for item in schedule[2].split(', '):
                        device, state = item.split(':')
                        state = state.lower() == 'on'
                        devices.append([device, state])
                    temp.append(devices)

                    rtn.append(temp)

        return rtn
