#include <Servo.h>

#define pinServo 9
#define pinStep 3
#define pinDir 4
#define pinRefill 5
#define pinLed 13

bool directionPump = HIGH;
float pulseDelay = 100;
unsigned long refillPulseDelay = 100;
bool refillButtonPressed;
bool refillDirection = LOW;
char cmd;
bool pumpOpen = LOW; 
bool pumpEnabled = LOW;

Servo servo;

void setup() {
  servo.attach(pinServo);
  servo.write(180);
  pinMode(pinStep, OUTPUT);
  pinMode(pinDir, OUTPUT);
  pinMode(pinRefill, INPUT);
  pinMode(pinLed, OUTPUT);
  Serial.begin(9600);
  Serial.println("Arduino is ready!");
}

void loop() {
  checkSerial();
  refill();
  updatePump();
  move();
  digitalWrite(pinLed, pumpEnabled);
}

void updatePump(){
  if(pumpOpen){
    openPump();
  } else {
    closePump();
  }
}

void closePump(){
  servo.write(90);
}

void openPump(){
  servo.write(180);
}

void move(){
  if(pumpEnabled){
    digitalWrite(pinDir, HIGH);
    digitalWrite(pinStep, HIGH);
    delay(pulseDelay);
    digitalWrite(pinStep, LOW);
    delay(pulseDelay);
  }
}

void refill(){
  refillButtonPressed = !digitalRead(pinRefill);
  if(refillButtonPressed){
    digitalWrite(pinDir, refillDirection);
    digitalWrite(pinStep, HIGH);
    delayMicroseconds(refillPulseDelay);
    digitalWrite(pinStep, LOW);
    delayMicroseconds(refillPulseDelay);
  }
}

void checkSerial(){
  if (Serial.available() > 0){
    cmd = Serial.read();
    if(cmd == 'i'){
      refillDirection = !refillDirection;
      Serial.print("Refill direction inverted");
    } else if(cmd == 's'){
      pulseDelay = Serial.parseFloat();
      Serial.print("pulseDelay changed to: ");
      Serial.println(pulseDelay);
    } else if(cmd == 'r'){
      refillPulseDelay = Serial.parseInt();
      Serial.print("refillPulseDelay changed to: ");
      Serial.println(refillPulseDelay);
    } else if(cmd == 'a'){
      // Pump active and tubing opened
      pumpOpen = HIGH;
      pumpEnabled = HIGH;
      Serial.println("Pump enabled");
    } else if(cmd == 'x') {
      // Pump active but tubing closed
      pumpOpen = LOW;
      pumpEnabled = HIGH;
      Serial.println("Pump disabled");
    } else if(cmd == 'h'){
      // Pump inactive and tubing closed
      pumpOpen = LOW;
      pumpEnabled = LOW;
    }
  } 
}
