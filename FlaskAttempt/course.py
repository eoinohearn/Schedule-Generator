class Course: 

    def __init__(self, name, credits, preReq = [], coReq = []) -> None:
        self.name = name
        self.credits = int(credits)
        self.preReq = self.makeList(preReq)
        self.coReq = self.makeList(coReq)

    def __str__(self) -> str:
        a = "Class: "
        b = "Credits: "
        c = "Prerequisites: "
        d = ""
        for i in self.preReq:
            d += i + " "
        return a + self.name + "\n" + b + str(self.credits) + "\n" + c + d + "\n"

    def makeList(self, str: str):
        sublist = []
        sublist.append(str)

        for el in range(len(sublist)):
            if " " in sublist[el]:
                tempList = sublist[el].split()
                sublist.clear()
                for i in tempList:
                    sublist.append(i)

        return sublist