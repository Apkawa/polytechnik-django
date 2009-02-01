                        <table>
                          <tr>
                            <td bgcolor="#e2e2ed"><font face="Arial, Helvetica, sans-serif" size="3"><b>Новости</b></font></td>
                          </tr>
                        </table>


<?php

include ('config/config.php'); 

#$q = "SELECT * FROM news ORDER BY -data";
$q = "SELECT `head`, `body`, `date` FROM `price_news` ORDER BY `date` DESC";
$result = mysql_query($q) or die("Query failed");

for ($i=0;$i<mysql_numrows($result);$i++)
{

$row = mysql_fetch_array($result);
$d = $row["date"];
$h = $row["head"];
$n = $row["body"];
$n=ereg_replace("\\\\", "<br>", $n);

print "  <table width='100%' border='0' cellspacing='1' cellpadding='0' bgcolor='#2F5170'>
                          <tr> 
                            <td bgcolor='#e2e2ed'> 
                              <table width='100%' border='0' cellspacing='0' cellpadding='5'>
                                <tr bgcolor='#85AFD6'> 
                                  <td width='50%' bgcolor='#85AFD6'><font face='Arial, Helvetica, sans-serif' size='2'><b><font color='#FFFFFF'>$h</font></b></font></td>
                                  <td width='50%'> 
                                    <div align='right'><font face='Arial, Helvetica, sans-serif' size='2'><font color='#FFFFFF'>$d</font></font></div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                          <tr> 
                            <td bgcolor='#e2e2ed'> 
                              <table width='100%' border='0' cellspacing='0' cellpadding='5'>
                                <tr valign=top> 
                                  <td  width='16%'> 
                                    <div align='center'><img src='images/polylogo.jpg' width='100' height='100' border='1'></div>
                                  </td>
                                  <td width='84%'><font face='Arial, Helvetica, sans-serif' size='2'>
				   $n
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </table>  &nbsp";


}



?>
