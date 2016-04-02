



#ifndef Ledmatrix_h
#define Ledmatrix_h

#include "Arduino.h"

#define dataIn  7
#define load  8
#define mxclock  9

#define max7219_reg_decodeMode   0x09
#define max7219_reg_intensity    0x0a
#define max7219_reg_scanLimit    0x0b
#define max7219_reg_shutdown     0x0c
#define max7219_reg_displayTest  0x0



class Ledmatrix {

    byte ledarray[9][9];
    byte max1[8]; //led driver chips
    byte max2[8];

    public:
    Ledmatrix();
    void FlashSquare(int row, int column, int milliseconds);
    void  ledon(int row, int column, int state);
    void UpdateLedMatrix() ;  //transfer 9*9 ledarray to 2 max[8*8] arrays
    void Clear();
    private:
   
    
    
    void WriteMatrix();      //writes max1 and max2 matrixes to 2 max7219
    void WriteByte(byte data);
    void writeMax(int reg, int pattern1, int pattern2);
    


};
#endif
