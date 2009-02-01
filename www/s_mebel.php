<?php
ini_set('display_errors',1);
error_reporting(E_ALL ^E_NOTICE);

include ("config/config.php");
#$q = "SELECT * FROM mebel where type='$type' ORDER BY position + 0";
$q_0 = mysql_query( " SELECT * FROM `price_category` WHERE `price_category`.`slug` = '$type';" ) or die('Nyaaa =(');
$category = mysql_fetch_assoc( $q_0 );
$c_id = $category["id"];
$q = "SELECT
            `price_price`.`name` AS `name_pr`,
            `price_price`.`desc`, 
            `price_price`.`img_url`, 
            `price_price`.`thumb_img_url`, 
            `price_manufacturer`.`name` AS `manuf`, 
            `price_type`.`name` AS `type_product`, 
            `price_price`.`cell`, 
            `price_valyuta`.`desc` AS `val`
            FROM 
            `polytechnik_django`.`price_price` AS `price_price`, 
            `polytechnik_django`.`price_valyuta` AS `price_valyuta`, 
            `polytechnik_django`.`price_manufacturer` AS `price_manufacturer`, 
            `polytechnik_django`.`price_type` AS `price_type`, 
            `polytechnik_django`.`price_category` AS `price_category` 
            WHERE 
            `price_price`.`valyuta_id` = `price_valyuta`.`id` 
            AND `price_price`.`manufacturer_id` = `price_manufacturer`.`id` 
            AND `price_price`.`type_product_id` = `price_type`.`id` 
            AND `price_price`.`category_id` = `price_category`.`id`
            AND `price_category`.`id` = '$c_id'
            ORDER BY 
            `price_manufacturer`.`name` DESC,
            `price_type`.`name` DESC,
            `price_price`.`cell` ASC;";
$result = mysql_query($q) or die("Query failed");

if ( $category  ) {
#var_dump($category);
    $c_name = $category["name"];
    $c_desc = nl2br($category["desc"]);
    $c_img_url = $category["img_url"];
    $c_img = "<img src='$c_img_url' alt='' />";
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='_b3'>
       <b> $c_name </b>
      </td>
    </tr>
    ";
    if ( $c_img_url) { 
            print "
    <tr bgcolor='e2e2ed'> 
      <TD>$c_img</TD>
      <TD colspan='2' width='66%'>$c_desc</TD>
      </tr>";
    } elseif ( $category["desc"] ) {
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='_b3'>
       $c_desc
      </td>
      </tr>"; } ;
};
$type_product = "";
$manuf = "";
for ($i=0;$i<mysql_numrows($result);$i++):

  $row = mysql_fetch_assoc($result);
#var_dump($row);


    $a = $row["name_pr"];
    $b = $row["desc"];
    $c = $row["cell"];
    $val =  $row["val"];
    $img_url = $row["img_url"];

    if ($img_url) {
    $thumb_img_url = $row["thumb_img_url"];
    #$img = "<a href='$img_url' ><img src='$thumb_img_url' alt='$a' width='100'/></a>";
    $img = "<img src='$thumb_img_url' alt='$a' width='100'/>";
    $class = "foto";
    
    } 
    else { 
        $img = "";
        $class = "text";
    };

    if ( $manuf != $row["manuf"] ) {
        #$a = $row["manuf"];
        $manuf = $row["manuf"];
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='_b3'>
        <b>$manuf</b>
      </td>
    </tr>
    ";
    };
    if ( $row["type_product"] != "NULL" ){
        if ( $type_product != $row["type_product"]) 
        {
            $type_product = $row["type_product"];
        print "
        <tr> 
          <td colspan='3' bgcolor='#e2e2ed' class='_b3'>
            <b>$type_product</b>
          </td>
        </tr>
        ";
        };
    };


  #$a = $row["0"];
  #$b = $row["2"];
  #if ($b == '') {$b="&nbsp";}
  #$c = $row["c"];
  #$id = $row["id"];
  #$val = $row["valyuta"];

  #$a=ereg_replace("\n", "<br/>", $a);
  #$b=ereg_replace("\n", "<br/>", $b);
  #$c=ereg_replace("\n", "<br/>", $c);

  if ($class == 'head'):
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='b3'>
        $a
      </td>
    </tr>
    ";
  endif;

  if ($class == 'text'):
    print "
    <tr bgcolor='e2e2ed'> 
    <td width='33%' class='b3'>  
        $a
      </td>

      <td width='33%'>
        $b
      </td>

      <td width='33%'>
        $c $val
      </td>

    </tr>

    ";
  endif;

  if ($class == 'foto'):
    print "
    
    <tr bgcolor='e2e2ed' width='33%'> 
      <td width='200'> 
        <div align='center'>$img</div>
      </td>
      
      <td width='33%'>
        <span class='b3'>$a</span><br/>
        $b
      </td>
  
      <td width='33%'>
        $c $val
      </td>

    ";
  endif;


  if ($class == 'single'):
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='osnova'>
        $a
      </td>
    </tr>
    ";
  endif;

  if ($class == 'link'):
    print "
    <tr> 
      <td colspan='3' bgcolor='#e2e2ed' class='osnova'>
        <a href='$b'>$a</a>
      </td>
    </tr>
    ";
  endif;



  if ($class == 't7030'):
    print "
    <tr bgcolor='e2e2ed'> 
      <TD colspan='2' width='66%'>$a</TD>
      <TD>$b</TD>
    </tr>

    ";
  endif;


  if ($class == 't3070'):
    print "
    <tr bgcolor='e2e2ed'> 
      <TD>$a</TD>
      <TD colspan='2' width='66%'>$b</TD>
    </tr>

    ";
  endif;




  if ($class == 'fototext'):

    $fotka = "img-mebel/$id";
    if (!file_exists($fotka))
      {
      $fotka = "img-mebel/no";
      } 
    $size = GetImageSize($fotka);
    $width = $size[0];
    $height = $size[1];

    print "
    
    <tr bgcolor='e2e2ed' width='33%'> 
      <td width='200'> 
        <div align='center'><img src='$fotka' width='$width' height='$height' border='1'></div>
      </td>
      
      <td colspan='2'>
        $a
      </td>

    ";
  endif;



  if ($class == 'pic'):

    $pic1 = "img-mebel/$id"."a";
    $pic2 = "img-mebel/$id"."b";
    $pic3 = "img-mebel/$id"."c";

    if (!file_exists($pic1))
      {
      $fotka = "img-mebel/no";
      } 

    if (!file_exists($pic2))
      {
      $fotka = "img-mebel/no";
      } 

    if (!file_exists($pic3))
      {
      $fotka = "img-mebel/no";
      } 


    print "
    
    <tr bgcolor='e2e2ed'> 
      <td width='33%'>  
        <div align='center'><img src='$pic1' border='1'></div>
      </td>
      
      <td width='33%'>
        <div align='center'><img src='$pic2' border='1'></div>
      </td>

      <td width='33%'>
        <div align='center'><img src='$pic3' border='1'></div>  
      </td>

    ";
  endif;



endfor;


?>
    <tr bgcolor='e2e2ed'> 
      <td width='33%'> </td>
      <td width='33%'> </td>
      <td width='33%'> </td>
