#include <Wire.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2);
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
    lcd.print(tresc);
  }
  if (tresc == "%") {
    lcd.clear();
  }


}
