# Dynamic linking of Go to Python
Dynamic linking can also go the other way around. There are examples on how to link
Go functions to Python using the `ctypes` library in the [`python`](./python/). 

|Authors note on linking Go or C to python|
|-----|
| This path is much more sinuous than the equivalent in Go. Whereas in Go all it's primitive types map directly to C types, this is not the case in Python. **Have a StackOverflow tab open.** |

## Build instructions
1. Run `go generate` in command line from inside [`go`](./go) folder. This will generate the `go.so` file (shared object) that contains the code that Python will run.  
   a. Alternatively, run: `go build -buildmode=c-shared -o go.so go.go`  (this is the same command `go generate` executes)

You are now ready to use the dynamic library contained in the `go` module! You can now run the benchmarks in `main.py`.

## Benchmarks

Benchmark results: Dynamic is Go call; Native is the equivalent python function.
```
Hello world print: Dynamic: 2.548694610595703e-06  Native: 1.3709068298339844e-06
JSON: Dynamic: 8.697509765625e-06  Native: 1.900196075439453e-06
Websocket mask 64kB: Dynamic: 0.00016345262527465822  Native: 1.2098654508590698
Websocket masking (256kB): Dynamic: 0.000755465030670166  Native: 45.29218244552612
```

Note that for relatively small function calls Go can be 2 to 4 times slower 
than simply using python built ins:

  - This is seen in the Hello World print (Python x2 faster)
  - JSON parsing (Python x4 faster)

For when working with non-trivial amounts of data, i.e. a 64kB buffer that is 
transformed via integer binary transformations, Go can outperform Python by orders
of magnitude. 

  - 64kB: Byte buffer xor transformation for websocket protocol (**Go x7000 faster**)
- 256kB: Identical transformation as above but on 4 times the memory (**Go x60000 faster**)

Note that the operations done are identical. There is no SIMD or shortcut done in the Go version
that is not present in the Python version.
 
Python is slower because for loops have a painfully noticeable overhead when working with large 
amounts of individual data points that must be transformed. 

## How it works
### Go's side
The `go` folder contains a go file with the functions exported via CGo. All these functions take in and return C types and are exported via the `export` compiler pragma (a.k.a. compiler directive).

These functions when compiled with the go compilers' special build-mode `c-shared` are built as a shared object (found with `.so` extension on linux, `.dll` on windows). Other programs can tap into these functions with their exported name and by knowing the function signature or Application Binary Interface (ABI). We use C's ABI since it is the most common one for interop between programs and Foreign Function Interfaces (FFI).

### Python's side
We define a folder that will contain the shared object and our python program, which will be an `__init__.py` script for ease of import (couldn't figure out how to do it any other way).

Within this file we import the `ctypes` native python library which allows us to work with the C ABI. With it we can import the generated `.so` object with LoadLibrary and immediately begin using the functions in the library, given we know their names and signature:

```python
library = ctypes.cdll.LoadLibrary(__file__.replace("__init__.py","go.so"))
result = int(library.add(ctypes.int(1), ctypes.int(2)))
print(result) # should print 3 if add exists and does what we expect.
```

We must be wary of types since the C ABIs will usually rely on pointers and Python eschews pointers in virtually all aspects, requiring some type juggling to get to the juicy low-level bits.