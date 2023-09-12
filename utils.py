
def get_header():
    with open("myheader.txt", "r") as f:
        line = f.readline()
        return eval(line.strip())