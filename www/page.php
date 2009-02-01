<?php

include ('config/config.php'); 

$q = "SELECT `name`, `body`, `slug` FROM `price_pages` WHERE `slug` = '$slug';";
$result = mysql_query($q) or die("Query failed");
$row = mysql_fetch_array($result);
$name = $row["name"];
$body = $row["body"];

print" <h2>  $name </h2>
<p>
 $body
</p>";
?>

