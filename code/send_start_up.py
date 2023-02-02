from guizero import *   
import tkinter as tk
import tkinter.font as font
import socket
import subprocess
import ipaddress
import RPi.GPIO as GPIO
import urllib.request
import sys
import board
import _thread
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import adafruit_vl53l0x
import os
from time import sleep
from motors import *


i2c = busio.I2C(board.SCL, board.SDA)


mcp = MCP23017(i2c) # initialized port extender




##### Set xshut pin directions and levels #####

enable0 = mcp.get_pin(0)
enable0.pull = Pull.UP
enable0.direction = Direction.OUTPUT
enable0.value = False
   
enable1 = mcp.get_pin(1)
enable1.pull = Pull.UP
enable1.direction = Direction.OUTPUT
enable1.value = False
    
enable2 = mcp.get_pin(2)
enable2.pull = Pull.UP
enable2.direction = Direction.OUTPUT
enable2.value = False
    
enable3 = mcp.get_pin(3)
enable3.pull = Pull.UP
enable3.direction = Direction.OUTPUT
enable3.value = False
    
    
##### enable one sensor after the other by setting xshut pins high one after the oter and set new addresses
sensors_functioning = [True, True, True, True]
try:
    enable0.value = True
    ToF0 = adafruit_vl53l0x.VL53L0X(i2c)
    ToF0.set_address(0x30)
except:
    sensors_functioning[0] = False
    print ("Right sensor not working")
    backgrd = "red"

try:
    enable1.value = True
    ToF1 = adafruit_vl53l0x.VL53L0X(i2c)
    ToF1.set_address(0x31)
except:
    sensors_functioning[1] = False
    print ("Front sensor not working")
    backgrd = "red"

try:
    enable2.value = True
    ToF2 = adafruit_vl53l0x.VL53L0X(i2c)
    ToF2.set_address(0x32)
except:
    sensors_functioning[2] = False
    print ("Back sensor not working")
    backgrd = "red"

try:
    enable3.value = True
    ToF3 = adafruit_vl53l0x.VL53L0X(i2c)
    ToF3.set_address(0x33)
except:
    sensors_functioning[3] = False
    print ("Left sensor not working")
    backgrd = "red" 

#### set output pins for motor drivers 

in1 = mcp.get_pin(9)
in1.pull = Pull.UP
in1.direction = Direction.OUTPUT
in1.value = False

in2 = mcp.get_pin(8)
in2.pull = Pull.UP
in2.direction = Direction.OUTPUT
in2.value = False

in3 = mcp.get_pin(11)
in3.pull = Pull.UP
in3.direction = Direction.OUTPUT
in3.value = False

in4 = mcp.get_pin(12)
in4.pull = Pull.UP
in4.direction = Direction.OUTPUT
in4.value = False

stby = mcp.get_pin(10)
stby.pull = Pull.UP
stby.direction = Direction.OUTPUT
stby.value = True

en = 5
en2 = 6

temp1=0
GPIO.setmode(GPIO.BCM)

GPIO.setup(en,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

p_val=GPIO.PWM(en,1000)
p2_val = GPIO.PWM(en2,1000)
p_val.start(50)
p2_val.start(50)
p_val.ChangeDutyCycle(50)
p2_val.ChangeDutyCycle(50)

start_time = 0
stby.value = True
def move(direction):
        i1, i2, i3, i4 = dir(direction)
        in1.value = i1
        in2.value = i2
        in3.value = i3
        in4.value = i4

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

rasp_id = socket.gethostname()
robot_id = rasp_id[11:len(rasp_id)]

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))


data = 'none'
p = None 
data = None
addr = None
started1 = False
started2 = False
last_message = ''
curr_message = ''

text_append = ''
backgrd = "bisque"

def run_code():
    global backgrd, last_message, started1, p, addr, data, start_text
    if (started1 == False):
        print ("starting")
        backgrd = run_code_btn_colour

        start_text.value = "Starting now \n please wait"
        #send the ip address and port as arguments when running python code 
        p = subprocess.Popen(["python3", "/home/pi/Desktop/code.py"]) 
        started1 = True
        
    last_message = 'run1'

