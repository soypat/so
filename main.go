package main

/*
#cgo LDFLAGS: -L. -ldyn
#include "dyn.h"
*/
import "C"

func main() {
	println("go program started")
	C.foo()
}
