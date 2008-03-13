%module FIBSCookieMonster

%{
#define SWIG_FILE_WITH_INIT
#include "clip.h"
#include "FIBSCookieMonster.h"
%}

int  FIBSCookie(const char * nextMessage);
void ResetFIBSCookieMonster();
void ReleaseFIBSCookieMonster();

%include FIBSCookies.i
%include CLIP.i


