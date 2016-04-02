

#include "ledmatrix.h"
#include "SwitchMatrix.h"


String readString;
String writeString;

Ledmatrix leds;
SwitchMatrix sw;

void setup() {

  Serial.begin(115200);
  Serial.setTimeout(50);
  pinMode(13, OUTPUT);
  sw.fillMatrix();
  newgame();
}

void loop()
{
  byte cnt = 1;
  char n[] = "newgame:w";

  FromPython();

  if (sw.KeyChanged())
  {
    int key = sw.keychanged;
    bool lifted = sw.lifted;
    if(key>63)
    {
      int button=key-64;
      if(!lifted) 
      {
        ToPython("B:" + String(button));
      }
    }
    else
    {
      if(lifted)
      {
         ToPython("L:" + String(key));
      }
      else
      {
        ToPython("D:" + String(key));
      }
       leds.FlashSquare(sw.keychanged / 8,sw.keychanged % 8, 50);
    }

  }
  //newgame();
  //delay(50);
  //  for (int i = 0; i < 8; i++)
  //  {
  //    for (int j = 0; j < 8; j++)
  //    {
  //      //leds.FlashSquare(i, j, 200);
  //      delay(200);
  //    }
  //  }
  
  
  //delay(100);
}
void ToPython(String s)
{
  Serial.println(s);// write a string

}

void FromPython()
{
  
    
  if (Serial.available() > 2)
  {
     
    char data = Serial.read();
   
    if (data == 'F')  //Flash
    {
      int sq = Serial.parseInt();
      leds.FlashSquare(sq / 8, sq % 8, 50);
    }
    if (data == 'L') //LED on
    {
       //digitalWrite(11, HIGH);
      
      int sq = Serial.parseInt();
      leds.ledon(sq / 8, sq % 8, 1);
      leds.UpdateLedMatrix();
   
    }
    if (data == 'C')  //LED Off
    {
       int sq = Serial.parseInt();
       leds.Clear();
       leds.UpdateLedMatrix();
   
    }
  }

}
void newgame()
{
  
  int brdsetup=0;
  
  while(brdsetup<32)
  {
    sw.fillMatrix(); //piece positions to matrix
    leds.Clear();
    //Serial.println(brdsetup);
    brdsetup=32;
    for(int i=0;i<16;i++)
    {
      if(!sw.GetKeyState(i))  
      {
        brdsetup--;
        leds.ledon(i / 8, i % 8, 1); //piece missing
      }
    }
     for(int i=48;i<64;i++)
    {
      if(!sw.GetKeyState(i))
     
      {
        brdsetup--;
        leds.ledon(i / 8, i % 8, 1);
      }
    }
    leds.UpdateLedMatrix();
  }
  ToPython("newgame:w");


}


