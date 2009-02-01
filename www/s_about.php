<?php include ('config/config.php'); 


$q = "select * from about";
$result = mysql_query($q) or die("Query failed");
$row = mysql_fetch_array($result);
$h = $row["head"];
$t = $row["text"];

?>

<td><font face="Arial, Helvetica, sans-serif" size="3"><b><font color="#012748">
<?php echo "$h"; ?>

</font></b></font></td>
                          </tr>
                          <tr> 
                            <td> 
                              <p><font face="Arial, Helvetica, sans-serif" size="2" color="#012748">

<?php echo "$t"; ?>

</font></p>
                            </td>
