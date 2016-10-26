//#include "ledmatrix.h"
#include "Switchmatrix.h"
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

SwitchMatrix sw;

int White=0;
int Black=1;
int buttonsave;

Adafruit_LEDBackpack matrix = Adafruit_LEDBackpack();

static long startTime = 0;  // the last time the output pin was toggled
int speakerPin = 12;
 
int numTones = 10;
int tones[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440};
//            mid C  C#   D    D#   E    F    F#   G    G#   A
 
void setup()
{
  
  Serial.begin(115200);
  Serial.setTimeout(50);
  matrix.begin(0x70);  // pass in the address
  sw.fillMatrix();
  buttonsave=0;
  newgame(White);

}

void loop() 
{
  static bool enablebuttons;
  
  FromPython();
  if(GetButtonMask())
  {
    if(sw.buttonmask==0)
    {
      enablebuttons=true;
    } 
    else if(enablebuttons)
    {
      enablebuttons=false;
      switch (sw.buttonmask)
      {
        case 1:
          ToPython("B:0");
          break;
        case 2:
          ToPython("B:1");
        break;
        case 4:
          ToPython("B:2");
        break;
        case 8:
          ToPython("B:3");
        break;
        case 16:
          ToPython("B:4");
        break;
        case 32:
          ToPython("B:5");
          //newgame(White);
        break;
        case 64:
          ToPython("B:6");
          // newgame(Black);
         break;
         case 128:
         ToPython("B:7");
         // ToPython("tb:");
        break;
      }
    }
  }
  if (sw.KeyChanged())
  {
    int key = sw.keychanged;
    bool lifted = sw.lifted;
    
      if(lifted)
      {
         ToPython("L:" + String(key));
        // move = squares[key];
      }
      else
      {
         ToPython("D:" + String(key));
      // ToPython(move+ squares[key]);
      }
      FlashSquare(sw.keychanged , 50);
  }
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
      FlashSquare(sq, 50);
    }
    if (data == 'L') //LED on
    {
      //beep(600,500);
      int sq = Serial.parseInt();
      LightSquare(sq);
      matrix.writeDisplay();
    }
    if (data == 'C')  //LED Off
    {
       int sq = Serial.parseInt();
       ClearLeds();
    }
    if (data == 'B')  //LED Off
    {
       int sq = Serial.parseInt();
       beep(sq);
    }
  }
}


bool GetButtonMask(void)
{
  long debounceDelay = 200;
  if (sw.buttonmask== buttonsave)
  {
    if((millis() - startTime) > debounceDelay )
     {
       return true;
     }
  }
  else 
  {
    startTime = millis();
    buttonsave=sw.buttonmask;
  }
  return false;
}



void newgame(int color)
{
  int brdsetup=0;
  
  while(brdsetup<32)
  {
    sw.fillMatrix(); //piece positions to matrix
    ClearLeds();
    
    brdsetup=32;
    for(int i=0;i<16;i++)
    {
      if(!sw.GetKeyState(i))  
      {
        brdsetup--;
        LightSquare(i);
      }
    }
     for(int i=48;i<64;i++)
    {
      if(!sw.GetKeyState(i))
     
      {
        brdsetup--;
        LightSquare(i);
      }
    }
    matrix.writeDisplay();
  }
  if(color)   ToPython("newgame:b");
  else ToPython("newgame:w");
}


void  lightled(int row,int column)
{
 
  if(column<8)
  {
    matrix.displaybuffer[column] |= (1<<row);
  }
  else if(row<8)  //column 8
  {
     matrix.displaybuffer[row] |= (1<<9);
  }
  else  //column and row 8
  {
    matrix.displaybuffer[0] |= (1<<10);
  }
}

void ClearLeds()
{
  for(int i=0;i<8;i++)
  {
    matrix.displaybuffer[i] =0;
  }
   matrix.writeDisplay();
}

void FlashSquare(int square, int milliseconds)
{
  ClearLeds();
  LightSquare(square);
  beep(350);
  matrix.writeDisplay();
  //delay(milliseconds);
  ClearLeds();
}

void  LightSquare(int square)
{
    int row =int (square/8);
    int column = square & 7;
    lightled(row,column);
    lightled(row+1, column);
    lightled(row,column+1);
    lightled(row+1,column+1);
   
}


void beep(int note1)
{
  tone(speakerPin, note1);
  delay(50);
  noTone(speakerPin);
  //delay(100);
  //tone(speakerPin, note2);
  //delay(50);
  //noTone(speakerPin);

}

