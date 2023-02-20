package main

/*
#cgo LDFLAGS: -L. -ldyn
#include "dyn.h"
*/
import "C"

func foo() { C.foo() }

func main() {
	println("go program started")
	foo()
}
