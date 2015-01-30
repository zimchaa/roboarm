# roboarm
Code for interfacing and notes about the OWI-535 Robotic Arm

## roboarm-simple.py
Really simple approach to creating a web interface to control the arm remotely. The single file will run whereever you have and open up a website on port 8080 that you can access directly from any device. 

The table layout that is shown represents the layout of the actual arm in the simplest way - note, each activation in this simple interface ends any current action and lasts 1 second.

Table: 

| Gripper Open |            | Gripper Close |
|:------------:|:----------:|:-------------:|
|              |  Wrist Up  |               |
|              | Wrist Down |               |
| Base         |  Elbow Up  |          Base |
| CCW          | Elbow Down |            CW |
|              |  Shld. Up  |               |
|              | Shld. Down |               |
|   Light On   |            |   Light Off   |
