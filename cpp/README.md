## Sample Space Reducing Process 

## Project Overview 

This project implement the space pace reducing process using `C++` with `Python` binding. The implementation is based on the description in [Sample space reducing cascading processes produce the full spectrum of scaling exponents](https://arxiv.org/abs/1703.10100).

## Compling

1. Clone the repo:

```bash
bash> https://github.com/aredjil/ssr.git
```

2. Navigate to the repo: 

```bash 
bash> cd ssr 
```

3. Compile with `cmake`:

```bash
bash> cmake -S . -B cmake-build 
bash> cmake --build cmake-build
```

or alternatively:

```
bash> mkdir -p cmake-build 
bash> cd cmake-build 
bash> make 
```

## Usage

```bash
bash> ./main.x [--n N] [--m MAX_ITER] [--mu MU]
```

| Option         | Description                              | Default Value |
| -------------- | ---------------------------------------- | ------------- |
| `--n N`        | Number of states in each SSR cascade     | 10001         |
| `--m MAX_ITER` | Number of SSR cascades to simulate       | 3000          |
| `--mu MU`      | Parameter $\mu$ controlling cascade behavior | 1.0           |

### Example 

```bash 
bash> ./main.x --n 5000 --m 1000 --mu 1.5 
```

The program outputs the states of each cascade as integers, one per line, to standard output.

### Notes 

- Output can be redirected to a file for later processing:
```bash 
bash> ./main.x --n 10000 --m 3000 > output.txt
```
- Each line in the output corresponds to a single state visited in the SSR cascades.


## Python Bindings

This project includes Python bindings for the `C++` SSR simulator using `pybind11`. To build and use the bindings locally:
```bash 
bash> python setup.py build_ext --inplace
```
This command compiles the `C++` extension and places the resulting `.so` file directly in the source directory (e.g., `pyssr.cpython-<version>-x86_64-linux-gnu.so`). This allows you to immediately import and use the module in Python:

```python 
#! /usr/bin/env python3 
import pyssr
def main():
  sim = pyssr.SSR()
  results = sim.ssr_casc(10001, 1.0)

if __name__ =="__main__":
  main()
```

## Notes 
- No installation is needed if you use `build_ext --inplace`.
- Avoid naming conflicts with the `C++` `build/` directory by using separate environments or temporary folders if both `CMake` and `Python` builds are required.
- Requires `Python ≥3.6`, `pybind11`, and a `C++17`-compatible compiler.

