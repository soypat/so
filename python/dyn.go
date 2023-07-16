package main

import (
	"C"
)
import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"math/bits"
	"strings"
	"unsafe"
)

//go:generate go build -buildmode=c-shared -o dyn.so dyn.go
func main() {}

//export helloWorld
func helloWorld() {
	fmt.Println("hello world")
}

//export parsejson
func parsejson(documentPtr *C.char) {
	type Document struct {
		Name    string   `json:"name"`
		Age     int      `json:"age"`
		Cars    []string `json:"cars"`
		Friends []struct {
			Name string `json:"name"`
			Age  int    `json:"age"`
		} `json:"friends"`
	}
	var doc Document
	var docStr string = C.GoString(documentPtr)
	json.NewDecoder(strings.NewReader(docStr)).Decode(&doc)
}

//export websocketTransform
func websocketTransform(keyIn C.int, data *C.char, l C.int) C.int {
	bytes := C.GoBytes(unsafe.Pointer(data), l)
	result := maskWS(uint32(keyIn), bytes)
	return C.int(result)
}

// Websocket masking/unmasking.
func maskWS(key uint32, b []byte) uint32 {
	if key == 0 {
		return 0
	}
	for len(b) >= 4 {
		v := binary.BigEndian.Uint32(b)
		binary.BigEndian.PutUint32(b, v^key)
		b = b[4:]
	}
	if len(b) != 0 {
		// xor remaining bytes and shift mask.
		for i := range b {
			b[i] ^= byte(key >> 24)
			key = bits.RotateLeft32(key, 8)
		}
	}
	return key
}
