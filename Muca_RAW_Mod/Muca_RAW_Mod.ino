#include <Muca.h>
#define I2C_ADDRESS 0x38
#define NUM_TX 21
#define NUM_RX 12

Muca muca;

void setup() {
  Wire.beginTransmission(0x38);
  Serial.begin(115200);
  //Serial.println("hola");
  muca.init(false);
  muca.useRawData(true); // If you use the raw data, the interrupt is not working
 // muca.setGain(100);
}

void loop() {
  //Serial.println("hola");
  GetRaw();
  delay(100);
}

void GetRaw() {

  if (muca.updated()) {
    Serial.print(muca.grid[0]);
    Serial.print(",");
    Serial.print(muca.grid[1]);
    Serial.print(",");
    Serial.print(muca.grid[12]);
    Serial.print(",");
    Serial.print(muca.grid[13]);
    Serial.println();
  }
}
