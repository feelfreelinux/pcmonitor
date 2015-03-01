
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define BACKLIGHT_PIN 3
LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7); //Tu podaj adres zdobyty przez I2C Scannera. u mnie to 0x3F
char znak;
String tresc = "";
void setup()
{
  lcd.begin(20,4);
  lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
  lcd.setBacklight(HIGH);
  lcd.home();
}

void loop() {
  char znak;
  String tresc = "";
  while(Serial.available()) {
    znak = Serial.read();
    tresc.concat(znak);
  }

  if (tresc != "") {

      if (tresc == "!") {
      tresc = "";
      lcd.setCursor(0,0);
  }

  if (tresc == "@") {
     tresc = "";
     lcd.setCursor(0,1);
  }
  if (tresc == "#") {
     tresc = "";
     lcd.setCursor(0,2);
  }
  if (tresc == "$") {
     tresc = "";
     lcd.setCursor(0,3);
  }
    lcd.print(tresc);
  }
  if (tresc == "%") {
    lcd.clear();
  }


}
