class Defector:
    def __init__(self, initialNumber:int) -> None:
        self.__numberHistory = []
        self.currentNumber = initialNumber

    def ChangeNumber(self, value) -> None:
        self.__numberHistory.append(self.currentNumber)
        self.currentNumber = self.currentNumber + value
    
    def GetNumberHistory(self):
        return self.__numberHistory
