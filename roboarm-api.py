# This is a rework of the RoboArm - Simple interface, allowing the motors to be run at the same time, and fully
# adopting the correct API, allowing for other operators to use it correctly, without sending invalid commands to the system.

# OWI-535 Robotic Arm - Advanced Web Interface and Controller / Python + Bottle

# imports
from bottle import Bottle, run, template, request, TEMPLATE_PATH
import usb.core, usb.util, time

ROBOARM = {
  "description": "OWI-535 Robotic Arm - USB Interface",
  "identification":{
    "description":"These are the parameters used to identify the RoboArm using the USB connection",
    "idVendor": 0x1267,
    "idProduct": 0x000
  },
  "initialisation":{
    "description": "These variables are used to transfer data on the created USB connection",
    "bmRequestType": 0x40,
    "bmRequest": 6,
    "wValue": 0x100,
    "wIndex": 0
  },
  "components": {
    "base": {
      "description": "The <ARM> components are mounted on this rotating base, with approx. 270deg freedom, clockwise and counterclockwise rotation is considered from the top of the RoboArm",
      "mask": 0b11111111,
      "features": {
        "all": {
          "description": "This is a pseudo-feature that allows for complex functions to be predescribed for the whole <ARM> component",
          "mask": 0b11111111,
          "verbs": {
            "stop": 0b00000000
          }
        },
        "direction": {
          "mask": 0b00000011,
          "verbs": {
            "ccw": 0b00000001,
            "cw": 0b00000010,
            "stop":0b00000000,
          }
        }
      }
    },
    "arm": {
      "description": "This component is mounted on the <BASE>, and replicates a typical human arm - with features, i.e. shoulder, elbow, wrist and a gripper.",
      "mask": 0b11111111,
      "features": {
        "all": {
          "description": "This is a pseudo-feature that allows for complex functions to be predescribed for the whole <ARM> component",
          "mask": 0b11111111,
          "verbs": {
            "wiggle":0b10101010,
            "wobble":0b01010101,
            "stop": 0b00000000
          }
        },
        "shoulder": {
          "description": "The first feature of the <ARM>, closest to the <BASE> offering 180deg of rotation, 0deg: parallel to <BASE>, 90deg: perpendicular",
          "mask": 0b11000000,
          "verbs": {
            "open": 0b01000000,
            "close": 0b10000000,
            "stop": 0b00000000
          }
        },
        "elbow": {
          "description":"",
          "mask": 0b00110000,
          "verbs": {
            "open": 0b00010000,
            "close": 0b00100000,
            "stop": 0b00000000
          }
        },
        "wrist": {
          "description":"",
          "mask": 0b00001100,
          "verbs": {
            "open": 0b00000100,
            "close": 0b00001000,
            "lift": 0b00000100,
            "stop": 0b00000000
          }
        },
        "grip": {
          "description":"",
          "mask": 0b00000011,
          "verbs": {
            "open": 0b00000001,
            "close": 0b00000010,
            "grab": 0b00000010,
            "drop": 0b00000001,
            "stop": 0b00000000,
            "pause": 0b00000000
          }
        },
      }
    },
    "light": {
      "description":"This is an LED mounted behind the <GRIP> feature on the <ARM> component - the focus of the light is useful to highlight where to grab, or that the system is in use",
      "mask": 0b11111111,
      "features": {
        "switch": {
          "description":"The only feature of the <LIGHT> is the <SWITCH>, simply flipping the last bit of the 3rd byte",
          "mask": 0b00000001,
          "verbs": {
            "on": 0b00000001,
            "spot": 0b00000001,
            "illuminate": 0b00000001,
            "stop": 0b00000000,
            "off": 0b00000000
          }
        }
      }
    }
  }
}

move_command = {"arm":0b00000000, "base":0b00000000, "light":0b00000000}

def change_move_command(update_move_command, roboarm_components_system, component, feature, verb):
  
  # check that the input is valid against the roboarm_components_system inputs
  input_exists = check_inputs(roboarm_components_system=, component, feature, verb)
  
  if input_exists[0]:
    # when receiving all valid inputs we should be cancelling out the current movement using the mask for the associated level (e.g. feature mask)
    # this is achieved through the the logical AND(&) with the logical NOT(~) of the mask
    update_move_command[component] = (update_move_command[component] & ~roboarm_components_system[component]["features"][feature]["mask"])
    # the return_move_command is further updated through the logical OR(|) with the desired movement - this leaves the existing values unchanged
    update_move_command[component] = (update_move_command[component] | roboarm_components_system[component]["features"][feature]["verbs"][verb])
  
  # calling the function just returns the updated dict {} and doesn't affect any data outside of the function, or use any data that is not passed in
  return update_move_command, input_exists
  
