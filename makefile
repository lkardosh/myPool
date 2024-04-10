CC = clang
CFLAGS = -std=c99 -Wall -pedantic
export LD_LIBRARY_PATH=`pwd`
all: _phylib.so 

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm
phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o
phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i
phylib_wrap.o: phylib_wrap.c phylib.py
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o
_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) phylib_wrap.o -shared -L. -lphylib -L/usr/lib/python3.11 -lpython3.11 -o _phylib.so
clean: 
	rm *.o *.so phylib.py *.svg phylib_wrap.c
