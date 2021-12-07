#pragma once

#include "Defines.h"
#include "Defines_Modes.h"

bool ChangeMode(int8_t mode);


void ModeModule_Init();

void ModeModule_Update();

void ModeModule_PrintStatus();

/********************************************
 *                 Function Modes           *
 * *****************************************/

void FUNC_printHelp(); //Mode h

void DEBUG_Func_1(); //Mode 7
void DEBUG_Func_2(); //Mode 8
void DEBUG_Func_3(); //Mode 9

void FUNC_ResetMemory(); //Mode R
void FUNC_ConfigChange(); //Mode c

void Func_Zero(); //Mode z

