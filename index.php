<?php
    $myfile = fopen("/home/pi/scale/status", "r") or die("Unable to open file!");
    $message = fread($myfile,filesize("/home/pi/scale/status"));
    fclose($myfile);
?>


<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="refresh" content="10">
<link rel="stylesheet" type="text/css" href="sytle.css">
</head>
<body>
<h1> Read Scale</h1>
    <form action="submit.php" method="POST">
        <h2><br>Status: <?php echo $message; ?></h2>
        <input type ="submit" name = "startscale" value = "Start"/><br>
        <input type ="submit" name = "stopscale" value = "Stop"/><br>
        <input type ="submit" name = "resetscale" value = "Reset"/><br>
    </form>
</body>
</html>