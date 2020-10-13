import os
from parser import *

PATH = 'tests'

tests = os.listdir(PATH)


def test():
    passed = 0
    testsnum = 0
    for file in tests:
        print("Filename: " + str(file))
        ok = True
        try:
            File = PATH + '/' + file
            with open(File, "r") as f:
                data = f.read()
            parser.parse(data)
        except SyntaxError:
            ok = False
        if file[0] == 'a' and not ok:
            print("Test failed")
            testsnum += 1
        elif file[0] == 'r' and ok:
            print("Test failed")
            testsnum += 1
        else:
            print("Test passed")
            passed += 1
            testsnum += 1
        print("")
    print("%d/%d tests passed" % (passed, testsnum))


if __name__ == "__main__":
    test()
