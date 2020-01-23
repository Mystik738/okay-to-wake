<?php 

$time = date_create_from_format('H:i', $_REQUEST['time']);
$schedule = json_decode($_REQUEST['schedule'], true);

$action = $_REQUEST['action'];
$now = new DateTime();

if(file_exists('time.txt')) {
    $cur_data = json_decode(file_get_contents('time.txt'), true);
    $oldtime = new DateTime($cur_data['time']);
    if(empty($schedule)) {
        $schedule = $cur_data['schedule'];
    }
} else {
    $oldtime = $now;
    $oldtime->modify('-1 day');
    $cur_data = array(
        'use_schedule' => false,
        'time' => $oldtime->format('Y-m-d H:i:s'),
        'schedule' => array(),
    );
}

//If we have a time set, set the time
if($action == 't') {  
    $cur_data['use_schedule'] = false;
    if(!empty($time)) {
        //If the time is less than right now, set the time for tomorrow
        if($time < $now) {
            $time->modify('+1 day');
        }
        $cur_data['time'] = $time->format('Y-m-d H:i:s');
    } else {
        $cur_data['time'] = $oldtime->format('Y-m-d H:i:s');
        $time = $oldtime;
    }
} else if($action == 's') {
    $time = $oldtime;
    $cur_data['use_schedule'] = true;
    $cur_data['schedule'] = $schedule;
} else if(!empty($action)) {
    $cur_data['use_schedule'] = false;
    //If the time isn't currently set, set it
    if($oldtime < $now) {
        $time = $now;
    } else {
        $time = $oldtime;
    }
    
    //If we need to reset the clock, set the time to now
    if($action == 'r') {
        $time = $now;
    } else if($action == 'm') { //If the action is to set minutes, add minutes
        $time->modify('+15 minute');
    } else { //Else add an hour
        $time->modify('+1 hour');
    }
    
    $cur_data['time'] = $time->format('Y-m-d H:i:s');
}

//Write the time to a file
$fh = fopen('time.txt', 'w');    
fwrite($fh, json_encode($cur_data));    
fclose($fh);

?>

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Okay to Wait</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
  <div class="containter" style="text-align:center">
    <br />
    <div class="jumbotron">
      <h2>
      <?php 
if($cur_data['use_schedule']) {
    echo "Using Schedule";
} else if(!empty($action)) {
    echo 'Alarm set to<br/>'.$time->format('M j, h:i A');
} else {
    echo 'Alarm currently<br/>'.$oldtime->format('M j, h:i A');
}

?> 
      </h2>
    </div>
    <form class="inline-form" role="form" method="post">
        <br/>       
        <button type="submit" name="action" value="r" class="btn btn-primary">Reset</button><br/><br/>
        <button type="submit" name="action" value="m" class="btn btn-primary">Set/Add 15m</button><br/><br/>
        <button type="submit" name="action" value="h" class="btn btn-primary">Set/Add 1h</button><br/><br/>
        <input type="time" name="time" value="" style="width:135px;"><br/><br/>
        <button type="submit" name="action" value="t" class="btn btn-primary">Set time</button><br/><br/>
        Use a schedule instead: <br/><br/>
        <textarea name="schedule" cols=30 rows=4><?php echo json_encode($cur_data['schedule']);?></textarea><br/><br/>
        <button type="submit" name="action" value="s" class="btn btn-primary">Set schedule</button><br/><br/>
    </form>
    </div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
  </body>
</html>
