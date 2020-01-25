#define pinStep 3
#define pinDir 4
#define pinRefill 5

bool directionPump = HIGH;
float pulseDelay = 100;
unsigned long refillPulseDelay = 100;
bool refillButtonPressed;
bool refillDirection = LOW;
char cmd;
bool pumpActive = LOW;

void setup() {
  pinMode(pinStep, OUTPUT);
  pinMode(pinDir, OUTPUT);
  pinMode(pinRefill, INPUT);
  Serial.begin(9600);
  Serial.println("Arduino is ready!");
}

void loop() {
  checkSerial();
  refill();
  move();
}

void move(){
  if(pumpActive){
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
      pumpActive = HIGH;
      Serial.println("Pump activated");
    } else if(cmd == 'd') {
      pumpActive = LOW;
      Serial.println("Pump deactivated");
    }
  } 
}
