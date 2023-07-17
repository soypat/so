# so
This is a README driven repository with a short demo of how to get started with 
the creation of dynamic libraries and the linking of them to a C program and then
a Go program.

This is for **linux**.

## Summary

### Linking Go to Python dynamically
See [`python`](./python/) folder for instructions on how to call Go functions from Python. Benchmarks included to give readers an idea of use cases for linking.


### Linking C to Go dynamically
```sh
# Generate .o files
gcc -c -Wall -Werror -fpic dyn.c
# Create shared object from .o files.
gcc -shared -o libdyn.so *.o
# Create dynamically linked C program.
gcc -L. -Wall -o main.bin main.c -ldyn
# Run the output `main.bin` program telling OS where dynamic libraries are:
LD_LIBRARY_PATH=. ./main.bin
# Run the Go version.
LD_LIBRARY_PATH=. go run main.go
```

Above are instructions to link C code to Go. More detailed instructions below.



# C dynamic linking
Prerequisites:
- `gcc`. Quick fix: `sudo apt install gcc`

## Define dynamic library code
Create your `.c` file with the dynamic code.

`dyn.c`
```c
#include<stdio.h>

void foo(void) {
    puts("Shared library call detected!");
}
```
We must also create the header file that will be distributed with the dynamic library.
The pragma compiler directive is so the code is not included multiple times in a single project.
IT may not be well supported across compilers so prefer using `ifndef` styled pragmas if cross compiling.

`dyn.h`
```h
#pragma once
extern void foo(void);
```


## Create the .so file so it can be dynamically loaded into programs
Start by creating the object files (`*.o`) for each source file.
```sh
gcc -c -Wall -Werror -fpic dyn.c
```
This command generates a single object file for each source `.c` file.
If there are various `.c` files list them as arguments to `gcc. `fpic` flag ensures
code is position independent (PIC). `-c` file ensures each `.o` file is not linked yet.

The result is that a **`dyn.o`** file is created for our single `dyn.c` source file.

Now we may compile the dynamic library from the `.o` files into a dynamic library
we will call **`libdyn.so`**. It's common to prefix dynamic library `.so` files with "lib".

```sh
gcc -shared -o libdyn.so *.o
```
You should now have a dynamic library ready to be loaded into a project!

## Use your dynamic library
Let's write our user or client-side program that uses the dynamic code:

```c
#include <stdio.h>
#include "dyn.h"

int main(void) {
    puts("running program");
    foo();
    return 0;
}
```
Notice we include the header file of the dynamic library and with that we are ready to use the library's `foo` function.

## Dynamically link your program
We can attempt to now compile our program to a program called **`test`**:
```sh
$ gcc -Wall -o test main.c -ldyn
/usr/bin/ld: cannot find -ldyn: No such file or directory
collect2: error: ld returned 1 exit status
```
Looks like we need to tell gcc where it can find our library with the `-L` flag.

We tell gcc to look in the current directory `.` for shared libraries.
```sh
gcc -L. -Wall -o test main.c -ldyn
```
We've now created our program **`test`**! Let's try running it!

## Running your dynamically linked program

```sh
$ ./test 
./test: error while loading shared libraries: libdyn.so: cannot open shared object file: No such file or directory
```
Looks like we need to tell the operating system where to look for the dynamic library.
We can do that by setting the `LD_LIBRARY_PATH` environement variable. The easiest
way to do that is just passing it as the command's current environment:

```sh
$ LD_LIBRARY_PATH=. ./test 
running program
Shared library call detected!
```

**Tada!**

If the above does not work try including the actual path into the variable:
```sh
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:. ./test 
```

# Go dynamic linking
Prerequisites:
- Any version of [Go](https://go.dev/dl/)
- `libdyn.so` generated in the previous shared object creation step

## Using dynamic library from Go
To link any kind of C code to a Go program we use what is called "Cgo". A staple of
Cgo lets us interoperate between C and Go easily. To do this we must include the
special `"C"` package into our Go program. This is really not a package like other Go packages,
it lets us define C code inline above it. We can then call C functions from the `C`
namespace as if we were programming in C within a Go source file.

`main.go`
```go
package main

/*
#include "dyn.h"
*/
import "C"

func main() {
	println("go program started")
	C.foo()
}
```

## Compiling and running a dynamically linked Go program
Let's try running this program:
```sh
$ go run main.go
# command-line-arguments
/usr/local/go/pkg/tool/linux_amd64/link: running gcc failed: exit status 1
/usr/bin/ld: /tmp/go-link-185139139/000001.o: in function `_cgo_403d439493e8_Cfunc_foo':
/tmp/go-build/cgo-gcc-prolog:49: undefined reference to `foo'
collect2: error: ld returned 1 exit status
```
Oof! Lots of errors. Link step is failing. We need to let Go know `foo` is a dynamically
linked function just like we told `gcc`.

```sh
$ LD_LIBRARY_PATH=. CGO_LDFLAGS="-L. -ldyn" go run main.go
go program started
Shared library call detected!
```

We may simplify this further by adding cgo pragmas to the inline C code in `main.go`:
```
#cgo LDFLAGS: -L. -ldyn
#include "dyn.h"
```
Now we just need the LD_LIBRARY_PATH variable to be set, just like when using `gcc`.

```sh
$ LD_LIBRARY_PATH=. go run main.go
go program started
Shared library call detected!
```

# Dynamic linking functions with arguments
The procedure is identical, just modify the header file to reflect the function signature.
You may find a worked example under [`withargs`](./withargs)

