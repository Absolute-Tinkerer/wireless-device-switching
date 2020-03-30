# -*- coding: utf-8 -*-
"""
The Absolute Tinkerer

This script determines the sunrise and sunset time
"""

import os
import time
from datetime import datetime, date, timedelta

from math import sin, cos, tan, acos, asin
from math import radians as rad
from math import degrees as deg

import keys


class SunCalculator:
    fileName = '../webpage/latlong.file'

    def __init__(self):
        """
        Constructor
        """
        values = SunCalculator.readDataFile()
        self._lat, self._long, self._fromUTC, self._observesDST = values

    @staticmethod
    def readDataFile():
        """
        Private function used to read the file and return the latitude and
        longitude in decimal form, as well as the number of hours your
        timezone deviates from easter standard time and whether your locale
        observes daylight savings time

        Parameters:
        -----------
        fileName : String
            The file containing the latitude and longitude values

        Returns:
        --------
        <value>, <value>, <value>, <value> : float, float, int, bool
            The latitude, longitude, hours deviated, and observes DST flag,
            respectively
        """
        lat, long, utc, dst = 0, 0, 0, True

        # Create an empty settings file if it doesn't exist
        if not os.path.exists(SunCalculator.fileName):
            with open(SunCalculator.fileName, 'w') as file:
                s = '%s=%s\n' % (keys.SETTINGS_LATITUDE, lat)
                s += '%s=%s\n' % (keys.SETTINGS_LONGITUDE, long)
                s += '%s=%s\n' % (keys.SETTINGS_DEVIATION, utc)
                s += '%s=%s' % (keys.SETTINGS_DST, dst)

                file.write(s)

            # Because the file didn't exist, we just return our starter values
            return lat, long, utc, dst
        else:
            # Read in the file
            f = open(SunCalculator.fileName, 'r')
            lines = f.readlines()
            f.flush()
            f.close()

            # Strip the newline character from each line
            lines = [line.replace('\n', '') for line in lines]

            # Locate and set the parameters we're returning
            for line in lines:
                if keys.SETTINGS_LATITUDE in line:
                    lat = float(line.split('=')[1])
                elif keys.SETTINGS_LONGITUDE in line:
                    long = float(line.split('=')[1])
                elif keys.SETTINGS_DEVIATION in line:
                    utc = int(line.split('=')[1])
                elif keys.SETTINGS_DST in line:
                    dst = line.split('=')[1].lower() == 'true'

        return lat, long, utc, dst

    @staticmethod
    def writeToDataFile(parameter, value):
        """
        Public static function used to write updated parameters to the data file
        """
        # Load the existing file
        try:
            f = open(SunCalculator.fileName, 'r')
            lines = f.readlines()
            f.close()
        except Exception:
            return

        # Locate the parameter string and replace the value
        for i, line in enumerate(lines):
            if parameter in line:
                token = line.split('=')[1].split('\n')[0]
                lines[i] = line.replace(token, value)
                break

        # Now write the built string to the file
        with open(SunCalculator.fileName, 'w') as f:
            f.writelines(lines)

    def sunriseTime(self, asFloat=True):
        """
        Public function used to retrieve the sunrise time in either float or
        string form

        Parameters:
        -----------
        asFloat : boolean
            True if this function will return the sunrise time as a float;
            False if the user wants a string

        Returns:
        --------
        <value> : float | String
            Representation of the sunrise time
        """
        sunrise = self._solarNoon() - (4/1440) * self._HaSunrise()
        sunrise *= 24

        if asFloat:
            return self._floatTime(sunrise)
        else:
            return self._stringTime(sunrise)

    def sunsetTime(self, asFloat=True):
        """
        Public function used to retrieve the sunset time in either float or
        string form

        Parameters:
        -----------
        asFloat : boolean
            True if this function will return the sunset time as a float;
            False if the user wants a string

        Returns:
        --------
        <value> : float | String
            Representation of the sunset time
        """
        sunset = self._solarNoon() + (4/1440) * self._HaSunrise()
        sunset *= 24

        if asFloat:
            return self._floatTime(sunset)
        else:
            return self._stringTime(sunset)

    def _floatTime(self, t):
        """
        t : float
            The time of day, so 0.xxx...
        """
        midnight = datetime.combine(date.today(), datetime.min.time())
        delta = timedelta(hours=t)

        return (midnight + delta).timestamp()

    def _stringTime(self, t):
        """
        t : float
            The time of day, so 0.xxx...
        """
        _time = self._floatTime(t)
        _timedate = datetime.fromtimestamp(_time)

        return _timedate.strftime("%I:%M:%S %p")

    def readouts(self):
        """
        Use for troubleshooting; use spreadsheet at NOAA site for reference
        """
        print('JD        : %s' % self._julianDay())
        print('JC        : %s' % self._julianCentury())
        print('GMLS      : %s' % self._gmls())
        print('GMAS      : %s' % self._gmas())
        print('EEO       : %s' % self._eeo())
        print('Eq of Ctr : %s' % self._eqOfCtr())
        print('True Long : %s' % self._trueLong())
        print('')
        print('')
        print('App Long  : %s' % self._appLong())
        print('MOE       : %s' % self._moe())
        print('Obliq Corr: %s' % self._obliqCorr())
        print('')
        print('Declin    : %s' % self._declination())
        print('y         : %s' % tan(rad(self._obliqCorr()/2))**2)
        print('Eq Of Time: %s' % self._eqOfTime())
        print('Ha Sunrise: %s' % self._HaSunrise())
        print('Solar Noon: %s' % self._solarNoon())
        print('')

    def _solarNoon(self):
        """
        """
        eot = self._eqOfTime()
        tz = self._timeZone()

        return (1/1440) * (720 - 4*self._long - eot + 60*tz)

    def _eqOfTime(self):
        """
        """
        y = tan(rad(self._obliqCorr()/2))**2
        gmls = self._gmls()
        gmas = self._gmas()
        eeo = self._eeo()

        rtn = y * sin(2*rad(gmls)) - 2*eeo * sin(rad(gmas))
        rtn += 4*eeo * y * sin(rad(gmas)) * cos(2*rad(gmls))
        rtn -= 0.5*y**2 * sin(4*rad(gmls)) - 1.25*eeo**2 * sin(2*rad(gmas))

        return 4*deg(rtn)

    def _obliqCorr(self):
        """
        """
        moe = self._moe()
        jc = self._julianCentury()

        return moe + 0.00256*cos(rad(125.04 - 1934.136*jc))

    def _moe(self):
        """
        """
        jc = self._julianCentury()

        rtn = (26+((21.448 - jc*(46.815 + jc*(0.00059 - jc*0.001813))))/60)/60

        return 23 + rtn

    def _gmls(self):
        """
        """
        jc = self._julianCentury()

        return (280.46646 + jc * (36000.76983 + 0.0003032*jc)) % 360

    def _gmas(self):
        """
        """
        jc = self._julianCentury()

        return 357.52911 + jc * (35999.05029 - 0.0001537*jc)

    def _eeo(self):
        """
        """
        jc = self._julianCentury()

        return 0.016708634 - jc * (0.000042037 + 0.0000001267*jc)

    def _julianCentury(self):
        """
        """
        jd = self._julianDay()

        return (1/36525) * (jd - 2451545)

    def _julianDay(self):
        """
        """
        tz = self._timeZone()
        dt_fromMidnight = 0  # Time past midnight... assume zero; low impact
        today = self._excelDate()

        return today + 2415018.5 + dt_fromMidnight - (1/24)*tz

    def _excelDate(self):
        """
        Okay, so this formulation originated from an excel worksheet from NOAA

        http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html

        They used an excel date in their computations, and as a result, I'm
        not too sure how linked the excel-based date is to the formula. As
        such, I need to convert the pythonic date to the excel date to ensure
        proper computation. Shout out to the following thread for an
        explanation on the conversion

        https://stackoverflow.com/questions/31359150/convert-date-from-excel-in-number-format-to-date-format-python
        """
        today = datetime.now().toordinal()
        from1900 = datetime(1900, 1, 1).toordinal()

        # Apparently excel does this from the last day in 1899 and assumes
        # 1900 was a leap year, which it was not
        return today - from1900 + 2

    def _timeZone(self):
        """
        """
        if self._observesDST:
            return self._fromUTC + time.localtime().tm_isdst
        else:
            return self._fromUTC

    def _HaSunrise(self):
        """
        """
        declin = self._declination()

        rtn = cos(rad(90.833))/(cos(rad(self._lat)) * cos(rad(declin)))
        rtn -= tan(rad(self._lat))*tan(rad(declin))

        return deg(acos(rtn))

    def _declination(self):
        """
        """
        appLong = self._appLong()
        oc = self._obliqCorr()

        return deg(asin(sin(rad(oc)) * sin(rad(appLong))))

    def _appLong(self):
        """
        """
        trueLong = self._trueLong()
        jc = self._julianCentury()

        return trueLong - 0.00569 - 0.00478*sin(rad(125.04 - 1934.16*jc))

    def _trueLong(self):
        """
        """
        return self._gmls() + self._eqOfCtr()

    def _eqOfCtr(self):
        """
        """
        gmas = self._gmas()
        jc = self._julianCentury()

        rtn = sin(rad(gmas)) * (1.914602 - jc*(0.004817+0.000014*jc))
        rtn += sin(rad(2*gmas)) * (0.019993 - 0.000101*jc)
        rtn += 0.000289*sin(rad(3*gmas))

        return rtn
