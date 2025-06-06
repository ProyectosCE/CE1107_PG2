import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.register_file import RegisterFile

# Módulos de prueba para RegisterFile
def test_basic_rw():
    rf = RegisterFile()
    rf.write("x1", 10)
    assert rf.read("x1") == 10

def test_x0_behavior():
    rf = RegisterFile()
    rf.write("x0", 999)
    assert rf.read("x0") == 0

def test_reset():
    rf = RegisterFile()
    rf.write("x3", 77)
    rf.reset()
    assert rf.read("x3") == 0

def test_invalid_register():
    rf = RegisterFile()
    try:
        rf.read("x33")
        assert False, "Expected ValueError for x33"
    except ValueError:
        pass

if __name__ == "__main__":
    print("Probando RegisterFile...")
    test_basic_rw()
    test_x0_behavior()
    test_reset()
    test_invalid_register()
    print("Todos los tests pasaron correctamente.")
