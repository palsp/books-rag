import sys

class Logger:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        print(f"[{self.name}] {message}")
    
    def debug(self, message):
        if "--debug" in sys.argv:
            print(f"[{self.name}] {message}")
    