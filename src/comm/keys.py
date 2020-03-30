"""
The Absolute Tinkerer

This file is used exclusively to manage all strings utilized
in the Outlet Project. These are the static strings; any user-
defined strings will be placed in JSON files elsewhere
"""

# Strings used as keys for device metadata
DEVICE_TITLE = 'Device Title'
DEVICE_STATE = 'Device State'

ON_CODE = 'ON Code'
ON_ONE_TIME_HIGH = 'ON Code Logical 1 High Time'
ON_ONE_TIME_LOW = 'ON Code Logical 1 Low Time'
ON_ZERO_TIME_HIGH = 'ON Code Logical 0 High Time'
ON_ZERO_TIME_LOW = 'ON Code Logical 0 Low Time'
ON_INTERVAL = 'Time Between ON Codes'

OFF_CODE = 'OFF Code'
OFF_ONE_TIME_HIGH = 'OFF Code Logical 1 High Time'
OFF_ONE_TIME_LOW = 'OFF Code Logical 1 Low Time'
OFF_ZERO_TIME_HIGH = 'OFF Code Logical 0 High Time'
OFF_ZERO_TIME_LOW = 'OFF Code Logical 0 Low Time'
OFF_INTERVAL = 'Time Between OFF Codes'

# Strings used as metadata options
STATE_ON = 'ON'
STATE_OFF = 'OFF'

# Strings used as keys for schedule metadata
SCHEDULE_ID = 'Schedule ID'
SCHEDULE_STATE = 'Schedule State'
SCHEDULE_TYPE = 'Absolute or Relative'
SCHEDULE_PARAMETERS = 'Schedule Parameters'
SCHEDULE_DAYS = 'Scheduled Days'
SCHEDULE_DEVICES = 'Scheduled Devices'

SCHEDULE_ABSOLUTE = 'Absolute'
SCHEDULE_RELATIVE = 'Relative'

SCHEDULE_TIME = 'Time'

SCHEDULE_AM_PM = 'AM or PM'
SCHEDULE_AM = 'AM'
SCHEDULE_PM = 'PM'

SCHEDULE_UNIT = 'Time Unit'
SCHEDULE_MINUTES = 'Minutes'
SCHEDULE_HOURS = 'Hours'

SCHEDULE_SIDE = 'Before or After'
SCHEDULE_BEFORE = 'Before'
SCHEDULE_AFTER = 'After'

SCHEDULE_SUN = 'Sunrise or Sunset'
SCHEDULE_SUNRISE = 'Sunrise'
SCHEDULE_SUNSET = 'Sunset'

# Strings used in the SunCalculator parameter file
SETTINGS_LATITUDE = 'Latitude'
SETTINGS_LONGITUDE = 'Longitude'
SETTINGS_DEVIATION = 'Standard Time Deviation from UTC'
SETTINGS_DST = 'Observes Daylight Savings Time'