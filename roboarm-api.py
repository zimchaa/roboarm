# This is a rework of the RoboArm - Simple interface, allowing the motors to be run at the same time, and fully
# adopting the correct API, allowing for other operators to use it correctly, without sending invalid commands to the system.

# OWI-535 Robotic Arm - Advanced Web Interface and Controller / Python + Bottle

# imports
from bottle import Bottle, run, template, request, static_file
import usb.core, usb.util

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
  input_exists = check_inputs(roboarm_components_system, component, feature, verb)
  
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
  # attempt to initialise the device 
  roboarm_device = initialise_roboarm()
  
  # perform the actual USB transfer, returning the length of the transfer
  transfer_stats = roboarm_device.ctrl_transfer(ctrl_roboarm["bmRequestType"], ctrl_roboarm["bmRequest"], ctrl_roboarm["wValue"], ctrl_roboarm["wIndex"], [move_command[0]["arm"], move_command[0]["base"], move_command[0]["light"]], timeout)
  
  return transfer_stats

app = Bottle()

@app.route('/roboarm/<component>/<feature>/<verb>')
def move_roboarm(component, feature, verb, move_command=move_command):
  
  # print out the input parameters
  print("request: component={}, feature={}, verb={}".format(component, feature, verb))
  
  # print out the current move command
  print("current move_command:{}".format(move_command))
  
  # update the move_command dictionary
  move_command = change_move_command(move_command, ROBOARM["components"], component, feature, verb)
  
  # print out the updated move command
  print("new move_command:{}".format(move_command))
  
  # make the transfer
  transfer_attempt = transfer_roboarm(move_command)
  
  # print out the result
  print("transfer_attempt:{}".format(transfer_attempt))

  # return the current move command
  return move_command[0]

@app.route('/interface/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/home/pi/stuff/roboarm/interface')

run(app, host='0.0.0.0', port=8888)


