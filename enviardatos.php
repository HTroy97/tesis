<?php
//Codigo PHP para enviar datos a phpMyAdmin
$link = mysqli_connect("localhost", "root", "", "esp32");
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
//Determina Temperatura y Humedad enviadas por ESP32
if (isset($_POST['temperature']))
{
    $temperature = floatval($_POST['temperature']);}
if (isset($_POST['humidity']))
    {
    $humidity = floatval($_POST['humidity']); 
}
// Attempt insert query execution
$sql = "INSERT INTO temperature (id, temperature, humidity, date) VALUES (NULL, '$temperature', '$humidity', current_timestamp())";
if(mysqli_query($link, $sql)){
    echo "Records inserted successfully.";
} else{
    echo "ERROR: Could not able to execute $sql. " . mysqli_error($link);
}
 
// Close connection
mysqli_close($link);
?>