<?php
$conexion = mysql_connect("localhost", "root", "root");
mysql_select_db("ESP32", $conexion);
mysql_query("SET NAMES 'utf8'");

$chipid = $_POST ['chipid'];
$temperatura = $_POST ['temperatura'];

mysql_query("INSERT INTO `esp32`.`temperature` (`id`, `temperature`, `humidity`, `date`) VALUES (NULL, '$chipid', CURRENT_TIMESTAMP, '$temperatura');");

mysql_close();

echo "Datos ingresados correctamente.";
?>