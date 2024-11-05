OBJECTS = twency48/build/main.o

all: $(OBJECTS)
	gcc $(OBJECTS) -shared -o ../twenty48AI/twency48.so -lm
	gcc $(OBJECTS) -o twency48/twency48 -lm

twency48/build/main.o: twency48/src/main.c | build
	gcc -c -fPIC $< -o $@

twency48/build/%.o: twency48/src/%.c | build
	gcc -c -fPIC $< -o $@

build:
	mkdir -p twency48/build

clean:
	rm -rf build ../twenty48AI/twency48.so
	rm -rf build twency48/twency48
