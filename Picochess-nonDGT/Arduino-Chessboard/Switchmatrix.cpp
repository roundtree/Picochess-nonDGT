
#include "SwitchMatrix.h"


using namespace std;
SwitchMatrix::SwitchMatrix(void)
{ 
  pinMode(SR_Sin , INPUT);

  pinMode(PSCont, OUTPUT);
  pinMode(SR_SCLK, OUTPUT);

  pinMode(Cntr_CLK, OUTPUT);
  pinMode(Cntr_CLR, OUTPUT);
}



bool SwitchMatrix::KeyChanged()
{
  static int lastkey;

  if ( (millis() - startTime) < debounceDelay )  return false;
  else startTime = millis();
  if (checkmatrix())      
  {                         //key changed
    //Serial.print("matrix  " );
    //Serial.println(key );
    if (key == lastkey)
    {
      lastkey = 0;
      matrix[row][column] = state;
      keychanged=key;
      if(state==1) lifted=false;
      else lifted=true;
      
      return true;
    }
    else
    {
      lastkey = key;
    }
  }
  return false;
}
 bool SwitchMatrix::GetKeyState(int key)
 {
    int c = key/8;
    int r = key & 0x7;
    if(matrix[c][r]==1) return true;
    else return false;
 }

bool SwitchMatrix::checkmatrix()
{
  
  //Serial.println("CheckMatrix");
  digitalWrite(Cntr_CLR, HIGH); //reset 4017
  digitalWrite(Cntr_CLR, LOW);

  for (row = 0; row < 9; row++)
  {
    digitalWrite(Cntr_CLK, HIGH);  //clock 4017 -use outputs 1-9 ; not 0
    digitalWrite(Cntr_CLK, LOW);

    digitalWrite(PSCont, HIGH);   //latch paralel data
    digitalWrite(PSCont, LOW);
    for (column = 0; column < 8; column++)
    {
      int data = digitalRead(SR_Sin);
      if (data != matrix[row][column])
      {
        
        state = data;
        key = (row * 8 + column);
        return (true);
      }

      digitalWrite(SR_SCLK, HIGH);            //next bit
      digitalWrite(SR_SCLK, LOW);

    }
  }
  return (false);

}


void SwitchMatrix::fillMatrix()
{
  digitalWrite(Cntr_CLR, HIGH); //reset 4017
  digitalWrite(Cntr_CLR, LOW);

  for (int c = 0; c < 8; c++)
  {
    digitalWrite(Cntr_CLK, HIGH);  //clock 4017 -use outputs 1-8 ; not 0
    digitalWrite(Cntr_CLK, LOW);

    digitalWrite(PSCont, HIGH);   //latch paralel data
    digitalWrite(PSCont, LOW);
    for (int r = 0; r < 8; r++)
    {
      int data = digitalRead(SR_Sin);
      matrix[c][r] = data;
  
      digitalWrite(SR_SCLK, HIGH);            //next bit
      digitalWrite(SR_SCLK, LOW);

    }
  }

}


