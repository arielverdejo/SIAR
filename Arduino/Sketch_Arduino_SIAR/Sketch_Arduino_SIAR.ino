
/**
 * @file a_wild_card.ino
 * @copyright (c) 2013-2020 Stroud Water Research Center (SWRC)
 *                          and the EnviroDIY Development Team
 *            This example is published under the BSD-3 license.
 * @author Kevin M.Smith <SDI12@ethosengineering.org>
 * @date August 2013
 *
 * @brief Example A: Using the Wildcard - Getting Single Sensor Information
 *
 * This is a simple demonstration of the SDI-12 library for Arduino.
 *
 * It requests information about the attached sensor, including its address and
 * manufacturer info.
 */

#include <SDI12.h>

#define SERIAL_BAUD 115200  /*!< The baud rate for the output serial port */
#define DATA_PIN 7          /*!< The pin of the SDI-12 data bus */
#define POWER_PIN 4         /*!< The sensor power pin (or -1 if not switching power) */

/** Define the SDI-12 bus */
SDI12 mySDI12(DATA_PIN);

/**
  '?' is a wildcard character which asks any and all sensors to respond
  'I' indicates that the command wants information about the sensor
  '!' finishes the command
*/

String startConcurrent = "0C!";
String solarPlus = "0D0!";
String windPlus = "0D1!";
String temperature = "0D2!";
String orientation = "0D3!";
String wind = "0D4!";
String Palabra;

unsigned long tiempo1 = 0;
unsigned long tiempo2 = 0;
unsigned long tiempoFinal = 0;

extern volatile unsigned long timer0_millis;
unsigned long new_value = 0;

void setup() {
  // Power the sensors;
  if (POWER_PIN > 0) {
    Serial.println("Powering up sensors...");
    pinMode(POWER_PIN, OUTPUT);
    digitalWrite(POWER_PIN, HIGH);
    delay(55000);
  }
  
  Serial.begin(SERIAL_BAUD);
  while (!Serial);

  Serial.println("Opening SDI-12 bus...");
  mySDI12.begin();
  delay(500);  // allow things to settle
}

void loop() {
  tiempo1 = millis();
  mySDI12.flush();
  Serial.println("Inicio");
  //Serial.println("startConcurrent");
  Serial.println("0C!");
  mySDI12.sendCommand(startConcurrent);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
  delay(500);                     // print again in three seconds
  
/*=========================================BIEN====================================*/
  //Serial.println("solarPlus");
  Serial.println("0D0!");
  mySDI12.flush();
  mySDI12.sendCommand(solarPlus);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
  

  //Serial.println("windPlus");
  Serial.println("0D1!");
  mySDI12.flush();
  mySDI12.sendCommand(windPlus);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
  

  //Serial.println("temperature");
  Serial.println("0D2!");
  mySDI12.flush();
  mySDI12.sendCommand(temperature);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
   

  //Serial.println("orientation");
  Serial.println("0D3!");
  mySDI12.flush();
  mySDI12.sendCommand(orientation);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
   

  //Serial.println("windMinus");
  Serial.println("0D4!");
  mySDI12.flush();
  mySDI12.sendCommand(wind);
  delay(500);                     // print again in three seconds
  while (mySDI12.available()) {   // write the response to the screen
    Serial.write(mySDI12.read());
  }
   
  Serial.println();
  mySDI12.flush();

  tiempo2 = millis();
  tiempoFinal = tiempo2 - tiempo1;
  
  while (tiempoFinal < 60000){
    tiempo2 = millis();
    tiempoFinal = tiempo2 - tiempo1;
  }

  setMillis(new_value);
  
}

void setMillis(unsigned long new_millis){
  uint8_t oldSREG = SREG;
  cli();
  timer0_millis = new_millis;
  SREG = oldSREG;
}
