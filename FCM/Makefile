_FIBSCookieMonster.so: FIBSCookieMonster_wrap.c FIBSCookies_wrap.c setup.py
	python setup.py build_ext --inplace

FIBSCookieMonster.py FIBSCookieMonster_wrap.c: FIBSCookieMonster.i FIBSCookies.i CLIP.i FIBSCookieMonster.c
	swig -python FIBSCookieMonster.i


clean:
	rm _FIBSCookieMonster.so FIBSCookieMonster_wrap.c FIBSCookieMonster.py
