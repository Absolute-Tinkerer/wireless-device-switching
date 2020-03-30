"""
19 March 2020

The Absolute Tinkerer

This class is used to read and write to our schedule data file used for any
of our schedule data storage requirements
"""

import os
import json
import uuid

import keys

from datetime import datetime


class ScheduleRW:
    fileName = 'schedule.file'

    def __init__(self, scheduleType):
        """
        Constructor

        Parameters:
        -----------
        scheduleType : String
            Either keys.SCHEDULE_ABSOLUTE or keys.SCHEDULE_RELATIVE
        """
        # Create the dissimilar parameters based on the schedule type
        _params = {}
        if scheduleType == keys.SCHEDULE_ABSOLUTE:
            _params[keys.SCHEDULE_TIME] = ''   # Form of str(xx:xx)
            _params[keys.SCHEDULE_AM_PM] = ''  # 'AM' or 'PM'
        elif scheduleType == keys.SCHEDULE_RELATIVE:
            _params[keys.SCHEDULE_TIME] = -1   # Integer
            _params[keys.SCHEDULE_UNIT] = ''   # 'Minutes' or 'Hours'
            _params[keys.SCHEDULE_SIDE] = ''   # 'Before' or 'After'
            _params[keys.SCHEDULE_SUN] = ''    # 'Sunrise' or 'Sunset'
        else:
            s = 'Error: Choose the proper schedule type! Either absolute '
            s += 'or relative!'
            raise(Exception(s))


        # Create the empty data object
        self.data = {keys.SCHEDULE_ID: str(uuid.uuid4()),
                     keys.SCHEDULE_STATE: keys.STATE_ON,
                     keys.SCHEDULE_TYPE: scheduleType,
                     keys.SCHEDULE_PARAMETERS: _params,
                     keys.SCHEDULE_DAYS: [False for i in range(7)],
                     keys.SCHEDULE_DEVICES: []}

    def save(self):
        """
        This function is used to write the metadata to the schedule data file

        Parameters:
        -----------
        Returns:
        --------
        """
        # Convert the metadata dictionary object to a string
        s = json.dumps(self.data)

        # Create and write to the schedule file if it doesn't already exist
        if not os.path.exists(ScheduleRW.fileName):
            with open(ScheduleRW.fileName, 'w') as file:
                file.write(s)
        # Otherwise append to the document with a newline first
        else:
            with open(ScheduleRW.fileName, 'a') as file:
                file.write('\n' + s)

    def setParameterValue(self, parameter, value):
        """
        Function used to set the value of a parameter for this particular
        ScheduleRW instance

        Parameters:
        -----------
        parameter : string
            The key of the data you want to write
        value : object
            The value for the data[parameter]
        """
        if parameter in self.data[keys.SCHEDULE_PARAMETERS].keys():
            self.data[keys.SCHEDULE_PARAMETERS][parameter] = value
        else:
            self.data[parameter] = value

    @staticmethod
    def remove(ID):
        """
        Function used to remove a specific schedule id from the data file

        Parameters:
        -----------
        id : String
            The schedule's id (UUID)

        Returns:
        --------
        """
        try:
            f = open(ScheduleRW.fileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Now we remove the schedule file, iterate over each line,
        # push the schedule data to a ScheduleRW instance if it's
        # not the data we're removing, and save that data
        os.remove(ScheduleRW.fileName)

        for line in lines:
            # Load the line into a dictionary object
            data = json.loads(line)

            if ID != data[keys.SCHEDULE_ID]:
                # Create the ScheduleRW instance and transfer the dict
                temp = ScheduleRW(data[keys.SCHEDULE_TYPE])
                temp.data = data
                temp.save()

    @staticmethod
    def getSchedules():
        """
        Function used to retrieve the display information for used on
        the schedule webpage

        Parameters:
        -----------

        Returns:
        --------
        <value> : 2D list [String, boolean, string, list of booleans, string]
            [[id, state, devices (i.e., "Device:On, Device2:Off, ..."),
              days, time_display_text], [...], ...]
        """
        try:
            f = open(ScheduleRW.fileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return []

        rtn = []

        for line in lines:
            temp = []
            data = json.loads(line)

            devices = ''
            for i, (device, state) in enumerate(data[keys.SCHEDULE_DEVICES]):
                if i != len(data[keys.SCHEDULE_DEVICES]) - 1:
                    devices += '%s:%s, ' % (device, state)
            devices += '%s:%s' % tuple(data[keys.SCHEDULE_DEVICES][-1])

            params = data[keys.SCHEDULE_PARAMETERS]
            if data[keys.SCHEDULE_TYPE] == keys.SCHEDULE_ABSOLUTE:
                text = '%s %s' % (params[keys.SCHEDULE_TIME], params[keys.SCHEDULE_AM_PM])
            else:
                num = params[keys.SCHEDULE_TIME]
                unit = params[keys.SCHEDULE_UNIT]
                side = params[keys.SCHEDULE_SIDE]
                sun = params[keys.SCHEDULE_SUN]

                if num == 1:
                    unit = unit[:-1]  # Drop the 's'

                text = '%s %s %s %s' % (num, unit, side, sun)

            temp.append(data[keys.SCHEDULE_ID])
            temp.append(data[keys.SCHEDULE_STATE] == keys.STATE_ON)
            temp.append(devices)
            temp.append(data[keys.SCHEDULE_DAYS])
            temp.append(text)

            rtn.append(temp)

        # Now, we want to have this list sorted first by absolute time and then by
        # relative 
        absolute = []
        relative = []
        for data in rtn:
            if len(data[4].split(' ')) == 4:
                relative.append(data)
            else:
                absolute.append(data)

        absolute = sorted(absolute, key=lambda z: datetime.strptime(z[4], '%I:%M %p'))

        # I didn't sort relative because I wasn't super sure the best way to do it
        return absolute + relative

    @staticmethod
    def setState(ID, state):
        """
        Function used to set the current ON/OFF State of the schedule element
        whose ID is passed in

        Parameters:
        -----------
        ID : String
            The schedule UUID
        state : boolean
            The state of this schedule item

        Returns:
        --------
        """
        try:
            # Load the data from the save file and update
            f = open(ScheduleRW.fileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Now we remove the data file, iterate over each line, push the
        # data to a ScheduleRW instance with the state updated if
        # needed, and save that data
        os.remove(ScheduleRW.fileName)

        for line in lines:
            # Load the line into a dictionary object
            data = json.loads(line)

            # Create the ScheduleRW instance and transfer the dict
            temp = ScheduleRW(data[keys.SCHEDULE_TYPE])
            temp.data = data

            if ID == data[keys.SCHEDULE_ID]:
                temp.data[keys.SCHEDULE_STATE] = keys.STATE_ON if state else keys.STATE_OFF

            temp.save()
