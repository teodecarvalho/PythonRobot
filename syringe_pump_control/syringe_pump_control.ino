#include <Stepper.h>
#define STEPS 2038 // Steps per revolution
#define pinRefill 2
#define pinDispense 3
#define depressurizationVolume 30
#define pressurizationVolume 10
#define pressurizationSpeed 30
float stepsPerMicroliter = STEPS / 100.00;
const int msgSize = 20;
char msg[msgSize];
float volume; // Volume in microliters
float dispensingSpeed = 0.0001; // Dispensing speed in microliters per second
bool continuous = LOW; // flag for continuous movement
float stepperSpeed = STEPS/60; // Stepper speed in steps/s (defaults to 33.9)

Stepper stepper(STEPS, 8, 10, 9, 11);

void setup(){  
  // Setting up the pushing buttons
  pinMode(pinRefill, INPUT_PULLUP);
  pinMode(pinDispense, INPUT_PULLUP);
  Serial.begin(9600);
  stepper.setSpeed(10);
}

void loop(){  
  if(Serial.available()) receiveMsg();
  if(msg[0] == 'd' && msg[1] == 'v') dispenseVolume();
  if(msg[0] == 's' && msg[1] == 's') customSetSpeed();
  if(msg[0] == 's' && msg[1] == 'c') pressurize();
  if(msg[0] == 'h' && msg[1] == 'c') depressurize();
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

void clearMsg(){
    // Clear msg variable
  for(int i = 0; i < (msgSize - 1); i++) msg[i] = '\0';
}

void moveContinuous(){
  if(continuous) stepCustom(-10);
}

void pressurize(){
  long stepsToMove;
  float previousSpeed = stepperSpeed;
  // Incresing speed for pressurization
  stepperSpeed = pressurizationSpeed * stepsPerMicroliter;
  // Pressurizing
  stepsToMove = pressurizationVolume * stepsPerMicroliter;
  stepCustom(-stepsToMove);
  // Starting flag for continuous movement (continuous dispensing)
  continuous = HIGH;
  // Returning dispensing speed to its original value
  stepperSpeed = previousSpeed;
  clearMsg();
}

void depressurize(){
  long stepsToMove;
  float previousSpeed = stepperSpeed;
  // Incresing speed for depressurization
  stepperSpeed = pressurizationSpeed * stepsPerMicroliter;
  // Pressurizing
  stepsToMove = depressurizationVolume * stepsPerMicroliter;
  stepCustom(stepsToMove);
  // Starting flag for continuous movement (continuous dispensing)
  continuous = LOW;
  // Returning dispensing speed to its original value
  stepperSpeed = previousSpeed;
  clearMsg();
}

void dispenseVolume(){
  long stepsToMove;
  volume = atof(&msg[2]);
  stepsToMove = volume * stepsPerMicroliter;
  //Serial.print("Volume: ");
  //Serial.println(volume);
  //Serial.print("Steps per microliter: ");
  //Serial.println(stepsPerMicroliter);
  //Serial.print("Steps to move: ");
  //Serial.println(stepsToMove);
   // The direction needs to be flipped. So I am using negative steps
  stepCustom(-stepsToMove);
  clearMsg();
}

void stepCustom(long steps){
  long previousMillis;
  long stepIntervalMillis;
  stepIntervalMillis = (1 / stepperSpeed) * 1000;
  previousMillis = millis();
  for(int i = 0; i < abs(steps); i++){
    while(millis() - previousMillis <= stepIntervalMillis) {
      Serial.println("Waiting");
    }
    if(steps > 0){
      stepper.step(1);
    } 
    if(steps <= 0){
      stepper.step(-1);
    }
    previousMillis = millis();
  }
}

void customSetSpeed(){
  dispensingSpeed = atof(&msg[2]); // Dispensing speed in microliter/s
  stepperSpeed = ((dispensingSpeed * stepsPerMicroliter));
  Serial.print("Speed:");
  Serial.println(stepperSpeed);
  clearMsg();
}

void checkButtons(){
  if(!digitalRead(pinRefill)) stepper.step(-10);
  if(!digitalRead(pinDispense)) stepper.step(10);
}
