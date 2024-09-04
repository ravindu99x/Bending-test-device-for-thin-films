//ATTEMPT_1

// Run a A4998 Stepstick from an Arduino UNO.
// Paul Hurley Aug 2015
int x; 
int k = 1;
int speed = 1;

#define BAUD (9600)
#define SWITCH_PIN 2 // Pin connected to the switch

const int EnablePin = 8;
const int stepPin = 5; 
const int dirPin = 4; 

int buttonState = 0;        // Current state of the button
int counter = 01;            // Variable for counter function
int lastButtonState = 1;    // Previous button state
volatile int count = 0;     // Volatile variable to store the count
int dead = 0;
int bend =0;
void setup() 
{
  
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  pinMode(6,OUTPUT); // Enable
  pinMode(5,OUTPUT); // Step
  pinMode(4,OUTPUT); // Dir
  digitalWrite(6,LOW); // Set Enable low
}

void loop() 
{
  pinMode(SWITCH_PIN, INPUT_PULLUP); // Set the switch pin as input with internal pull-up resistor
  attachInterrupt(digitalPinToInterrupt(SWITCH_PIN), switchInterrupt, FALLING); // Attach interrupt to switch pin
  if (Serial.available() > 0) { // If data is available to read
    // Read the incoming command
    String command = Serial.readStringUntil('\n');
        speed = command.substring(0, 4).toInt();
        bend = command.substring(4, 7).toInt();
        int dead = command.substring(7, 8).toInt();
        Serial.println(speed);
        Serial.println(bend);
        Serial.println(dead);

        if (dead == 1) {
        count = 0; // Reset the count to zero
        counter = 0;
        dead = 0;
//      Serial.println("Count reseted");
    }
  }
  k = speed;
  
  digitalWrite(6,LOW); // Set Enable low
  digitalWrite(4,HIGH); // Set Dir high
  if (count != bend) 
  {
    digitalWrite(5,HIGH); // Output high
    delayMicroseconds(k); // Wait
    digitalWrite(5,LOW); // Output low
    delayMicroseconds(k); // Wait

  }

  
}

void switchInterrupt() {
  buttonState = digitalRead(SWITCH_PIN);
  if (buttonState != lastButtonState) {
    // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
    if (buttonState == HIGH) {
      count = counter++;  // Increment the counter each time the switch is pressed
      delay(5);
      lastButtonState = HIGH;
      Serial.println(count);
    } else {
      lastButtonState = LOW;
    }
  }
}
