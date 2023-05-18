# tesis
This was my final project in order to get my bachelor of science degree in electronics engineering at the Universidad Simón Bolívar.

The project consisted of developing a data acquisition system, that was capable of measuring variables from an industrial engine, storing them in a database
and then showing graphs with the values in real time trough an application.

The microcontroller used is an esp32 from Espressif Systems, and its code was written with Arduino.
The backend is written with PHP and connects the information sent by the microcontroller with the SQL database, hosted in phpMyAdmin.
The desktop app was written in Python, using the library pyQT for the user interface and matplotlib for the graphs.It updates the graph every fixed amount of seconds
with the new entries written into the database. It also has the option to export this data into an CSV file so it can be further processed and analyzed.
