#[pymodule]
import ctypes

library = ctypes.cdll.LoadLibrary(__file__.replace("__init__.py","go.so"))

def hello_world():
    library.helloWorld()

def add(a:int,b:int) -> int:
    return int(library.add(ctypes.c_int(a), ctypes.c_int(b)))

def wstx(key:int, data:bytearray) -> int:
    ubuffer =  (ctypes.c_ubyte * len(data)).from_buffer(data)
    return int(library.websocketTransform(ctypes.c_int(key), ubuffer, ctypes.c_int(len(data))))

def parse_person(data:bytes):
    library.parsePerson(data)


