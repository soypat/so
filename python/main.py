# import dyn
import time
import ctypes
import json

try:
    # If calling this lib from inside the python folder.
    library = ctypes.cdll.LoadLibrary('./dyn.so')
except Exception as e:
    # If calling this lib from the root folder.
    library = ctypes.cdll.LoadLibrary('./python/dyn.so')



def main():
    N = 100
    nativeTime = benchHelloNative(N)
    dynamicTime = benchHelloDynamic(N)
    print(f"Hello: Dynamic: {dynamicTime}  Native: {nativeTime}")
    nativeTime = benchJSONNative(N)
    dynamicTime = benchJSONDynamic(N)
    print(f"JSON: Dynamic: {dynamicTime}  Native: {nativeTime}")
    nativeTime = benchWebsocketNative(4)
    dynamicTime = benchWebsocketDynamic(N)
    print(f"Websocket: Dynamic: {dynamicTime}  Native: {nativeTime}")

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
print(jsonStr)

def benchJSONDynamic(n:int) -> float:
    jsonUTF8 = jsonStr.encode('utf-8')
    start = time.time()
    for i in range(n):
        library.parsejson(jsonUTF8) 
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
        library.helloWorld() 
    end = time.time()
    return (end - start)/n

def benchHelloNative(n:int) -> float:
    start = time.time()
    for i in range(n):
        print("hello world")
    end = time.time()
    return (end - start)/n  

kilobytes = 64
wsData = ("HelloWorld"*(1000*kilobytes)).encode('utf-8')
wsData = bytearray(wsData)

def benchWebsocketNative(n:int) -> float:
    start = time.time()
    key = 1231242
    for i in range(n):
        key = wstx(key, wsData)
    end = time.time()
    return (end - start)/n

def benchWebsocketDynamic(n:int) -> float:
    ubuffer =  (ctypes.c_ubyte * len(wsData)).from_buffer(wsData)
    start = time.time()
    key = ctypes.c_int(12334)
    for i in range(n):
        key = library.websocketTransform(key, ubuffer, ctypes.c_int(len(wsData)))
    end = time.time()
    return (end - start)/n

def wstx(key:int, data:bytearray) -> int:
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




