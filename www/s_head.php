<?php

include ("config/config.php");

$q_1 = "SELECT name, body, img_url_1, img_url_2 FROM `price_pages` WHERE `price_pages`.`slug` = '$id';";
$result_1 = mysql_query($q_1) or die("Query failed");
$row_1 = mysql_fetch_assoc($result_1);

$q_2 = "SELECT id FROM price_category WHERE `price_category`.`slug` = '$id';";
$result_2 = mysql_query($q_2);

$parent_category_id = mysql_fetch_assoc( $result_2);
$par_id = $parent_category_id["id"];
#var_dump($row_1);
#var_dump($parent_category_id);

$q_3 = "SELECT `price_category`.`id`, `price_category`.`name`, `price_category`.`slug`, `price_category`.`parent_id` FROM `price_category` WHERE `price_category`.`parent_id` = '$par_id'";

$result_3 = mysql_query($q_3);

#var_dump($row_3);

$name = $row_1["name"];
$body = $row_1["body"];
$img_url_1 = $row_1["img_url_1"];
$img_url_2 = $row_1["img_url_2"];

?>



<td colspan="3" bgcolor="#e2e2ed"><font face="Arial, Helvetica, sans-serif" size="3"><b>
                              <?php echo $name ?></b></font></td>
                          </tr>
                          <tr bgcolor="e2e2ed"> 
                            <td width="200"> 
                              <div align="center"><img src="<?php echo $img_url_1 ?>" width='198' border="1"></div>
                            </td>
                            <td><font face="Arial, Helvetica, sans-serif" size="2">
                              <?php echo $body ?>
                              </font></td>
                            <td width="200"><img src="<?php echo $img_url_2 ?>" width='198' border="1"></td>

                          </tr>
<tr><td colspan=3>
<?php 
while ( $row_3 = mysql_fetch_assoc($result_3) )
{
    #var_dump($row_3);
    $c_name = $row_3["name"];
    $c_slug = $row_3["slug"];
    print "<p>$c_name <a href='?a=s_mebel&amp;type=$c_slug'>&gt;&gt;</a></p>";
}

?>
</td>
