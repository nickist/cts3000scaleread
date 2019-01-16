<?php   
       if($_SERVER['REQUEST_METHOD'] === 'POST'){
        if(isset($_POST["startscale"])){
            $isrunning = exec('/home/pi/scale/checkRunningProcess.sh readScale.py');
            if($isrunning == 'Running'){
                echo $isrunning;
            }else {
                $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            }
        }else if($_POST["stopscale"]){
             $stopoutput = exec('touch /var/www/html/stop-script');
        }else if($_POST["resetscale"]){
            exec('touch /var/www/html/stop-script');
            sleep(2);
            $pid = exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
        }
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
<a href="http://scalereader.local">go Back</a>

</body>
</html>