CC = g++
CFLAGS = -O3 -march=native
LDFLAGS =

SRC_DIR = ./src
BIN_DIR = ./bin

TARGETS = $(BIN_DIR)/cascade_ssr.x $(BIN_DIR)/noisy_ssr.x $(BIN_DIR)/std_ssr.x

all: $(TARGETS)

# Ensure bin directory exists
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Build rules with bin directory dependency
$(BIN_DIR)/cascade_ssr.x: $(SRC_DIR)/cascade_ssr.cpp | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

$(BIN_DIR)/noisy_ssr.x: $(SRC_DIR)/noisy_ssr.cpp | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

$(BIN_DIR)/std_ssr.x: $(SRC_DIR)/std_ssr.cpp | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(BIN_DIR)/*.x
