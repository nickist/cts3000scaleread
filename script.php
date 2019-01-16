<?php
    if($_SERVER['REQUEST_METHOD'] === 'POST'){
        if(isset($_POST["startscale"])){
            exec('touch /var/www/html/stop-script');
            sleep(2);
            $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
        }else if($_POST["stopscale"]){
             $stopoutput = exec('touch /var/www/html/stop-script');
        }else if($_POST["resetscale"]){
            exec('touch /var/www/html/stop-script');
            sleep(2);
            $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);

        }
    }

?>
