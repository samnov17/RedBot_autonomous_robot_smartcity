#include <RedBot.h>
RedBotMotors motors;
RedBotSensor IRSensor1 = RedBotSensor(A0);
RedBotSensor IRSensor2 = RedBotSensor(A6);
int triggerPin = 9;  // Connect the HC-SR04 Trigger pin to D3
int echoPin = 11;    // Connect the HC-SR04 Echo pin to D2

int leftPower;  // variable for setting the drive power
int rightPower;
char command = 'S';
int sensor_right, sensor_left;
int c1 = 0;

void setup() {

  Serial.begin(115200);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void moveForward() 
{
    while (command == 'D') {
          if (Serial.available() > 0) {
            command = Serial.read();
          }
          //Serial.println("Drive");
          int sensor1Value = IRSensor1.read();
          int sensor2Value = IRSensor2.read();

          if (sensor1Value < 200 && sensor2Value < 200) {
            motors.stop();
          } else {
            int error = (sensor1Value - sensor2Value) / 12;
            int leftSpeed = 70;
            int rightSpeed = 70;

            if (error > 0) {
              leftSpeed -= abs(error);
            } else if (error < 0) {
              rightSpeed -= abs(error);
            }
            motors.leftMotor(leftSpeed);
            motors.rightMotor(rightSpeed);
          }
        }
}

void reverse() 
{
    int count = 0;
    while (command = 'Z') 
    {
          count = count+1;           
          int sensor1Value = IRSensor1.read();
          int sensor2Value = IRSensor2.read();
          // if (Serial.available() > 0) {
          if (sensor1Value > 200 && sensor2Value > 200)  
          {
           motors.leftMotor(-50);
           motors.rightMotor(-50);
          }
          if (sensor1Value < 200 )  
          {
           motors.leftMotor(-60);
           motors.rightMotor(50);
           delay(100);
           motors.leftMotor(-50);
           motors.rightMotor(-50);
           delay(800);
          }
          if (sensor2Value < 200 )
          {            
           motors.leftMotor(50);
           motors.rightMotor(-60);
           delay(100);
           motors.leftMotor(-50);
           motors.rightMotor(-50);
           delay(800);

          }
          if (count > 35)
          {
            break;
          }


        //   if (sensor1Value < 100 && sensor2Value < 100) 
        //   {
        //      motors.leftMotor(0);
        //      motors.rightMotor(0);
        //      command = 'A';
        //      break;
        //  } 
        }
}

void moveForward_slow() 
{
    while (command == 'Q') {
          if (Serial.available() > 0) {
            command = Serial.read();
          }
          //Serial.println("Drive");
          int sensor1Value = IRSensor1.read();
          int sensor2Value = IRSensor2.read();

          if (sensor1Value < 200 && sensor2Value < 200) {
            motors.stop();
          } else {
            int error = (sensor1Value - sensor2Value) / 12;
            int leftSpeed = 60;
            int rightSpeed = 60;

            if (error > 0) {
              leftSpeed -= abs(error);
            } else if (error < 0) {
              rightSpeed -= abs(error);
            }
            motors.leftMotor(leftSpeed);
            motors.rightMotor(rightSpeed);
          }
        }
}

void left() 
{
    bool sflag = true;
    bool fflag = true;
    while (command == 'L') {

          sensor_right = IRSensor2.read();
          sensor_left = IRSensor1.read();
          motors.leftMotor(0);
          motors.rightMotor(60);

          while (sensor_right < 500 && sflag) 
          {
            sensor_left = IRSensor1.read();
            sensor_right = IRSensor2.read();
            delay(100);
          }
          sflag = false;

          while (sensor_right > 500 && fflag) 
          {
            sensor_left = IRSensor1.read();
            sensor_right = IRSensor2.read();
            delay(100);
          }
          fflag = false;

          if (sensor_left > 500) 
          {
            motors.stop();
            command = 'S';
            fflag = true;
            sflag = true;
            break;
          }
        }
        command = 'D';
}

void right() 
  
{
    bool sflag = true;
    bool fflag = true;
    while (command == 'R') {
          sensor_right = IRSensor2.read();
          sensor_left = IRSensor1.read();
          delay(100);
          motors.leftMotor(60);
          motors.rightMotor(0);
          //c = 0;
          while (sensor_left < 500 && sflag) {
            sensor_left = IRSensor1.read();
            sensor_right = IRSensor2.read();
            delay(100);
          }
          sflag = false;
          while (sensor_left > 500 && fflag) {
            sensor_left = IRSensor1.read();
            sensor_right = IRSensor2.read();
            delay(100);
          }
          fflag = false;

          if (sensor_right > 500) {
            delay(100);
            motors.stop();
            command = 'S';
            sflag = true;
            fflag = true;
            //c = 0;
            break;
          }
        }
        command = 'D';
}

void proximity() 
{
   char test = 'T';
    while (test == 'T') {
          long duration;
          duration = 0;
          motors.stop();
          int obst_count;
          obst_count = 0;
          for (int i = 0; i < 10; i++) 
          {
            digitalWrite(triggerPin, LOW);
            delayMicroseconds(2);
            digitalWrite(triggerPin, HIGH);
            delayMicroseconds(10);
            digitalWrite(triggerPin, LOW);
            duration = pulseIn(echoPin, HIGH);
            //Serial.println(duration);
            if (duration < 7000) 
            {
              obst_count = obst_count + 1;
            }
          }

          //Serial.println(obst_count);
          if (obst_count > 4) {
            motors.stop();
          }

          else {
            command = 'D';
            test = 'D';
          }
        }
    }

void stop() 
{
        while (command == 'S') {
          int sensor1Value = IRSensor1.read();
          int sensor2Value = IRSensor2.read();

          //Serial.println(sensor1Value);
          //Serial.println(sensor2Value);

          motors.stop();

          //Serial.println("Stop");
          if (Serial.available()) {
            command = Serial.read();
          }
        }
      }

  void loop() {
      while (true) 
      {

        if (command == 'C') 
        {
          motors.stop();
          delay(5000);
          command = 'D';
        } 
        else if (command == 'D') 
        {
          moveForward();
        } 
        else if (command == 'Q') 
        {
          moveForward_slow();
        } 
        else if (command == 'L') 
        {
          left();
        } 
        else if (command == 'S') 
        {
          stop();
        } 
        else if (command == 'Z') 
        {
          motors.leftMotor(-60);
          motors.rightMotor(-60);
          //reverse();
          delay(4360);
          motors.leftMotor(-60);
          motors.rightMotor(0);
          delay(1700);
          command = 'D';
        } 
        else if (command == 'W') 
        {
          motors.leftMotor(150);
          motors.rightMotor(150);
          delay(250);
          command = 'D';
        } 
        else if (command == 'A') 
        {
          motors.leftMotor(0);
          motors.rightMotor(150);
          delay(250);
          command = 'D';
        } 
        else if (command == 'F') 
        {
          motors.leftMotor(150);
          motors.rightMotor(0);
          delay(250);
          command = 'D';
        } 
        else if (command == 'X') 
        {
          motors.leftMotor(-100);
          motors.rightMotor(-100);
          delay(500);
          command = 'D';
        } 
        else if (command == 'R') 
        {
          right();
        } 
        else if (command == 'P') 
        {
          Serial.flush();
        } 
        else if (command == 'T') 
        {
          proximity();
        }
      }
}

