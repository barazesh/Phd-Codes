import pysd
import os
from pathlib import Path

def main():
    vensimDirectory='./Simulation Files/Prosumers & defectors'
    vensimFile ='net metering-no fixed tariff.mdl'
    filepath = Path(vensimDirectory,vensimFile)
    model = pysd.read_vensim(str(filepath))
    stocks = model.run()
    print(model.doc())


if __name__=='__main__':
    main()