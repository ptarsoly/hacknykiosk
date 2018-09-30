#include <Key.h>
#include <Keypad.h>
#include <RFID.h>
#include <SPI.h>

// NFC reader specific definitions
#define SS_PIN 53
#define RST_PIN 5

RFID rfid(SS_PIN, RST_PIN);
unsigned long pastNFCTime = 0;
unsigned long delayNFCMillis = 2000;


// Keypad specific definitions
const byte rows = 4; //four rows
const byte cols = 3; //three columns
char keys[rows][cols] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte rowPins[rows] = {37, 38, 41, 42}; //connect to the row pinouts of the keypad
byte colPins[cols] = {45, 46, 49}; //connect to the column pinouts of the keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, rows, cols );
String outcome = "";
char key;
void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.init();
  keypad.setDebounceTime(50);
}

void loop() {
  if (rfid.isCard() && rfid.readCardSerial()) {
    if (millis() - pastNFCTime >= delayNFCMillis) {
      Serial.println("Peter");
      pastNFCTime = millis();
    }

  }

  key = keypad.getKey();

  if (key != NO_KEY) {
    outcome += key;
    if(key == '#') {
      Serial.println(outcome);
      outcome = "";
    }
  }

  rfid.halt();
}
