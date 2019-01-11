<?php
    if($_SERVER['REQUEST_METHOD'] === 'POST'){
        if(isset($_POST["startscale"])){
            exec("rm /var/www/html/stop-script");
            $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            $message = "Running".$input;
        }else if($_POST["stopscale"]){
            $stopoutput = exec('touch /var/www/html/stop-script');
            $message = "Stopped".$input;
        }else if($_POST["resetscale"]){
            exec('touch /var/www/html/stop-script');
            sleep(2);
            exec("rm /var/www/html/stop-script");
            $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            $message = "Running".$input;

        }
    }

?>


<!DOCTYPE html>
<html lang="en">
<body>
<h1> Read Scale</h1>
    <form action="" method="POST">
        <h2><br>Status: <?php echo $message; ?></h2>
       <!----Box Quantity: <input type ="text" name = "boxQty"><br>
        Lot Number:<input type ="text" name = "lotNumber"><br>
        PONumber:<input type ="text" name = "PONumber"><br>
        SKU Number:<input type ="text" name = "sku"><br>-->
        <input type ="submit" name = "startscale" value = "Start"/><br>
        <input type ="submit" name = "stopscale" value = "Stop"/><br>
        <input type ="submit" name = "resetscale" value = "Reset"/><br>
    </form>

</body>
</html>