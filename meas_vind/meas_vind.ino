int sensorPin = A1;
int delayTime = 10;
bool record = false;


void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}


void loop() {
  if (record) {
    Serial.println(analogRead(sensorPin));
    delay(delayTime);
  }
  else {
    if (Serial.available()) {
      record = true;
      Serial.println("Recording");
      Serial.println(delayTime);
    }
  }
}
