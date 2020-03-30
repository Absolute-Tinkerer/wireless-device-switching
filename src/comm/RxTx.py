"""
20 April 2019

Absolute Tinkerer

This class is used to handle all Rx and Tx operations inherent to the
433.92MHz Outlet project

"""

import time
import RPi.GPIO as GPIO

RECEIVE_PIN = 11
TRANSMIT_PIN = 7

class RxTx:
    def __init__(self, codes={}):
        """
        Constructor

        Parameters:
        -----------
        codes : key-value pairs
            The values are the known binary codes button presses
        """
        # Assign class variables
        self._codes = codes

        # Set up the Raspberry Pi Model 3 B+
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(RECEIVE_PIN, GPIO.IN)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    """
    -----------------------------------------------------------------
                           Private Functions
    -----------------------------------------------------------------
    """
    def _createBuffer(self, start_time, mode=GPIO.HIGH):
        """
        Private function used to create the buffer that will later be
        processed. Function allows for the user to specify a high- or
        low-centric buffer

        Parameters:
        -----------
        start_time : float
            The time that the detection period began
        mode : int
            GPIO.HIGH or GPIO.LOW

        Returns:
        --------
        buffer : list of floats
            The time spent as HIGH or LOW, depending on mode
        """
        if mode != GPIO.HIGH and mode != GPIO.LOW:
            raise(Exception('Mode must be either GPIO.HIGH or GPIO.LOW'))

        buffer_limit = 200
        dt = -1
        t = 0
        buffer = []
        while len(buffer) < buffer_limit:
            dt = time.time() - start_time
            bit = GPIO.input(RECEIVE_PIN)

            if bit == mode:
                t += dt
            else:
                if t != 0:
                    buffer.append(t)
                t = 0

        return buffer

    def _processBuffer(self, buffer, mode=GPIO.HIGH):
        """
        Private function used to handle the processing of the
        buffer generated from constantly listening to the receiver
        input

        Parameters:
        -----------
        buffer : list of floats
            Contains the times during which the receiver measured
            high (1) inputs
        mode : int
            GPIO.HIGH or GPIO.LOW

        Returns:
        --------
        <value> : list of strings
            List of unique codes from this buffer
        """
        if mode != GPIO.HIGH and mode != GPIO.LOW:
            raise(Exception('Mode must be either GPIO.HIGH or GPIO.LOW'))

        codes = []
        if mode == GPIO.HIGH:
            for i in range(len(buffer) - 25):
                l_max = max(buffer[i:i+25])
                l_min = min(buffer[i:i+25])
                thresh = (l_max - l_min)/3 + l_min
                out = ''
                for j in range(25):
                    if buffer[i+j] < thresh:
                        out += '1'
                    else:
                        out += '0'

                # Append the unique code
                if out not in codes:
                    codes.append(out)
        else:
            for i in range(len(buffer) - 25):
                # The max is the long delay between pulses; this
                # is our reference point
                l_max = max(buffer[i:i+25])
                l_min = min(buffer[i:i+25])
                idx = buffer.index(l_max)
                # We want to pass until idx == i
                if idx == i:
                    # Reset the local max value
                    l_max = max(buffer[i+1:i+25])
                    thresh = (l_max - l_min)/3 + l_min
                    out = ''
                    for j in range(24):
                        if buffer[i+1+j] < thresh:
                            out += '0'
                        else:
                            out += '1'
                    # Append the unique code
                    if out not in codes:
                        codes.append(out)
        return codes

    def _sniffTiming(self, start_time):
        """
        Private function used to discover the required timing
        for the short, long, and extended delay

        Parameters:
        -----------
        start_time : float
            The time that the detection time began

        Returns:
        --------
        one_high : float
            Represents the high time for a '1'
        one_low : float
            Represents the low time for a '1'
        zero_high : float
            Represents the high time for a '0'
        zero_low : float
            Represents the low time for a '0'
        interval : float
            The delay representing the low time between codes
        """
        buffer_limit = 1000
        buffer = []
        temp_bit = -1

        one_high = -1
        one_low = -1
        zero_high = -1
        zero_low = -1
        interval = -1

        # This builds an array of dt's where the bits alternate
        # between 1's and 0's
        while len(buffer) < buffer_limit:
            dt = time.time() - start_time
            bit = GPIO.input(RECEIVE_PIN)

            if len(buffer) == 0:
                buffer.append(dt)
                temp_bit = bit
            elif bit != temp_bit:
                buffer.append(dt)
                temp_bit = bit
                start_time = time.time()

        POWER = 1e5
        simplified = [int(POWER*b) for b in buffer]

        # The interval between codes is the largest number
        interval = max(simplified)
        idx = simplified.index(interval)
        interval /= POWER

        # the short and long high times alternate every two increments
        # in index; the larger of the two determines the bit type
        while idx < len(simplified) - 1:
            first = simplified[idx+1]
            second = simplified[idx+2]
            idx += 2

            if first < second:
                one_high = first/POWER
                one_low = second/POWER
            else:
                zero_high = first/POWER
                zero_low = second/POWER

            if(one_high != -1 and one_low != -1 and
               zero_high != -1 and zero_low != -1):
                break

        return one_high, one_low, zero_high, zero_low, interval

    """
    -----------------------------------------------------------------
                           Public Functions
    -----------------------------------------------------------------
    """
    def rxCode(self, runTime=None):
        """
        Public function used to detect a button press and return the code
        when a known code is found

        Parameters:
        -----------
        runTime : int
            Detection time, in seconds

        Returns:
        --------
        """
        start_time = time.time()

        try:
            while True:
                # Break called when the user specified a time
                if(runTime is not None and
                   (time.time() - start_time) > runTime):
                    break

                # Build the buffer to test
                buffer = self._createBuffer(start_time)

                # Process the buffer into codes
                codes = self._processBuffer(buffer)

                # Test for code in known codes
                key = ''
                for i, l_key in enumerate(self._codes):
                    for j, l_code in enumerate(codes):
                        if l_code == self._codes[l_key]:
                            key = l_key
                            break
                if key:
                    return key

        except Exception as e:
            raise(Exception(e))

    def txCode(self, code, one_high, one_low, zero_high, zero_low,
               interval):
        """
        Public function used to transmit codes of indeterminate
        length

        Parameters:
        -----------
        code : String
            A string of binary digits. This function will likely
            error otherwise
        one_high : float
            Represents the high time for a '1'
        one_low : float
            Represents the low time for a '1'
        zero_high : float
            Represents the high time for a '0'
        zero_low : float
            Represents the low time for a '0'
        interval : float
            The delay representing the low time between codes

        Returns:
        --------
        """
        for i in range(5):
            for bit in code:
                if int(bit) == GPIO.HIGH:
                    GPIO.output(TRANSMIT_PIN, GPIO.HIGH)
                    time.sleep(one_high)
                    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
                    time.sleep(one_low)
                else:
                    GPIO.output(TRANSMIT_PIN, GPIO.HIGH)
                    time.sleep(zero_high)
                    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
                    time.sleep(zero_low)
            GPIO.output(TRANSMIT_PIN, GPIO.LOW)
            time.sleep(interval)

    def sniffCode(self, seekTime=2):
        """
        Public function used to sniff out new codes that the
        user is trying to detect. The user should press and hold
        the button being sniffed for the duration of this function.

        Parameters:
        -----------
        seekTime : int
            Time allocated to sniff the code within

        Returns:
        --------
        high_code : string
            None if no code detected; otherwise returns the
            detected code
        one_high : float
            Represents the high time for a '1'
        one_low : float
            Represents the low time for a '1'
        zero_high : float
            Represents the high time for a '0'
        zero_low : float
            Represents the low time for a '0'
        interval : float
            The delay representing the low time between codes

        """
        start_time = time.time()

        # Run the sniffer for the allocated amount of time
        while time.time() - start_time < seekTime:
            # Get the unique codes corresponding to pulse down-time 
            buffer = self._createBuffer(start_time, mode=GPIO.LOW)
            low_codes = self._processBuffer(buffer, mode=GPIO.LOW)

            # Get the unique codes corresponding to pulse up-time
            buffer = self._createBuffer(start_time)
            high_codes = self._processBuffer(buffer)

            # Get the delay times
            o_h, o_l, z_h, z_l, _i = self._sniffTiming(time.time())

            # The up-time codes are complete, but the down-time codes
            # have the long down-time between pulses, leading to an
            # incomplete code, BUT we can use this incomplete code
            # to mark the 24 of the 25 digits corresponding to the
            # correct code. Odds of wrong code: 2^-25
            for high_code in high_codes:
                for low_code in low_codes:
                    # Our low code collection ignores the last bit due
                    # to ambiguity as it its length (blank between
                    # pulses)
                    if low_code == high_code[:-1]:
                        return high_code, o_h, o_l, z_h, z_l, _i

    def cleanup(self):
        """
        Public function that must be called upon the termination of
        the program. This function handles the necessary cleanup
        actions required.

        Parameters:
        -----------
        Returns:
        --------
        """
        # Clean-up code
        GPIO.output(TRANSMIT_PIN, GPIO.LOW)
        GPIO.cleanup()
