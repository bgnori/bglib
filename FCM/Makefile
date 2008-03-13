_FIBSCookieMonster.so: FIBSCookieMonster_wrap.c setup.py
	python setup.py build_ext --inplace

FIBSCookieMonster_wrap.c FIBSCookieMonster.py: FIBSCookieMonster.i FIBSCookieMonster.c CLIP.i FIBSCookies.i
	swig -python FIBSCookieMonster.i 

clean:
	rm _FIBSCookieMonster.so FIBSCookieMonster_wrap.c FIBSCookieMonster.py
