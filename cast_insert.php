<?php
include "config.php";
include "util.php";

$connect = dbconnect($host, $dbid, $dbpass, $dbname);


$private_key = $_POST['input_id'];
$candidate = $_POST['input_ca']; //candidate는 "1", "2" 이런식


$result = mysql_query("select public_key from candidate LIMIT $candidate,1");
$candidate_public = mysql_fetch_array($result);

$myfile = fopen("ballot.txt", "w") or die("Unable to open file!");

fwrite($myfile, $private_key);
fwrite($myfile, "\n");
fwrite($myfile, $candidate_public[0]);

fclose($myfile);


exec('python3 web_vote.py');

sleep(2);


$file = fopen("log.txt", "r") or exit("unable to open file");

$validate = fgets($file);

fclose($file);

// 만약에 0이면
if ($validate == "0\n") {
    msg("error!");
} else {


//	$query = "insert into ballot (voter, candidate) values ('$id','$candidate_public[0]')";
//	$result = mysql_query($query, $connect);


    echo "<meta http-equiv='refresh' content='0;url=display.php'>";
}


mysql_close($connect);
?>