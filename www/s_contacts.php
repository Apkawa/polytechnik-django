<?php

include ('config/config.php'); 

$q = "SELECT name, body FROM `price_page` WHERE slug=$page";
$result = mysql_query($q) or die("Query failed");
$row = mysql_fetch_array($result);
$post = $row["post"];
$adr = $row["adr"];
$tel = $row["tel"];
$fax = $row["fax"];
$email = $row["email"];
$www = $row["www"];


?>
                            <td width="42%"><font face="Arial, Helvetica, sans-serif" size="3"><b><font color="#012748">Контактная 
                              информация: </font></b></font> </td>
                            <td width="58%">&nbsp;</td>
                          </tr>
                          <tr vAlign=top>
                            <td width="42%"> 
                              <table width="100%" border="0" cellspacing="0" cellpadding="5">
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">Почтовый 
                                    адрес:</font></b><font color="#012748"><? echo $post  ?></font></font></td>
                                </tr>
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">Адрес:</font></b><font color="#012748"> 
                                    <? echo $adr  ?></font></font></td>
                                </tr>
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">тел:</font></b><font color="#012748"> 
                                    <? echo $tel  ?></font></font></td>
                                </tr>
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">тел/факс:</font></b><font color="#012748"> 
                                    <? echo $fax ?></font></font></td>
                                </tr>
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">E-mail:</font></b> 
                                    <font color="#012748"><a href="mailto:<? echo $email ?>"><? echo $email ?></a></font></font></td>
                                </tr>
                                <tr> 
                                  <td><font face="Arial, Helvetica, sans-serif" size="2"><b><font color="#0158A6">Интернет:</font></b> 
                                    <font color="#012748"><a href="<? echo $www ?>"><? echo $www ?></a></font></font></td>
                                </tr>
                              </table>
                            </td>
                            <td width="58%"><img src="images/karta.gif" width="410" height="490" border="1"></td>
