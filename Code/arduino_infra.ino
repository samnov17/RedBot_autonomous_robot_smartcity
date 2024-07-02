#include <Servo.h>

// Create a servo object
Servo myServo;
char command ='S';

void setup() {
  // Attach the servo to pin 9
  Serial.begin(115200);
  myServo.attach(9);
}

void loop() {
  while (true)
  {
    if (Serial.available() > 0) 
          {
              command = Serial.read();
          }
  // Move the servo from 0 to 90 degrees
    if (command == 'O')
      {
        for (int angle =90 ; angle <= 180; angle++) 
          {
            myServo.write(angle);
            delay(5); // Delay for smoother motion, adjust as needed
          }
        delay(15000);
        // Move the servo back to 0 degrees
        for (int angle = 180; angle >= 90; angle--) 
          {
            myServo.write(angle);
            delay(5); // Delay for smoother motion, adjust as needed
          }
        command = 'S';
      }
     





  }

  // Add additional code or conditions here if needed
}
