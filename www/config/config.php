<?php
ini_set('display_errors',1);
error_reporting(E_ALL);

$host = "localhost";
$base = "polytechnik_django";
$user = "polytechnik";
$pass = "nya";

$link = mysql_pconnect($host, $user, $pass) or die ("Could not connect");
mysql_select_db($base, $link) or die("Can't connect to DB");
mysql_query("SET NAMES UTF8");


?>
