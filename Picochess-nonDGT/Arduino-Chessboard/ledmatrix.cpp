
#include "ledmatrix.h"


Ledmatrix::Ledmatrix(void)
{

  pinMode(dataIn, OUTPUT);    //mx
  pinMode(mxclock,  OUTPUT);
  pinMode(load,   OUTPUT);

  writeMax(max7219_reg_scanLimit, 0x07, 0x07);
  writeMax(max7219_reg_displayTest, 0x00, 0x00); // no display test
  writeMax(max7219_reg_decodeMode, 0x00, 0x00);  // using an led matrix (not digits)
  writeMax(max7219_reg_intensity, 0x0f , 0x0f); //, 0x0f);    // the first 0x0f is the value you can set
  writeMax(max7219_reg_shutdown, 0x01, 0x01);    // not in shutdown mode
  
  for (int e = 1; e <= 8; e++)
  {
    writeMax(e, 0, 0);  // empty registers, turn all LEDs off
  }
  
  // range: 0x00 to 0x0f

}
void Ledmatrix::FlashSquare(int row, int column, int milliseconds)
{
  
  ledon(row, column, 1);
  UpdateLedMatrix();
  //WriteMatrix();
  delay(milliseconds);
  ledon(row, column, 0);
 
  UpdateLedMatrix();
  //WriteMatrix();

}

void  Ledmatrix::ledon(int row, int column, int state)
{
  row = 7 - row;      //to correct for reverse board wiring 0,0 now bottom left
  ledarray[row][column] = state;
  ledarray[row + 1][column] = state;
  ledarray[row][column + 1] = state;
  ledarray[row + 1][column + 1] = state;
  
  //WriteMatrix();
}

void Ledmatrix::UpdateLedMatrix()   //transfer 9*9 ledarray to 2 max[8*8] arrays
{
  for (int row = 0; row < 8; row++)
  {
    for (int column = 0; column < 8; column++)
    {
      if (ledarray[row][column] == 1) max1[column] |= (1 << row);
      else max1[column] &= ~(1 << row);
    }
  }

  for (int j = 0; j < 8; j++)
  {
    if (ledarray[8][j] == 1) max2[1] |= (1 << j);
    else max2[1] &= ~(1 << j);

    if (ledarray[j][8] == 1)  max2[0]  |= 1 << j;
    else max2[0] &= ~(1 << j);
  }
  if (ledarray[8][8] == 1) max2[2] |= 1;
  else max2[2] &= ~0x1;
  for (int i = 0; i < 8; i++)
  {
    writeMax(i + 1, max1[i], max2[i]);
  }
}
//void Ledmatrix::WriteMatrix()      //writes max1 and max2 matrixes to 2 max7219
//{
//  for (int i = 0; i < 8; i++)
//  {
//    writeMax(i + 1, max1[i], max2[i]);
//  }
//  //writeMax(2, 0xff, 0xff);
//}


void Ledmatrix::WriteByte(byte data)
{
  for (int i = 0; i < 8; i++)
  {
    digitalWrite( mxclock, LOW);   // tick
    if (data & 0x80)  digitalWrite(dataIn, HIGH); // send 1
    else digitalWrite(dataIn, LOW); // send 0
    data <<= 1;
    digitalWrite( mxclock, HIGH);   // tock
  }
}
void Ledmatrix::writeMax(int reg, int pattern1, int pattern2)
{
  digitalWrite(load, LOW);       // begin
  WriteByte(reg);                // specify register
  WriteByte(pattern2);
  WriteByte(reg);
  WriteByte(pattern1);
  digitalWrite(load, LOW);       // load
  digitalWrite(load, HIGH);
}
void  Ledmatrix::Clear()
{
  for(int row=0;row<8;row++)
    {
      for(int column= 0;column<8;column++)
      {
        ledarray[row][column] = 0;
        ledarray[row + 1][column] = 0;
        ledarray[row][column + 1] = 0;
        ledarray[row + 1][column + 1] = 0;
      }
    }
  
  
  
}


