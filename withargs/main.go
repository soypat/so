package main

/*
#cgo LDFLAGS: -L. -ldyn
#include "dyn.h"
*/
import "C"

func main() {
	println("go program started")
	a := C.fibonacci(10)
	println("tenth fibonacci number:", a)
}
