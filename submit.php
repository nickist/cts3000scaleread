<?php   
    header('Content-Type: text/event-stream');
    header('Cache-Control: no-cache');
    ///home/pi/scale/status
    $path = "/home/nick/Desktop/status";
    $myfile = fopen($path, "r") or die("Unable to open file!");
    $message = fread($myfile,filesize("$path"));
    fclose($myfile);

    echo "data: {$message}";   

       if($_SERVER['REQUEST_METHOD'] === 'POST'){
        if(isset($_POST["startscale"])){
             exec('/home/pi/scale/checkRunningProcess.sh readScale.py', $isrunning);
            if($isrunning[0] == 'Running'){
                echo $isrunning[0];
            }else {
                exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            }
        }else if($_POST["stopscale"]){
             exec('touch /var/www/html/stop-script');
        }else if($_POST["resetscale"]){
            exec('/home/pi/scale/checkRunningProcess.sh readScale.py', $isrunning);
            if($isrunning[0] == 'Running'){
                exec('touch /var/www/html/stop-script');
                sleep(2);
                exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            }else {
                exec("/home/pi/scale/bin/python /home/pi/scale/readScale.py> /dev/null 2>&1 & echo $!; ", $output);
            }
        }
    }
    flush();
?>
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
<h1><a href="http://scalereader.local">go Back</a></h1>
</body>
</html>

