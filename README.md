# roboarm
Code for interfacing and notes about the OWI-535 Robotic Arm

## roboarm-simple.py
Really simple approach to creating a web interface to control the arm remotely. The single file will run whereever you have and open up a website on port 8080 that you can access directly from any device. 

The table layout that is shown represents the layout of the actual arm in the simplest way - note, each activation in this simple interface ends any current action and lasts 1 second.

### Interface 
Visit http://\<your-ip\>:8080 and the table should be displayed. Confirmed working with Raspberry Pi (Server) and iPhone (client).

| Gripper Open |            | Gripper Close |
|:------------:|:----------:|:-------------:|
|              |  Wrist Up  |               |
|              | Wrist Down |               |
| Base         |  Elbow Up  |          Base |
| CCW          | Elbow Down |            CW |
|              |  Shld. Up  |               |
|              | Shld. Down |               |
|   Light On   |            |   Light Off   |

### Preparation 
You will need Python Bottle to get this working, but nothing else - it uses the reference Web Server included, but seems easy to change out for something else (see Bottle documentation: http://bottlepy.org/docs/dev/deployment.html). This works on the latest Raspbian on Raspberry Pi.

```
> sudo pip install --pre pyusb
> sudo pip install bottle
> sudo python roboarm-simple.py
```
#### PyUSB problems
See here for some further information:
http://raspberrypi.stackexchange.com/questions/6774/installed-pyusb-still-importerror-no-module-named-core

http://stackoverflow.com/questions/22049399/how-to-install-pyusb-on-ubuntu

### Thanks
@lizquilty - code from this implementation that is a direct copy of code from this system: https://github.com/lizquilty/roboticarm - full explanation of what is happening within the code.

## roboarm-rest.py
This will be a more complex integration with the USB controller of the Robotic Arm - it will essentially allow for the system to run more that 1 motor at a time and will build on the roboarm-simple.py in two ways to achieve this: *Updated interface* and *Protocol logic enhancement*.

### Web Interface
Todo: design RESTful interface to work with the on-off control provided by the new protocol logic.

### Protocol Logic
Using the logic below, as found by @notbrainsurgery here: http://notbrainsurgery.livejournal.com/38622.html we can drive the motors independantly to create a more fully functional arm.

#### USB Interface
From the site above, 
> The device is controlled by 3 byte commands sent via USB control transfers. Command format is byte0, byte1, byte2. Each byte controls a group of arm features. All motors could be controlled independently. Most commands start action which is continued until next action is signalled. Byte '00' universally used as stop action.

##### Byte 0
This table helps represent the calculations requried for the first byte of the 3, this controls the main functions of the Arm Actuators:
- Shoulder (SH), 
- Elbow (EL), 
- Wrist (WR) and 
- Gripper (GR)

and Actions: 
- UP (Clockwise when viewed from the side), 
- DW (Down, Counter-Clockwise), 
- OP (Open, increase the width between the grippers), 
- CL (Close, decrease the width)

| Bit Number | Controls        | All Stop | GR CL | GR OP | All UP | All DW | GR CL / EL UP | GR OP / SH DW | EL DW / WR UP / GR OP | Invalid |
|------------|-----------------|----------|-------|-------|--------|--------|---------------|---------------|-----------------------|---------|
| 7          | Shoulder: SH DW | 0        | 0     | 0     | 1      | 0      | 0             | 1             | 0                     | 1       |
| 6          | SH UP           | 0        | 0     | 0     | 0      | 1      | 0             | 0             | 0                     | 1       |
| 5          | Elbow: EL DW    | 0        | 0     | 0     | 1      | 0      | 0             | 0             | 1                     | 0       |
| 4          | EL UP           | 0        | 0     | 0     | 0      | 1      | 1             | 0             | 0                     | 0       |
| 3          | Wrist: WR DW    | 0        | 0     | 0     | 1      | 0      | 0             | 0             | 0                     | 0       |
| 2          | WR UP           | 0        | 0     | 0     | 0      | 1      | 0             | 0             | 1                     | 0       |
| 1          | Gripper: GR OP  | 0        | 0     | 1     | 1      | 0      | 0             | 0             | 1                     | 0       |
| 0          | GR CL           | 0        | 1     | 0     | 0      | 1      | 1             | 1             | 0                     | 0       |
| Byte HEX   |                 | 00       | 01    | 02    | AA     | 55     | 11            | 81            | 26                    |         |

#### Byte 1
This byte controls the Base (BS), turning the arm either 
- CCW (Counter-clockwise when viewed from the side) or 
- CW (Clockwise)

| Bit Number | Controls     | BS CCW | BS CW | BS Stop |
|------------|--------------|--------|-------|---------|
| 7          |              |        |       |         |
| 6          |              |        |       |         |
| 5          |              |        |       |         |
| 4          |              |        |       |         |
| 3          |              |        |       |         |
| 2          |              |        |       |         |
| 1          | Base: BS CCW | 1      | 0     | 0       |
| 0          | BS CW        | 0      | 1     | 0       |
| Byte HEX   |              | 02     | 01    | 00      |

#### Byte 2
This byte controls the Light (LED) mounted behind the Gripper than can be useful for targetting:
- ON 
- OFF

| Bit Number | Controls      | LED ON | LED OFF |
|------------|---------------|--------|---------|
| 7          |               |        |         |
| 6          |               |        |         |
| 5          |               |        |         |
| 4          |               |        |         |
| 3          |               |        |         |
| 2          |               |        |         |
| 1          |               |        |         |
| 0          | Light: LED ON | 1      | 0       |
| Byte HEX   |               | 01     | 00      |




