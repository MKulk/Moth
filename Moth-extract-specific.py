from Classes.viewer import reader
import sys
import os






try:
    file = sys.argv[1]
    try:
        materials=list(sys.argv[2].split(','))
    except:
        print("no materila argument provided! Why are you even using it then?")
        os.exit(1)
except:
    print("No filename is provided")
    os.exit(1)
   
if __name__ == "__main__":
    data=reader(file)
    data.GetMHonT(filter=materials)
    data.GetMTonH(filter=materials)
