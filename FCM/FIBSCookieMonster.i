%module FIBSCookieMonster

%{
#define SWIG_FILE_WITH_INIT
#include "clip.h"
#include "FIBSCookieMonster.h"
%}

%include FIBSCookies.i
%include CLIP.i

int  FIBSCookie(const char * nextMessage);
void ResetFIBSCookieMonster();
void ReleaseFIBSCookieMonster();



