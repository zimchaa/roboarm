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
		app_mode = {{app_mode}} <br>
		compiled_command = {{compiled_command}} <br>

	    <table>
		    <tr>
			    <td colspan="2"><a href="/?command=gripper-open">Gripper Open</a></td>
			    <td colspan="2"><a href="/?command=gripper-close">Gripper Close</a></td>
		    </tr>
		    <tr>
			    <td rowspan="6"><a href="/?command=base-cw">Base CW</a></td>
			    <td colspan="2"><a href="/?command=wrist-open">Wrist Up</a></td>
			    <td rowspan="6"><a href="/?command=base-ccw">Base CCW</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=wrist-close">Wrist Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=elbow-open">Elbow Up</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=elbow-close">Elbow Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=shoulder-open">Shoulder Up</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=shoulder-close">Shoulder Down</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=light-on">Light On</a></td>
			    <td colspan="2"><a href="/?command=light-off">Light Off</a></td>
		    </tr>
	    </table>
	</body>
</html>
