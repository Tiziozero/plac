#!/usr/bin/python3
import sys
from typing import List

class Emulator:
    def __init__(self, lines):
        self.__memory = [None for _ in range(1024)]
        self.__length = len(self.__memory)
        self.__vars = {}
        self.__stack_ptr = 0
        self.__pc = 0
        self.__acc = 0
        self.parse(lines)

    def parse(self, lines):
        print("Purified Lines")

        clean_lines = []
        for line in lines:
            # print(f"{line=}")
            line.strip("\n")
            line = line.split(" ")
            if "--" in line:
                line = line[:line.index("--")]

            line = list(filter(lambda x: x.strip(), line))
            if len(line) > 0:
                print(line)
                clean_lines.append(line)
            ...
    def __repr__(self) -> str:
        return f"Acc: {self.__acc}\nPC: {self.__pc}\nStack Ptr: {self.__stack_ptr}\n"

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("Missing file")
        exit(0)

    filepath = args[1]
    with open(filepath) as f:
        lines = [l.strip('\n') for l in f.readlines()]
        
        print("lines:",lines)
        e = Emulator(lines)
