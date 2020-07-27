#include <Stepper.h>
#define STEPS 2038 // Steps per revolution
#define pinRefill 2
#define pinDispense 3

float stepsPerMicroliter = STEPS / 100.00;
const int msgSize = 20;
char msg[msgSize];
float volume; // Volume in microliters
float dispensingSpeed = 5; // Dispensing speed in microliters per second
bool continuous = LOW; // flag for continuous movement

Stepper stepper(STEPS, 8, 10, 9, 11);

void setup(){  
  // Setting up the pushing buttons
  pinMode(pinRefill, INPUT_PULLUP);
  pinMode(pinDispense, INPUT_PULLUP);
  Serial.begin(9600);
  stepper.setSpeed(((dispensingSpeed * stepsPerMicroliter)/STEPS) * 60);
}

void loop(){  
  if(Serial.available()) receiveMsg();
  if(msg[0] == 'd' && msg[1] == 'v') dispenseVolume();
  if(msg[0] == 's' && msg[1] == 's') customSetSpeed();
  if(msg[0] == 's' && msg[1] == 'c') continuous = HIGH;
  if(msg[0] == 'h' && msg[1] == 'c') continuous = LOW;
  moveContinuous();
  checkButtons();
}

void receiveMsg(){
  int index = 0;
  bool invalid = LOW;
  // Clear msg variable
  for(int i = 0; i < (msgSize - 1); i++) msg[i] = '\0';
  // Check if first character is '<'
  if(Serial.read() != '<') return;
  delay(2);
  while(Serial.available()){
    msg[index] = Serial.read();
    // Check if message is finished, if so replace '>' by '\0'
    if(msg[index] == '>') msg[index] = '\0';
    index++;
    delay(2);
  }
  // Clear message if longer than msgSize
  if(index >= msgSize) for(int i = 0; i < (msgSize - 1); i++) msg[i] = '\0';
  Serial.println(msg);
}

void moveContinuous(){
  if(continuous) stepper.step(-10);
}

void dispenseVolume(){
  long stepsToMove;
  volume = atof(&msg[2]);
  stepsToMove = volume * stepsPerMicroliter;
  // The direction needs to be flipped. So I am using negative steps
  stepper.step(-stepsToMove);
  //Serial.print("Volume: ");
  //Serial.println(stepsPerMicroliter);
  //Serial.print("Steps to move: ");
  //Serial.println(stepsToMove);
}

void customSetSpeed(){
  float stepperSpeed;
  dispensingSpeed = atof(&msg[2]);
  // Convert dispensing speed from microliter per second to rotations per minute
  stepperSpeed = ((dispensingSpeed * stepsPerMicroliter)/STEPS) * 60;
  stepper.setSpeed(stepperSpeed);
  //Serial.print("Speed:");
  //Serial.println(stepperSpeed);
}

void checkButtons(){
  if(!digitalRead(pinRefill)) stepper.step(-10);
  if(!digitalRead(pinDispense)) stepper.step(10);
}
