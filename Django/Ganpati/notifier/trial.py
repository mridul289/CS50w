class helo():
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def getname(self):
        """returns the name of the object"""
        return self.name

m = helo('Mridul', 'MIT')
print(m.getname())

import datetime as dt

print(str(dt.date.today()))