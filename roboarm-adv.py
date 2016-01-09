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


# initialise the Robot Arm variable from the USB.core function - that Vendor ID is specific to the OWI USB interface board for this robot arm
robo_arm = usb.core.find(idVendor=0x1267, idProduct=0x000)

# initiate the full_command as a complete 'stop'
usb_command_array = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
compiled_command = [0, 0, 0]

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

# Groups:
# 1: Arm motors
# 2: Base motor
# 3: Light

arm_interface_map = {
	'base-ccw'      : ['10', 7],
	'base-cw'       : ['01', 7],
	'base-stop'     : ['00', 7],
	'light-on'      : ['01', 11],
	'light-off'     : ['00', 11],
	'gripper-close' : ['01', 3],
	'gripper-open'	: ['10', 3],
	'gripper-stop'	: ['00', 3],
	'wrist-close'	: ['10', 2],
	'wrist-open'	: ['01', 2],
	'wrist-stop'	: ['00', 2],
	'elbow-close'	: ['10', 1],
	'elbow-open'	: ['01', 1],
	'elbow-stop'	: ['00', 1],
	'shoulder-close': ['10', 0],
	'shoulder-open'	: ['01', 0],
	'shoulder-stop' : ['00', 0]
}

app = Bottle()

@app.route('/')
def MoveArmInterface():

	if robo_arm is None: # in case the robotic arm hasn't been found through usb
		app_mode = "testing"
	else:
		app_mode = "live"

	# map the URL params and the appropriate movemap
	if request.params.get('command') in arm_interface_map:
		move_command = arm_interface_map[request.params.get('command')]
		# move_arm(get_command, app_mode)

		# calculate the correct full_command
		# update the usb_command_array with appropriate value for the command and the right place for it in the array
		usb_command_array[move_command[1]] = move_command[0];

		#build up the compiled array in parts so that it's readable
		compiled_command_arm = usb_command_array[0] + usb_command_array[1] + usb_command_array[2] + usb_command_array[3]
		compiled_command_base = usb_command_array[4] + usb_command_array[5] + usb_command_array[6] + usb_command_array[7]
		compiled_command_light = usb_command_array[8] + usb_command_array[9] + usb_command_array[10] + usb_command_array[11]

		# compose the command and represent the values as hex to send to the arm
		compiled_command = [hex(int(compiled_command_arm, 2)), hex(int(compiled_command_base, 2)), hex(int(compiled_command_light, 2))]

		# Function to start the movement
		if app_mode == "testing":

			# don't do the USB transfer
			print compiled_command

		elif app_mode == "live":

			# do the transfer
			# debugging - it seems like the compiled_command array comes across as strings, which don't work 
			print compiled_command
			print ''.join(compiled_command)
			print '[' + ', '.join(compiled_command) + ']'
			list_comp_commd = '[{0:x}, {1:x}, {2:x}]'.format(int(compiled_command[0], 16), int(compiled_command[1], 16), int(compiled_command[2], 16))
			print list_comp_commd
			new_list_commd = [int(compiled_command[0], 16), int(compiled_command[1], 16), int(compiled_command[2], 16)]
			print new_list_commd
			robo_arm.ctrl_transfer(0x40, 6, 0x100, 0, new_list_commd, 1000)

		return template('roboarm_adv_template', app_mode=app_mode, compiled_command=new_list_commd)

	else:
		# moverequest = movemap['light-on']
		# MoveArm(moverequest, Duration)

		# return template("Welcome to <br />The OWI-535 Robotic Arm control interface.<br />Moving: {{moveaction}}", moveaction=moverequest)

		# return '''
		# '''

		return template('roboarm_adv_template', app_mode="initialising", compiled_command="")

run(app, host='0.0.0.0', port=8080)


