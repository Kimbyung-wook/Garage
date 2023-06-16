import sys
sys.path.append(r"E:\MyNote\Garage\DesignPattern\Singleton")

from Singleton import SingletonType

class Earth(metaclass=SingletonType):
    def __init__(self):
        self.__radius = 6483000
        self.__year2day = 365.24
        self.__day2hour = 24.0000
        self.__number = 0

    def getRadius(self):
        return self.__radius

    def showSiderealPeriod(self):
        print("Sidereal Period of Earth is {:6.2f} days per a year\n".format(self.__year2day))

    def setNumber(self, input:int):
        self.number = input

    def getNumber(self):
        return self.number

if __name__ == "__main__":
    earth1 = Earth()
    earth2 = Earth()

    earth1.showSiderealPeriod()
    earth1.setNumber(1)
    print("Earth1 : {:d}".format(earth1.getNumber()))
 
    earth2.showSiderealPeriod()
    print("Earth2 : {:d}".format(earth2.getNumber()))
    print("Earth1 : {:d}".format(earth1.getNumber()))
