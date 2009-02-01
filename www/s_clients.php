<?php include ('config/config.php'); ?>
                            <td colspan="3" bgcolor="#e2e2ed"><font face="Arial, Helvetica, sans-serif" size="3"><b><font color="#012748">Наши 
                              клиенты </font></b></font></td>
                          </tr>
                          <tr> 
                            <td colspan="3" bgcolor="#e2e2ed"><font face="Arial, Helvetica, sans-serif" size="2" color="#012748"> 
В Санкт-Петербурге, Ленинградской области, более чем в 50 городах России нашими клиентами стали тысячи учебных организаций различного профиля и статуса. Это школы, лицеи, гимназии, училища, колледжи, детские дошкольные учреждения, учреждения дополнительного образования, высшие учебные заведения, военные и медицинские учебные организации, другие учреждения повышения профессиональной квалификации различного профиля. Из наиболее известных - это:                             

  
                            </font></td>
                          </tr>

<?php

$q = "SELECT * FROM `price_clients`";
$result = mysql_query($q) or die("Query failed");


while ($row = mysql_fetch_array($result))
{
$clients = $row["name"];

print "
                          <tr> 
                            <td colspan='3' bgcolor='#e2e2ed'><b><font face='Arial, Helvetica, sans-serif' size='2'> 
                              <li><font color='#0158A6'>$clients</font> 
                              </font></b></td>
                          </tr>
";

}



?>
