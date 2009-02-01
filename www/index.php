<?php

include ("a_top.php");
include ("b_topmenu.php");
include ("c_menu.php");

include ("r_top.php");

$a = $_GET["a"];
$type = $_GET["type"];
$id = $_GET["id"];
$slug = $_GET["slug"];
switch ($a):
  case("s_mebel"):
    include ("$a.php");
  break;

  case("s_about"):
    include ("$a.php");
  break;

  case("s_head"):
    include ("$a.php");
  break;

  case("page"):
    include ("$a.php");
  break;

  case("s_clients"):
    include ("$a.php");
  break;

  #case("s_contacts"):
  #  include ("$a.php");
  #break;

  default:
    include ("s_news.php");
  break;

endswitch;





include ("r_down.php");


include ("z_bottom.php");

?>
