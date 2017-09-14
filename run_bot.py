import sys
import importlib

if __name__ == "__main__":
    bot = sys.argv[1]
    name = "bots." + bot
    mod = importlib.import_module(name)
    mod.run(*sys.argv[2:])