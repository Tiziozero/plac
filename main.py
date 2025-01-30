#!/usr/bin/python3
import sys

class Emulator:
    def __init__(self, lines):
        self.__memory = [None for _ in range(1024)]
        self.__length = len(self.__memory)
        self.__vars = {}
        self.__stack_ptr = 0
        self.__pc = 0
        self.__acc = 0

    def parse(self, lines, 

    def __repr__(self) -> str:
        return f"Acc: {self.__acc}\nPC: {self.__pc}\nStack Ptr: {self.__stack_ptr}\n"

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("Missing file")
        exit(0)

    filepath = args[1]
    with open(filepath) as f:
        lines = [l[:-1].split(" ") for l in f.readlines()]
        e = Emulator(lines)
        print(e, lines)
