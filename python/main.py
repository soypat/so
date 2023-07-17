# To build dynamic library run `go generate` inside the `go` folder.
import time
import json
import go # My dynamic library linked to go code.


def main():
    N = 20
    nativeTime = benchHelloNative(N)
    dynamicTime = benchHelloDynamic(N)
    print(f"Hello: Dynamic: {dynamicTime}  Native: {nativeTime}")
    nativeTime = benchJSONNative(N)
    dynamicTime = benchJSONDynamic(N)
    print(f"JSON: Dynamic: {dynamicTime}  Native: {nativeTime}")
    nativeTime = benchWebsocketNative(1)
    dynamicTime = benchWebsocketDynamic(N)
    print(f"Websocket masking (64kB): Dynamic: {dynamicTime}  Native: {nativeTime}")


mrJSON = {
    "name": "John",
    "age": 30,
    "cars": [
        "Ford",
        "BMW",
        "Fiat"
    ],
    "friends": [
        {
            "name": "Peter",
            "age": 30
        },
        {
            "name": "Anna",
            "age": 30
        },
    ],
}


jsonStr = json.dumps(mrJSON)

def benchJSONDynamic(n:int) -> float:
    jsonUTF8 = jsonStr.encode('utf-8')
    start = time.time()
    for i in range(n):
        go.parse_person(jsonUTF8) 
    end = time.time()
    return (end - start)/n

def benchJSONNative(n:int) -> float:
    start = time.time()
    for i in range(n):
        a = json.loads(jsonStr)
    end = time.time()
    return (end - start)/n

def benchHelloDynamic(n:int) -> float:
    start = time.time()
    for i in range(n):
        go.hello_world() 
    end = time.time()
    return (end - start)/n

def benchHelloNative(n:int) -> float:
    start = time.time()
    for i in range(n):
        print("hello world")
    end = time.time()
    return (end - start)/n  

kilobytes = 256
wsData = ("HelloWorld"*(1000*kilobytes)).encode('utf-8')
wsData = bytearray(wsData)

def benchWebsocketNative(n:int) -> float:
    start = time.time()
    key = 1231242
    for i in range(n):
        key = wstxNative(key, wsData)
    end = time.time()
    return (end - start)/n

def benchWebsocketDynamic(n:int) -> float:
    start = time.time()
    key = 12334
    for i in range(n):
        key = go.wstx(key, wsData)

    end = time.time()
    return (end - start)/n

def wstxNative(key:int, data:bytearray) -> int:
    if key == 0:
        return 0
    while len(data) >= 4:
        v = int.from_bytes(data[:4], byteorder='big')
        for i in range(4):
            data[i] = ((v^key)>>i*8)%256
        data = data[4:]
    i=0
    while len(data) > 0:
        byte = key >> 24
        data[i] ^= byte
        key = ((key << 8) & 0xffffffff) | byte # rotate left 8 bits
        i-=1
    return key

main()




