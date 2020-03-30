"""
The Absolute Tinkerer
"""

import sys

from flask import Flask, render_template, request, jsonify
from datetime import date

# Append necessary python source code folders
sys.path.append('../comm/')

# Import custom packages
from RxTx import RxTx
from DataRW import DataRW
from ScheduleRW import ScheduleRW
from ScheduleThread import ScheduleThread
from suncalculator import SunCalculator
import keys

app = Flask(__name__)
data = DataRW('Placeholder')

@app.route('/')
def index():
    today = date.today()
    today = today.strftime('%A, %d %B, %Y')

    calc = SunCalculator()
    sunrise = calc.sunriseTime(asFloat=False)
    sunset = calc.sunsetTime(asFloat=False)

    return render_template('index.html', today=today, sunrise=sunrise,
                           sunset=sunset)

@app.route('/checkTitle', methods=['POST'])
def checkTitle():
    title = request.form['title']
    if not DataRW.isTitleValid(title):
        return jsonify({'result': 'Title Exists'})
    else:
        data = DataRW(title)
        return jsonify({'result': ''})

@app.route('/getTitles', methods=['POST'])
def getTitles():
    titles = DataRW.getTitles()
    # Need the array in reverse order for proper load in webpage
    titles.reverse()

    return jsonify({'result': titles})

@app.route('/getStates', methods=['POST'])
def getStates():
    titles = DataRW.getTitles()
    # Need the array in reverse order for proper load in webpage
    titles.reverse()

    rtn = []
    for title in titles:
        state = DataRW.getState(title)
        rtn.append([title, state])

    return jsonify({'result': rtn})

@app.route('/turnOn', methods=['POST'])
def turnOn():
    title = request.form['title']

    c1, c2, c3, c4, c5, c6 = DataRW.getOnParameters(title)
    rxtx.txCode(c1, c2, c3, c4, c5, c6)

    DataRW.setState(title, keys.STATE_ON)

    return jsonify({'result': ''})

@app.route('/turnOff', methods=['POST'])
def turnOff():
    title = request.form['title']

    c1, c2, c3, c4, c5, c6 = DataRW.getOffParameters(title)
    rxtx.txCode(c1, c2, c3, c4, c5, c6)

    DataRW.setState(title, keys.STATE_OFF)

    return jsonify({'result': ''})

@app.route('/changeTitles', methods=['POST'])
def changeTitles():
    newTitles = request.form.getlist('titles[]')

    DataRW.updateTitles(newTitles)

    return jsonify({'result': ''})

@app.route('/deleteOutlets', methods=['POST'])
def deleteOutlets():
    titles = request.form.getlist('titles[]')

    for title in titles:
        DataRW.remove(title)

    return jsonify({'result': ''})

@app.route('/removeAdd', methods=['POST'])
def removeAdd():
    title = request.form['title']

    data = DataRW('Placeholder')

    return jsonify({'result': ''})

@app.route('/findOnCode', methods=['POST'])
def findOnCode():
    codes = rxtx.sniffCode()

    if codes is None:
        return jsonify({'result': 'Code Not Found'})
    else:
        title = request.form['title']
        if DataRW.isTitleValid(title):
            c1, c2, c3, c4, c5, c6 = codes
            data.setParameterValue(keys.ON_CODE, c1)
            data.setParameterValue(keys.ON_ONE_TIME_HIGH, c2)
            data.setParameterValue(keys.ON_ONE_TIME_LOW, c3)
            data.setParameterValue(keys.ON_ZERO_TIME_HIGH, c4)
            data.setParameterValue(keys.ON_ZERO_TIME_LOW, c5)
            data.setParameterValue(keys.ON_INTERVAL, c6)

            return jsonify({'result': c1})
        else:
            return jsonify({'result': 'Error: Title Conflict'})

@app.route('/findOffCode', methods=['POST'])
def findOffCode():
    codes = rxtx.sniffCode()

    if codes is None:
        return jsonify({'result': 'Code Not Found'})
    else:
        title = request.form['title']
        if DataRW.isTitleValid(title):
            c1, c2, c3, c4, c5, c6 = codes
            data.setParameterValue(keys.OFF_CODE, c1)
            data.setParameterValue(keys.OFF_ONE_TIME_HIGH, c2)
            data.setParameterValue(keys.OFF_ONE_TIME_LOW, c3)
            data.setParameterValue(keys.OFF_ZERO_TIME_HIGH, c4)
            data.setParameterValue(keys.OFF_ZERO_TIME_LOW, c5)
            data.setParameterValue(keys.OFF_INTERVAL, c6)

            return jsonify({'result': c1})
        else:
            return jsonify({'result': 'Error: Title Conflict'})

