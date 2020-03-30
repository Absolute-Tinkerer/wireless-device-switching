"""
08 June 2019

The Absolute Tinkerer

This class is used to read and write to our data file used for any
of our data storage requirements

"""

import os
import json

import keys


class DataRW:
    # The file name
    datafileName = 'data.file'

    def __init__(self, title):
        """
        Constructor

        Parameters:
        -----------
        datafileName : String
            The name of the file where the metadata is stored
        """

        # Create the empty data object
        self.data = {keys.DEVICE_TITLE: title,
                     keys.DEVICE_STATE: '',

                     keys.ON_ONE_TIME_HIGH: '',
                     keys.ON_ONE_TIME_LOW: '',
                     keys.ON_ZERO_TIME_HIGH: '',
                     keys.ON_ZERO_TIME_LOW: '',
                     keys.ON_INTERVAL: '',

                     keys.OFF_ONE_TIME_HIGH: '',
                     keys.OFF_ONE_TIME_LOW: '',
                     keys.OFF_ZERO_TIME_HIGH: '',
                     keys.OFF_ZERO_TIME_LOW: '',
                     keys.OFF_INTERVAL: ''}

    @staticmethod
    def updateTitles(newTitles):
        """
        Static function used to change the titles from the existing set in the data
        file. Titles passed in shall be in the same order in which they're
        stored in the data file.

        Parameters:
        -----------
        newTitles : list of Strings
            The outlet titles

        Returns:
        --------
        """
        # Start by calling the getTitles function to get the current title order
        # These titles are in the same order as newTitles
        oldTitles = DataRW.getTitles()

        try:
            # Load the data from the save file and update
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Now we remove the data file, iterate over each line,
        # push the data to a DataRW instance, and save that data
        os.remove('data.file')

        for line in lines:
            # Load the line into a dictionary object
            data = json.loads(line)
            # Create the DataRW instance and transfer the dict
            temp = DataRW(data[keys.DEVICE_TITLE])
            temp.data = data

            # Get the index of this data's title from oldTitles and push the new title
            idx = oldTitles.index(temp.data[keys.DEVICE_TITLE])
            temp.data[keys.DEVICE_TITLE] = newTitles[idx]

            # Finally save the new data
            temp.save()

    @staticmethod
    def remove(title):
        """
        Function used to remove a specific code from the data file

        Parameters:
        -----------
        title : String
            The outlet title

        Returns:
        --------
        """
        try:
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Now we remove the data file, iterate over each line,
        # push the data to a DataRW instance if it's not the data
        # we're removing, and save that data
        os.remove('data.file')

        for line in lines:
            # Load the line into a dictionary object
            data = json.loads(line)

            if title != data[keys.DEVICE_TITLE]:
                # Create the DataRW instance and transfer the dict
                temp = DataRW(data[keys.DEVICE_TITLE])
                temp.data = data
                temp.save()

    @staticmethod
    def getTitles():
        """
        Function used to retrieve the list of titles, sorted
        alphabetically. There is only one line per title in
        the data file, so no need to test if it's already in
        the new list.

        Parameters:
        -----------

        Returns:
        --------
        <value> : 1D list
            Alphabetically sorted list of titles
        """
        try:
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return []

        titles = []

        for line in lines:
            data = json.loads(line)
            titles.append(data[keys.DEVICE_TITLE])

        titles.sort()

        return titles

    @staticmethod
    def isTitleValid(title):
        """
        Function used to identify whether a given title and type
        combination is already stored in our data file

        Parameters:
        -----------
        title : String
            The outlet title

        Returns:
        --------
        <value> : Boolean
            True if the title is valid (doesn't already exist)
            False if the title is not valid
        """
        try:
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return True

        for line in lines:
            data = json.loads(line)

            if data[keys.DEVICE_TITLE] == title:
                return False

        return True

    @staticmethod
    def getState(title):
        """
        Function used to get the current ON/OFF state of the
        device title passed in

        Parameters:
        -----------
        title : String
            The device title we're getting the state of

        Returns:
        --------
        <value> : String
            The ON/OFF state
        """
        try:
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        for line in lines:
            data = json.loads(line)

            if data[keys.DEVICE_TITLE] == title:
                return data[keys.DEVICE_STATE]

        s = 'Could not locate the device "' + title + '"'
        raise(Exception(s))

    @staticmethod
    def setState(title, state):
        """
        """
        try:
            # Load the data from the save file and update
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Now we remove the data file, iterate over each line,
        # push the data to a DataRW instance with the state updated
        # if needed, and save that data
        os.remove('data.file')

        for line in lines:
            # Load the line into a dictionary object
            data = json.loads(line)

            # Create the DataRW instance and transfer the dict
            temp = DataRW(data[keys.DEVICE_TITLE])
            temp.data = data

            if title == data[keys.DEVICE_TITLE]:
                temp.data[keys.DEVICE_STATE] = state

            temp.save()

    @staticmethod
    def getOnParameters(title):
        """
        Function used to get the list of parameters associated
        with the particular title for the ON code

        Parameters:
        -----------
        title : String
            The string corresponding to the data's OUTLET_TITLE

        Returns:
        --------
        <data> : tuple
            The ON_CODE, ON_ONE_TIME_HIGH, ON_ONE_TIME_LOW, ON_ZERO_TIME_HIGH,
            ON_ZERO_TIME_LOW, ON_INTERVAL corresponding to the particular
            title
        """
        try:
            # Load the data from the save file and update
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        output = None

        for line in lines:
            data = json.loads(line)

            if data[keys.DEVICE_TITLE] == title:
                output = (data[keys.ON_CODE],
                          data[keys.ON_ONE_TIME_HIGH],
                          data[keys.ON_ONE_TIME_LOW],
                          data[keys.ON_ZERO_TIME_HIGH],
                          data[keys.ON_ZERO_TIME_LOW],
                          data[keys.ON_INTERVAL])
                break

        return output

    @staticmethod
    def getOffParameters(title):
        """
        Function used to get the list of parameters associated
        with the particular title for the OFF code

        Parameters:
        -----------
        title : String
            The string corresponding to the data's OUTLET_TITLE

        Returns:
        --------
        <data> : tuple
            The OFF_CODE, OFF_ONE_TIME_HIGH, OFF_ONE_TIME_LOW, OFF_ZERO_TIME_HIGH,
            OFF_ZERO_TIME_LOW, OFF_INTERVAL corresponding to the particular
            title
        """
        try:
            # Load the data from the save file and update
            f = open(DataRW.datafileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        output = None

        for line in lines:
            data = json.loads(line)

            if data[keys.DEVICE_TITLE] == title:
                output = (data[keys.OFF_CODE],
                          data[keys.OFF_ONE_TIME_HIGH],
                          data[keys.OFF_ONE_TIME_LOW],
                          data[keys.OFF_ZERO_TIME_HIGH],
                          data[keys.OFF_ZERO_TIME_LOW],
                          data[keys.OFF_INTERVAL])
                break

        return output

    def save(self):
        """
        This function is used to write the metadata to the data file

        Parameters:
        -----------

        Returns:
        --------
        """
        # Convert the metadata dictionary object to a string
        s = json.dumps(self.data)

        # Create and write to the data file if it doesn't already exist
        if not os.path.exists(DataRW.datafileName):
            with open(DataRW.datafileName, 'w') as file:
                file.write(s)
        # Otherwise append to the document with a newline first
        else:
            with open(DataRW.datafileName, 'a') as file:
                file.write('\n' + s)

    def setParameterValue(self, parameter, value):
        """
        Function used to set the value of a parameter for the title
        of this DataRW object
        """
        self.data[parameter] = value