def update_code():
    global backgrd, last_message, started1, p, addr, data, start_text
    try:
       url = 'http://' + addr[0] + ':8000/code.py'
       urllib.request.urlretrieve(url, '/home/pi/Desktop/code.py')
       start_text.value = "Code updated"
       print ("updated code")
       backgrd = fetch_code_btn_colour
    except: 
        start_text.value = "Did not update. \n Send a handshake \n command from \n server_udp.py from \n computer so the robot \n knows the addr"
        print ("Need to handshake first")
        backgrd = "red"
    
    last_message = 'update'

def startup():
    global backgrd, last_message, started1, p, addr, data, start_text
    try: 
        url = 'http://' + addr[0] + ':8000/send_start_up.py'
        urllib.request.urlretrieve(url, '/home/pi/Desktop/send_start_up.py')
        backgrd = fetch_startup_btn_colour
        print ("updated startup")
        start_text.value = "Startup code udpated"
    except:
        start_text.value = "Did not update. \n Send a handshake \n command from \n server_udp.py from \n computer so the robot \n knows the addr"
        print ("Need to handshake first")
        backgrd = "red"

    last_message = 'startup'

def central():
    global backgrd, last_message, started1, p, addr, data, start_text
    last_message = 'central'
    backgrd = connect_central_btn_colour
    print ("switched to central")
    subprocess.call ("sudo cp /home/pi/Desktop/central.conf /etc/wpa_supplicant/wpa_supplicant.conf", shell = True)
    start_text.value = "Switched to Central \n SSID: SwarmTouch \n Now reboot \n \n WARNING: it takes some \n time to find and \n connect to the network \n so be patient \n upon reboot"

def adhoc():
    global backgrd, last_message, started1, p, addr, data, start_text
    last_message = 'adhoc'
    backgrd = connect_adhoc_btn_colour
    print ("switched to adhoc")
    subprocess.call ("sudo cp /home/pi/Desktop/adhoc.conf /etc/wpa_supplicant/wpa_supplicant.conf", shell = True)
    start_text.value = "Switched to Adhoc \n SSID: mosaix \n Now reboot"

def shutdown():
    subprocess.call("sudo poweroff", shell=True)

def reboot():
    subprocess.call("sudo reboot", shell=True)

def test_motors(cmd):
    global backgrd, last_message, started1, p, addr, data, start_text
    last_message = 'test_motors'
    print ("move: ", cmd)
    backgrd = test_motors_btn_colour
    if (cmd == "forward"):
        move("forward")
        start_text.value = "forward"
        start_text.after(1000,lambda: test_motors("backward"))
    elif (cmd == "backward"):
        move("backward")
        start_text.value = "forward \n backward"
        start_text.after(1000,lambda: test_motors("right"))
    elif (cmd == "right"):
        move("right")
        start_text.value = "forward \n backward \n right"
        start_text.after(1000,lambda: test_motors("left"))
    elif (cmd == "left"):
        move("left")
        start_text.value = "forward \n backward \n right \n left"
        start_text.after(1000,lambda: test_motors("stop"))
    else:
        move("stop")
        start_text.value = "forward \n backward \n right \n left \n stop"


def test_sensors():
    global backgrd, last_message, started1, p, addr, data, start_text
    sensor_vals = ""
    last_message = 'test_sensors'
    backgrd = test_sensors_btn_colour
    if (sensors_functioning[0] == True):
        sensor_vals = "Right: " + str(ToF0.range) + "\n"
    else:
         sensor_vals = "Right: ERROR" + "\n"

    if (sensors_functioning[1] == True):
        sensor_vals += "Front: " + str(ToF1.range) + "\n"
    else:
        sensor_vals += "Front: ERROR" + "\n"

    if (sensors_functioning[2] == True):
        sensor_vals += "Back: " + str(ToF2.range) + "\n"
    else:
        sensor_vals += "Back: ERROR" + "\n"

    if (sensors_functioning[3] == True):
        sensor_vals += "Left: " + str(ToF3.range) 
    else:
        sensor_vals += "Left: ERROR" 
    start_text.value = sensor_vals