def check_inputs(roboarm_components_system, component, feature, verb):
  # print(component in roboarm_components_system.keys())
  component_exists = component in roboarm_components_system.keys()
  # print(feature in roboarm_components_system[component]["features"].keys())
  feature_exists = feature in roboarm_components_system[component]["features"].keys()
  # print(verb in roboarm_components_system[component]["features"][feature]["verbs"].keys())
  verb_exists = verb in roboarm_components_system[component]["features"][feature]["verbs"].keys()
  
  # return the complete list of the 
  return (component_exists & feature_exists & verb_exists), component_exists, feature_exists, verb_exists
	
def initialise_roboarm(vendor_id=ROBOARM["identification"]["idVendor"], product_id=ROBOARM["identification"]["idProduct"]):
  return usb.core.find(idVendor=vendor_id, idProduct=product_id)
  
def transfer_roboarm(move_command, ctrl_roboarm=ROBOARM["initialisation"], timeout=1000):
  if roboarm_device is None:
    roboarm_device = initialise_roboarm()
  
  transfer_stats = roboarm_device.ctrl_transfer(ctrl_roboarm["bmRequestType"], ctrl_roboarm["bmRequest"], ctrl_roboarm["wValue"], ctrl_roboarm["wIndex"], move_command, timeout)
  
  return transfer_stats

app = Bottle()

@app.route('/roboarm/<component>/<feature>/<verb>')
def move_roboarm(component, feature, verb):
  print("request: component={}, feature={}, verb={}".format(component, feature, verb))
  
  print("current move_command:{}".format(move_command))
  
  move_command = change_move_command(move_command, ROBOARM["components"], component, feature, verb)
  
  print("new move_command:{}".format(move_command))
  
  transfer_attempt = transfer_roboarm(move_command)
  
  print("transfer_attempt:{}".format(transfer_attempt))

# @app.route('/')
# def MoveArmInterface():
# 
# 	if robo_arm is None: # in case the robotic arm hasn't been found through usb
# 		app_mode = "testing"
# 	else:
# 		app_mode = "live"
# 
# 	# map the URL params and the appropriate movemap
# 	if request.params.get('command') in arm_interface_map:
# 		move_command = arm_interface_map[request.params.get('command')]
# 		# move_arm(get_command, app_mode)
# 
# 		# calculate the correct full_command
# 		# update the usb_command_array with appropriate value for the command and the right place for it in the array
# 		usb_command_array[move_command[1]] = move_command[0];
# 
# 		#build up the compiled array in parts so that it's readable
# 		compiled_command_arm = usb_command_array[0] + usb_command_array[1] + usb_command_array[2] + usb_command_array[3]
# 		compiled_command_base = usb_command_array[4] + usb_command_array[5] + usb_command_array[6] + usb_command_array[7]
# 		compiled_command_light = usb_command_array[8] + usb_command_array[9] + usb_command_array[10] + usb_command_array[11]
# 
# 		# compose the command and represent the values as hex to send to the arm
# 		compiled_command = [hex(int(compiled_command_arm, 2)), hex(int(compiled_command_base, 2)), hex(int(compiled_command_light, 2))]
# 
# 		# Function to start the movement
# 		if app_mode == "testing":
# 
# 			# don't do the USB transfer
# 			print compiled_command
# 
# 		elif app_mode == "live":
# 
# 			# do the transfer
# 			# debugging - it seems like the compiled_command array comes across as strings, which don't work 
# 			print compiled_command
# 			print ''.join(compiled_command)
# 			print '[' + ', '.join(compiled_command) + ']'
# 			list_comp_commd = '[{0:x}, {1:x}, {2:x}]'.format(int(compiled_command[0], 16), int(compiled_command[1], 16), int(compiled_command[2], 16))
# 			print list_comp_commd
# 			new_list_commd = [int(compiled_command[0], 16), int(compiled_command[1], 16), int(compiled_command[2], 16)]
# 			print new_list_commd
# 			robo_arm.ctrl_transfer(0x40, 6, 0x100, 0, new_list_commd, 1000)
# 
# 		return template('roboarm_adv_template', app_mode=app_mode, compiled_command=compiled_command)
# 
# 	else:
# 		# moverequest = movemap['light-on']
# 		# MoveArm(moverequest, Duration)
# 
# 		# return template("Welcome to <br />The OWI-535 Robotic Arm control interface.<br />Moving: {{moveaction}}", moveaction=moverequest)
# 
# 		# return '''
# 		# '''
# 
# 		return template('roboarm_adv_template', app_mode="initialising", compiled_command="")

run(app, host='0.0.0.0', port=8888)


