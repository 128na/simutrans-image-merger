import sys

def run():
    if(len(sys.argv) < 2):
        raise Exception("json file path not provided.")

    filename = sys.argv[1]


if(__name__ == '__main__'):
    run()
