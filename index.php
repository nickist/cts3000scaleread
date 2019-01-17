<?php
    $myfile = fopen("/home/pi/scale/status", "r") or die("Unable to open file!");
    $message = fread($myfile,filesize("/home/pi/scale/status"));
    fclose($myfile);
    if($message == "Running"){
        $color = '#008000';
    }else if ($message == "Error" || $message == "Stopped" || $message == "Error"){
        $color = '#FF0000';
    }

?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="refresh" content="5">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div class="wrapper">
<h1> Read Scale</h1>
    <form action="submit.php" method="POST">
        <h2><br>Status: <?php echo "<span style=\"color: $color\">$message</span>";  ?></h2>
        <div class="start"><input type ="submit" name = "startscale" value = "Start"/></div><br>
        <div class="stop"><input type ="submit" name = "stopscale" value = "Stop"/></div><br>
        <div class="reset"><input type ="submit" name = "resetscale" value = "Reset"/></div><br>
    </form>
</div>
</body>
</html>

