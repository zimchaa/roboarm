# roboarm
Code for interfacing and notes about the OWI-535 Robotic Arm

## roboarm-simple.py
Really simple approach to creating a web interface to control the arm remotely. The single file will run whereever you have and open up a website on port 8080 that you can access directly from any device. 

The table layout that is shown represents the layout of the actual arm in the simplest way - note, each activation in this simple interface ends any current action and lasts 1 second.

### Interface 
Visit http://<your-ip>:8080 and the table should be displayed. Confirmed working with Raspberry Pi (Server) and iPhone (client).

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
> pip install pyusb
> pip install bottle
> python roboarm-simple.py
```
### Thanks
@lizquilty - code from this implementation that is a direct copy of code from this system: https://github.com/lizquilty/roboticarm - full explanation of what is happening within the code.
