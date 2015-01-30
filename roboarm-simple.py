# OWI-535 Robotic Arm - Web Interface / Python + Bottle
# imports
from bottle import Bottle, run, template, request
import usb.core, usb.util, time

# attempt to rewrite lizquilty's OWI 535 Robotic Arm Control Web Interface from Apache to Python Bottle
# objectives: learning Bottle / Python
# 	- having a simple 1 file script for creating the web interface
#   - creates a simple <table> element layout with the links that trigger 1 second of movement in the corresponding motor

# constants
Duration = 1

# initialise the Robot Arm from the USB function
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x000)

# movearm object for controlling the Arm
def MoveArm (ArmCmd, Duration):  # After this, all code until the demo commands must be indented
	' Function to start the movement '
	RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 1000)

	#Stop the movement after waiting a specified duration
	time.sleep(Duration)
	ArmCmd = [0, 0, 0]
	RoboArm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 1000)

movemap = {
	'base-anti-clockwise': [0, 1, 0],
	'base-clockwise': [0, 2, 0],
	'shoulder-up': [64, 0, 0],
	'shoulder-down': [128, 0, 0],
	'elbow-up': [16, 0, 0],
	'elbow-down': [32, 0, 0],
	'wrist-up': [4, 0, 0],
	'wrist-down': [8, 0, 0],
	'grip-open': [2, 0, 0],
	'grip-close': [1, 0, 0],
	'light-on': [0, 0, 1],
	'light-off': [0, 0, 0],
	'stop': [0, 0, 0]
}



app = Bottle()

@app.route('/')
def MoveArmInterface():
	
	if RoboArm is None: # in case the robotic arm hasn't been found through usb
		return '''
			The OWI-535 Robotic Arm has not been found.
		'''
	else:
        	# map the URL params and the appropriate movemap
		if request.params.get('move') in movemap:
			moverequest = movemap[request.params.get('move')]
			MoveArm(moverequest, Duration)
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


