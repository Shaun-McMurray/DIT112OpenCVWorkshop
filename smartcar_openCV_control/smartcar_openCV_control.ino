#include <Smartcar.h>
#include  <Chrono.h>

Car car;
Chrono myChrono; 

const int redPin = 7;
const int greenPin = 6;
const int bluePin = 5;

void setup() {
  Serial.begin(9600);
  car.begin();
  car.setAngle(0);  // Always go straight

  // RGB LED pins
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  
  // Reset timer for stopping function
  myChrono.restart();
}

void loop() {
  handleInput();
  stopTimer();
}

/*
 * Handle serial input from RPi if there is any
 */
void handleInput() {
  if (Serial.available()) {
    String inputRPi = Serial.readStringUntil('\n');
     
    if (inputRPi.startsWith("f")) {
      setColor(0, 0, 255);  // Set LED to blue
      car.setSpeed(50);     // Apply 50 % thottle
      myChrono.restart();   // Restart timer for stop timer
    }
    else if (inputRPi.startsWith("s")) {
      setColor(255, 0, 0);  // Set LED to red
      car.setSpeed(0);      // Stop the car
      myChrono.restart();
    }
  }
}

/* Sets color of the RBG LED according to passed args
 *  https://learn.adafruit.com/adafruit-arduino-lesson-3-rgb-leds/arduino-sketch 
 */
void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}

/* 
 * Stops the car and powers off RGB LED in case of no valid input from RPi for 500 ms
 */
void stopTimer() {
  if (myChrono.hasPassed(500)) {
    setColor(0, 0, 0);
    car.setSpeed(0);
  }
}
