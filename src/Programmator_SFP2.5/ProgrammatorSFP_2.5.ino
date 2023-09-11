//ProgrammatorSFP_2.5
//Прошивка программатора для версии SFP_ProgV2.3.3
//Developed by ZemtsovV

#include <Wire.h>
//#include <EEPROM.h>

byte byteAr[256];
byte sumOfBytes[1];
byte numOfBytes[256];
byte valOfBytes[256];
byte WriteAddr[1];
int Arr[256];
byte act[1];
byte S;


void setup() {
  esp_deep_sleep_disable_rom_logging();
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000L);
  Serial.write(0xDD);
  Serial.println();
}

void loop() {
  if (Serial.available() > 0){
    Serial.readBytes(act, 1);
    if (act[0] == 0x01 or act[0] == 49) {
      ReadMem(); 
    }
    if (act[0] == 0x05) {
      WriteBytes();
    }
    if (act[0] == 0x04) {
      ReadBytesArray();
      WriteFromFile(byteAr);
    }
    if (act[0] == 0x06) {
      ClearSFP();
    }
    if (act[0] == 0x03) {
      InputPassword();
      }
    if (act[0] == 0x07) {
      ReadByte();
    }

    if (act[0] == 0x08){
      FastWrite();
    }
    if (act[0] == 0x0a) {
      Serial.readBytes(WriteAddr, 1);
      Serial.write(0x99);
      Serial.println();
      Serial.readBytes(numOfBytes, 1);
      Serial.write(0x99);
      Serial.println();
      Serial.readBytes(valOfBytes, 1);
      Serial.write(0x99);
      Serial.println();
      EEPROM_WriteByte(WriteAddr[0],numOfBytes[0],valOfBytes[0]);
      delay(100);
      Serial.write(0xDD);
      Serial.println();
    }
    if (act[0] == 0xee){
      I2CScan();
    }
  }
}

void FastWrite(){
  byte address[1];
  byte num[1];
  byte data[1];
  Serial.readBytes(address, 1);
  Serial.readBytes(num, 1);
  Serial.readBytes(data, 1);
  EEPROM_WriteByte(address[0], num[0], data[0]);
}
void ReadByte(){
  byte address[1];
  Serial.readBytes(address, 1);
  int bAdd = address[0];
  delay(500);
  Serial.write(0x99);
  Serial.println();
  Wire.beginTransmission(0x50);  
  Wire.write(bAdd);  
  Wire.endTransmission();
  Wire.requestFrom(0x50,1);
  S = Wire.read();
  Serial.println(S);
}
  
void ReadMem(){
  byte address[1];
  Serial.readBytes(address, 1);
  int iAdd = address[0];
  delay(500);
  Serial.write(0x99);
  Serial.println();
  Wire.beginTransmission(iAdd);  
  Wire.write(0x00);  
  Wire.endTransmission(); 
  for (int b = 1; b<=8; b++){
    Wire.requestFrom(iAdd,32);
    while(Wire.available() == 0);
    for (int i = 0; i<= 31; i++){
      S = Wire.read();
      Serial.println(S);
    }
  }
 }

void ReadBytesArray(){
  Serial.readBytes(WriteAddr, 1);
  delay(200);
  Serial.write(0x99);
  Serial.println();
  Serial.readBytes(sumOfBytes, 1);
  delay(200);
  Serial.write(0x99);
  Serial.println();
  Serial.readBytes(byteAr, sumOfBytes[0]);
  for (int i=0;i<sumOfBytes[0];i++){
    Arr[i] = int(byteAr[i]);
  }
 }
void WriteFromFile(byte lst[]){
    int iAdd = WriteAddr[0];
    for (int i=0;i<=sumOfBytes[0];i++){;
      EEPROM_WriteByte(iAdd,i,lst[i]);
    }
    Serial.write(0x99);
    Serial.println();
  }
 
void ClearSFP(){
   for (int i = 0; i<=255; i++){
    EEPROM_WriteByte(0x50,i,0x00);
  }
  Serial.write(0x99);
  Serial.println();
 }

void EEPROM_WriteByte(byte dev, byte Address, byte data){
    Wire.beginTransmission(dev);
    Wire.write(Address);
    Wire.write(data);
    delay(5); 
    Wire.endTransmission();
  }

void WriteBytes(){
    ReadWrite();
    int iAdd = WriteAddr[0];
    for (int i = 0; i<sumOfBytes[0]; i++){
      EEPROM_WriteByte(iAdd, numOfBytes[i], valOfBytes[i]);
    }
    Serial.write(0xDD);
    Serial.println();
  }

void ReadWrite(){ 
    Serial.readBytes(WriteAddr, 1);
    Serial.write(0x99);
    Serial.println();
    Serial.readBytes(sumOfBytes, 1);
    Serial.write(0x99);
    Serial.println();
    Serial.readBytes(numOfBytes, sumOfBytes[0]);
    Serial.write(0x99);
    Serial.println();
    Serial.readBytes(valOfBytes, sumOfBytes[0]);
  }

void InputPassword(){
  ReadWrite();
  for (int i = 0; i<sumOfBytes[0]; i++){
    EEPROM_WriteByte(0x51, numOfBytes[i], valOfBytes[i]);
  }
  Serial.write(0xDD);
  Serial.println();
}

void I2CScan() {
  int nDevices = 0;
  byte Devices[127]; 
  byte error, address, i;
  
  for(address = 8; address < 127; address++ ){
      Wire.beginTransmission(address);
      error = Wire.endTransmission();
      if (error == 0){
          Devices[nDevices] = address;
          nDevices++;
      }
  }
  if (nDevices == 0) {
      Serial.write(0x00);
      Serial.println();
      Serial.write(0xEE);
      Serial.println();
  } else {
      for (i = 0; i <= nDevices; i++){
        Serial.write(Devices[i]);
        Serial.println();
      }
      Serial.write(0xEE);
      Serial.println();
  }
}

  
