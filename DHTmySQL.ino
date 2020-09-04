#include <WiFi.h>
#include "DHT.h"
#define DHTPIN 19
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
//Definimos constantes a utilizar en el codigo
const char* ssid     = "HTROY 8612";
const char* password = "v-25963240";
//const char* host = "192.168.137.45";
const char* host="192.168.43.7";
const char* strurl ="/arduino/esp32/enviardatos.php";
IPAddress ip;
//en el setup definimos el puerto serial y la conexion wifi del esp32
void setup()
{
    Serial.begin(115200);
    Serial.println("DHT11 Output!");
    dht.begin();
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    ip=WiFi.localIP();
    Serial.println(ip);
}
//En el loop obtenemos la temperatura y la humedad determinadas por el sensor y lo enviamos como un string de datos a traves del metodo post
void loop()
{
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  if(isnan(temperature) || isnan(humidity)){
    Serial.println("Failed to read DHT11");
  }
  else{
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print(" %\t");
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" *C");
    delay(30000);
  }
  String datos= "&temperature=" + String(temperature,2) + "&humidity=" + String(humidity, 2);
  Serial.print("connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  // This will send the request to the server
  client.print(String("POST ") + strurl + " HTTP/1.1" + "\r\n" + 
               "Host: " + host + "\r\n" +
               "Connection: keep-alive" + "\r\n" + 
               "Content-Length: " + datos.length() + "\r\n" +
               "Cache-Control: max-age=0" + "\r\n" + 
               "Origin: http://"+ ip + "\r\n" + 
               "Upgrade-Insecure-Requests: 1" + "\r\n" + 
               "Content-Type: application/x-www-form-urlencoded" + "\r\n" + 
               "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36" + "\r\n" + 
               "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" + "\r\n" + 
               "Referer: http://192.168.137.45/arduino/esp32/formulario.html" + "\r\n" + 
               "Accept-Encoding: gzip, deflate" + "\r\n" + 
               "Accept-Language: es-419,es;q=0.8" + "\r\n" +           
               "\r\n" + datos);  
  /*client.print(String("POST /arduino/esp32/enviardatos.php?") + 
                          ("&temperature=") + temperature +
                          ("&humidity=") + humidity +
                          " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");*/
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 1000) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }

  // Read all the lines of the reply from server and print them to Serial
  while(client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line); 
  }
  Serial.println();
  Serial.println("closing connection");
}

  