def listen():
  while True:
    
    global backgrd, last_message, started1, p, addr, data

    data, addr = client.recvfrom(1024)
    data = data.decode()
    print ("last message", last_message)
    if (data == 'handshake'):
        if (last_message != 'handshake'):
                start_text.value =" Handshake.... ok"
                print ("Handshake")
                backgrd = "yellow"
                last_message = 'handshake'
              
    elif (data[0] == 'r' and data[1] == 'u' and data[2] == 'n'):
        if (last_message != 'run1'):
            run_code()
        else:
            print ("ignored run command")

            
    elif (data == 'stop'):
        if (last_message != 'stop'):
            in1.value = False
            in2.value = False
            in3.value = False
            in4.value = False
            GPIO.cleanup()
            p.kill()
            start_text.value = "Stopped running"
            print ("stopped running")
            backgrd = "bisque"
            
            started1 = False
            
            started2 = False
            last_message = 'stop'

    elif (data == 'update'):
        update_code()

    elif (data == 'startup'):
        startup()
            

    elif (data == 'central'):
        central()
            

    elif (data == 'adhoc'):
        adhoc()
 
    elif (data == 'reboot'):
        subprocess.call("sudo reboot", shell=True)

    elif (data == 'delete'):
        if (last_message != 'delete'):
            start_text.value = "Log files deleted"
            print ("deleted")
            backgrd = "bisque"
            last_message = 'delete'
            subprocess.call("sudo rm /home/pi/Desktop/opinions*.csv", shell=True)
            

    elif (data == 'shutdown'):
        subprocess.call("sudo poweroff", shell=True)


_thread.start_new_thread(listen,())


def main_app():
    app.bg = backgrd
    run_code_btn.bg = run_code_btn_colour
    connect_adhoc_btn.bg = connect_adhoc_btn_colour
    connect_central_btn.bg = connect_central_btn_colour
    fetch_code_btn.bg = fetch_code_btn_colour
    fetch_startup_btn.bg = fetch_startup_btn_colour
    shutdown_btn.bg = shutdown_btn_colour
    reboot_btn.bg = reboot_btn_colour
    test_motors_btn.bg = test_motors_btn_colour
    test_sensors_btn.bg = test_sensors_btn_colour
    start_text.after(2,main_app)
    


title_app = "Robot ID: " + robot_id
app = App(title=title_app, bg = "black", layout = "grid")

run_code_btn = PushButton(app, width=10, height=4, grid=[0,0], command= lambda: run_code(), text = "Run code")
run_code_btn_colour = "sea green"
connect_adhoc_btn = PushButton(app, width=10, height=4, grid=[0,1], command= lambda: adhoc(), text = "Connect Adhoc")
connect_adhoc_btn_colour = "HotPink1"
connect_central_btn = PushButton(app, width=10, height=4, grid=[0,2], command= lambda: central(), text = "Connect Central")
connect_central_btn_colour= "medium orchid"
fetch_code_btn = PushButton(app, width=10, height=4, grid=[1,0], command= lambda: update_code(), text = "Fetch code")
fetch_code_btn_colour = "orange"
fetch_startup_btn = PushButton(app, width=10, height=4, grid=[1,1], command= lambda: startup(), text = "Fetch startup")
fetch_startup_btn_colour = "DodgerBlue3"
shutdown_btn = PushButton(app, width=10, height=4, grid=[1,2], command= lambda: shutdown(), text = "Shutdown")
shutdown_btn_colour = "grey"
reboot_btn = PushButton(app, width=10, height=4, grid=[2,0], command= lambda: reboot(), text = "Reboot")
reboot_btn_colour = "grey"
test_motors_btn = PushButton(app, width=10, height=4, grid=[2,1], command= lambda: test_motors("forward"), text = "Test motors")
test_motors_btn_colour = "indian red"
test_sensors_btn = PushButton(app, width=10, height=4, grid=[2,2], command= lambda: test_sensors(), text = "Test sensors")
test_sensors_btn_colour= "dark turquoise"


start_text = Text(app, grid=[3,0,3,3], font="Helvetica", size=10, text = "Hello") 
    

main_app()

app.display()

