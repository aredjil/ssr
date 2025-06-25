CC = g++
CFLAGS = -O3 -march=native 
LDFLAGS = 

TARGET = main.x
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)
	rm *.txt 
