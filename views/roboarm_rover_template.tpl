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

		td a {
			display: block;
			width: 100%;
			height: 30px;
		}
	</style>

	</head>

	<body>
		app_mode = {{app_mode}} <br>
		compiled_command = {{compiled_command}} <br>

	    <table>
		    <tr>
			    <td colspan="1"><a href="/?command=gripper-open">Gripper Open</a></td>
				<td colspan="2"><a href="/?command=gripper-stop">Gripper Stop</a></td>
			    <td colspan="1"><a href="/?command=gripper-close">Gripper Close</a></td>
		    </tr>
		    <tr>
			    <td rowspan="5"><a href="/?command=shoulder-close">LTrack Go</a></td>
				<td rowspan="2"><a href="/?command=wrist-stop">Stop</a></td>
			    <td colspan="1"><a href="/?command=wrist-open">Wrist Open</a></td>
			    <td rowspan="5"><a href="/?command=base-cw">RTrack Go</a></td>
		    </tr>
		    <tr>
			    <td colspan="1"><a href="/?command=wrist-close">Wrist Close</a></td>
		    </tr>
		    <tr>
				<td rowspan="2"><a href="/?command=elbow-stop">Stop</a></td>
			    <td colspan="1"><a href="/?command=elbow-open">Elbow Open</a></td>
		    </tr>
		    <tr>
			    <td colspan="1"><a href="/?command=elbow-close">Elbow Close</a></td>
		    </tr>
		    <tr>
				<td rowspan="2"><a href="/?command=shoulder-stop">LTrack Stop</a></td>
			    <td rowspan="2"><a href="/?command=base-stop">RTrack Stop</a></td>
		    </tr>
		    <tr>
				<td rowspan="1"><a href="/?command=shoulder-open">LTrack Back</a></td>
				<td rowspan="1"><a href="/?command=base-ccw">RTrack Back</a></td>
		    </tr>
		    <tr>
			    <td colspan="2"><a href="/?command=light-on">Light On</a></td>
			    <td colspan="2"><a href="/?command=light-off">Light Off</a></td>
		    </tr>
	    </table>
	</body>
</html>
