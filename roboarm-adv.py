# This is a rework of the RoboArm - Simple interface, allowing the motors to be run at the same time, and fully 
# adopting the correct API, allowing for other operators to use it correctly, without sending invalid commands to the system.

# OWI-535 Robotic Arm - Advanced Web Interface and Controller / Python + Bottle

# imports
from bottle import Bottle, run, template, request
import usb.core, usb.util, time

# attempt to rewrite lizquilty's OWI 535 Robotic Arm Control Web Interface from Apache to Python Bottle
# objectives: learning Bottle / Python
# Originally:
# 	- having a simple 1 file script for creating the web interface
#	- creates a simple <table> element layout with the links that trigger 1 second of movement in the corresponding motor
# In the Advanced version:
# 	- an advanced function for creating the correct string to feed to the USB, and removing the simple timing approach
#	- an advanded web interface that allows multiple inputs at the same time


# initialise the Robot Arm from the USB function
robo_arm = usb.core.find(idVendor=0x1267, idProduct=0x000)

# initiate the full_command as a complete 'stop'
usb_command_array = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']

# movearm object for controlling the Arm
def move_arm (move_command, app_mode):  # After this, all code until the demo commands must be indented

	# calculate the correct full_command
	usb_command_array[move_command[1]] = move_command[0];

	# Function to start the movement 
	robo_arm.ctrl_transfer(0x40, 6, 0x100, 0, full_command, 1000)

        # Sim -> Adv. remove the time constraint - leaving the comment in case we need to implement a safety valve
	# that turns off any movement past say 5 seconds - that would be as the result of the server and client
	# loosing connection.

	# Stop the movement after waiting a specified duration
	# time.sleep(Duration)
	# ArmCmd = [0, 0, 0]
	# RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 1000)

# Sim -> Adv - the movemap is not needed at the moment, as we're going to recreate a more flexible interface
# leaving here for reference

# movemap = {
#	'base-anti-clockwise': [0, 1, 0],
#	'base-clockwise': [0, 2, 0],
#	'shoulder-up': [64, 0, 0],
#	'shoulder-down': [128, 0, 0],
#	'elbow-up': [16, 0, 0],
#	'elbow-down': [32, 0, 0],
#	'wrist-up': [4, 0, 0],
#	'wrist-down': [8, 0, 0],
#	'grip-open': [2, 0, 0],
#	'grip-close': [1, 0, 0],
#	'light-on': [0, 0, 1],
#	'light-off': [0, 0, 0],
#	'stop': [0, 0, 0]
#}

# full width interface

# stop:
# 2-bit [00;00;00;00, 00;00;00;00, 00;00;00;00]
# 	[0, 0, 0]
# Pairs:
# 1: shoulder
# 2: elbow
# 3: wrist
# 4: gripper
# 5: <<nothing>>
# 6: <<nothing>>
# 7: <<nothing>>
# 8: base
# 9: <<nothing>>
#10: <<nothing>>
#11: <<nothing>>
#12: light

arm_interface_map = {
	'base-ccw'      : ['10', 7],
	'base-cw'       : ['01', 7],
	'base-stop'     : ['00', 7],
	'light-on'      : ['01', 11],
	'light-off'     : ['00', 11],
	'gripper-close' : ['01', 3],
	'gripper-open'	: ['10', 3],
	'gripper-stop'	: ['00', 3],
	'wrist-close'	: ['01', 2],
	'wrist-open'	: ['10', 2],
	'wrist-stop'	: ['00', 2],
	'elbow-close'	: ['01', 1],
	'elbow-open'	: ['10', 1],
	'elbow-stop'	: ['00', 1],
	'shoulder-close': ['01', 0],
	'shoulder-open'	: ['10', 0],
	'shoulder-stop' : ['00', 0]
}

app = Bottle()

@app.route('/')
def MoveArmInterface():
	
	if RoboArm is None: # in case the robotic arm hasn't been found through usb
		app_mode = "testing"
	else:
		app_mode = "live"

	# map the URL params and the appropriate movemap
	if request.params.get('command') in arm_interface_map:
		get_command = arm_interface_map[request.params.get('command')]
		MoveArm(get_command, app_mode)
	
	else:   
		moverequest = movemap['light-on']
		MoveArm(moverequest, Duration)

		# return template("Welcome to <br />The OWI-535 Robotic Arm control interface.<br />Moving: {{moveaction}}", moveaction=moverequest)
		
		return '''
		<!DOCTYPE html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Robotic Arm</title>

	<style>
		table {
			text-align: center;
			width: 100%;
		}

		td {
			border: 1px solid black;
		}
		
		a {
			font-size: large;
		}
	</style>
	
	</head>
	
	<body>
	    <table>
		    <tr>
			    <td colspan="2"><a href="/?move=grip-open">Gripper Open</a></td>
			    <td colspan="2"><a href="/?move=grip-close">Gripper Close</a></td>
		    </tr>
		    <tr>
			    <td rowspan="6"><a href="/?move=base-clockwise">Base CW</a></td>
			    <td colspan="2"><a href="/?move=wrist-up">Wrist Up</a></td>
			    <td rowspan="6"><a href="/?move=base-anti-clockwise">Base CCW</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=wrist-down">Wrist Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=elbow-up">Elbow Up</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=elbow-down">Elbow Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=shoulder-up">Shoulder Up</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=shoulder-down">Shoulder Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?move=light-on">Light On</a></td>
			    <td colspan="2"><a href="/?move=light-off">Light Off</a></td>
		    </tr>
	    </table>
	</body>
</html>

		'''

run(app, host='0.0.0.0', port=8080)


