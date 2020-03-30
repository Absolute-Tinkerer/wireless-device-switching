# wireless-device-switching
Responsive web frontend to switch on/off device power manually or via schedule

<hr>

The beauty of this project is it allows you to switch on/off devices (typically lights plugged into relays) through a web frontend, which enables you to use any device with a modern browser to control the system. I've only tested this on Chrome. Additionally, you can schedule devices to turn on/off at a specific time (absolute or relative) and day of week.

The following is a list of everything you need to make this project:
<ul>
  <li>Raspberry Pi (<a href="https://www.amazon.com/Raspberry-Complete-Starter-Cooling-Heavy-Aluminum/dp/B07BDQZ2TB/ref=sr_1_1_sspa?crid=DUA31CO4DEL7" target="_blank">I used a RPi 3 Model B+</a>)</li>
  <li>A 433.92MHz Transmitter and Receiver (<a href="https://www.amazon.com/RioRand-Superheterodyne-transmitter-receiver-3400/dp/B00HEDRHG6" target="_blank">I used this one</a>)</li>
  <li>433.92MHz Outlet Relays (<a href="https://www.amazon.com/Etekcity-Household-Appliances-Unlimited-Connections/dp/B00DQELHBS" target="_blank">I used this</a>)</li>
  <li>Female-to-Female Jumpers (<a href="https://www.amazon.com/REXQualis-120pcs-Breadboard-Arduino-Raspberry/dp/B072L1XMJR" target="_blank">I bought this bunch</a>)</li>
  <li>A computer on your network, as well as a keyboard, mouse, and computer monitor</li>
</ul>

<hr>
<h3>(1) Set Up Your Raspberry Pi</h3>
<ul>
  <li>Install Raspbian on your Pi</li>
  <li>Connect your keyboard, mouse, and monitor to the Pi and connect your Pi to your network via WiFi or Ethernet</li>
  <li>Confirm you have python3 on your Pi by typing <code>python3</code> into the command line. Exit the terminal with <code>exit()</code></li>
  <li>Get the Pi's IP address typing <code>ifconfig</code> into the command line. Write this down for later.</li>
  <li>Download <a href="https://www.realvnc.com/en/connect/download/viewer/" target="_blank">VNC Viewer</a> if you want to remote into your Pi from a computer. Additional Pi configurations: <a href="https://www.raspberrypi.org/documentation/remote-access/vnc/" target="_blank">link</a></li>
</ul>

<hr>
<h3>(2) Connect Hardware</h3>
<ul>
  <li>Type <code>pinout</code> into the command line for the Pi's pinout</li>
  <li>Connect the following chip pins to the appropriate pins on the Pi:</li>
  <ul>
    <li>Receiver Chip:</li>
    <ul>
      <li>GND - Any ground pin</li>
      <li>DATA - Pin 11</li>
      <li>DER - Not connected</li>
      <li>+5V - Any +5V pin</li>
      <li>+5V - Any +5V pin</li>
      <li>GND - Any ground pin</li>
      <li>GND - Not connected</li>
      <li>ANT - Not connected</li>
    </ul>
    <li>Transmitter Chip:</li>
    <ul>
      <li>P - 3.3V pin</li>
      <li>DA - Pin 7</li>
      <li>G - Any ground pin</li>
      <li>AN - Not connected</li>
    </ul>
  </ul>
  <li>Of course you can use different pins besides 11 and 7, those those are the pins configured in RxTx.py</li>
</ul>

<hr>
<h3>(3) Try it!</h3>
<p>Go ahead and start the server by opening a terminal window, navigating to <code>src/webpage/app.py</code>, and start the server by typing <code>python3 app.py</code>.</p>

To add a device, ensure you're depressing and holding the associated on/off button on the remote that came with your relays before clicking the <code>ON Code</code> button.

<hr>
<h3>(4) Debugging</h3>
<p>Use the <code>src/comm/test.py</code> file to view a particular code. I've designed this to work with 25 bit codes, so if your code is a different length, let me know. I'll work to modify the code to accept generic code lengths.</p>

The most common failure point is (1) either your connections are poor or invalid or (2) you purchased a bad receiver. I had receiver issues until I purchased the one I linked above.