@app.route('/finalizeSave', methods=['POST'])
def finalizeSave():
    title = request.form['title']

    # Save the device state as off
    data.setParameterValue(keys.DEVICE_TITLE, title)
    data.setParameterValue(keys.DEVICE_STATE, keys.STATE_OFF)
    data.save()

    # Reset the data object
    # data = DataRW('Placeholder')

    return jsonify({'result': ''})

@app.route('/schedule.html')
def schedule():
    today = date.today()
    today = today.strftime('%A, %d %B, %Y')

    calc = SunCalculator()
    sunrise = calc.sunriseTime(asFloat=False)
    sunset = calc.sunsetTime(asFloat=False)

    return render_template('schedule.html', today=today, sunrise=sunrise,
                           sunset=sunset)

@app.route('/addToSchedule', methods=['POST'])
def addToSchedule():
    scheduleType = request.form['schedule_type']
    params = request.form.getlist('params[]')
    days = request.form.getlist('days[]')
    devices = request.form.getlist('devices[]')

    # Instantiate the data element
    schedule = ScheduleRW(scheduleType)

    # Transfer the parameters from params
    if len(params) == 2:
        schedule.setParameterValue(keys.SCHEDULE_TIME, params[0])
        schedule.setParameterValue(keys.SCHEDULE_AM_PM, params[1])
    else:
        schedule.setParameterValue(keys.SCHEDULE_TIME, int(params[0]))
        schedule.setParameterValue(keys.SCHEDULE_UNIT, params[1])
        schedule.setParameterValue(keys.SCHEDULE_SIDE, params[2])
        schedule.setParameterValue(keys.SCHEDULE_SUN, params[3])

    # Cast the days, which are strings, as booleans
    days = [day.lower() == 'true' for day in days]

    # Create a 2d list from the strings in devices, delineated by a colon
    for i, device in enumerate(devices):
        device, state = device.split(':')
        state = keys.STATE_ON if state.lower() == "on" else keys.STATE_OFF
        devices[i] = [device, state]

    # Transfer the remaining parameters
    schedule.setParameterValue(keys.SCHEDULE_DAYS, days)
    schedule.setParameterValue(keys.SCHEDULE_DEVICES, devices)

    # Finalize the save
    schedule.save()

    return jsonify({'result': ''})

@app.route('/getSchedules', methods=['POST'])
def getSchedules():
    schedules = ScheduleRW.getSchedules()

    # Need to reverse the list so it loads properly in the webpage
    schedules.reverse()

    return jsonify({'result': schedules})

@app.route('/toggleSchedule', methods=['POST'])
def toggleSchedule():
    ID = request.form['id']
    state = request.form['state'] == 'true'

    ScheduleRW.setState(ID, state)

    return jsonify({'result': ''})

@app.route('/deleteSchedule', methods=['POST'])
def deleteSchedule():
    ID = request.form['id']

    ScheduleRW.remove(ID)

    return jsonify({'result': ''})

@app.route('/more.html')
def more():
    return render_template('more.html')

@app.route('/getSettings', methods=['POST'])
def getSettings():
    lat, long, utc, dst = SunCalculator.readDataFile()

    return jsonify({'result': [lat, long, utc, dst]})

@app.route('/more_submit', methods=['POST'])
def more_submit():
    lat = request.form['lat']                     # Latitude
    long = request.form['long']                   # Longitude
    tz = request.form['tz']                       # Time Zone
    dst = request.form['dst']                     # Observes DST?

    # Now set these values in the calculator file
    SunCalculator.writeToDataFile(keys.SETTINGS_LATITUDE, lat)
    SunCalculator.writeToDataFile(keys.SETTINGS_LONGITUDE, long)
    SunCalculator.writeToDataFile(keys.SETTINGS_DEVIATION, tz)
    SunCalculator.writeToDataFile(keys.SETTINGS_DST, dst)

    return jsonify({'result': ''})


if __name__ == '__main__':
    try:
        # Initialize the RxTx Library
        rxtx = RxTx()
        # Initialize the Scheduler
        scheduler = ScheduleThread(rxtx, scanInterval=15)
        scheduler.run()

        # Start the Server
        app.run(host='0.0.0.0', port=5000, debug=False)

        # Clean up
        scheduler.terminate()
        rxtx.cleanup()
    except Exception as e:
        scheduler.terminate()
        rxtx.cleanup()
        print(e)
