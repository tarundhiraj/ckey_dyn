from database import DBDriver

class Util:
    def printData(self,data, multi = False):
        if multi:
            for row in data:
                for r in row:
                    print r
        else:
            for d in data:
                print data

    def printList(self, data):
        for d in data:
            print d

    def getuserlist(self, users):
        userlist = []
        for user in users:
            userlist.append(user[0])
        return userlist

    def runtest(self):

        driver = DBDriver()
        driver.connectDb()

        tables = driver.getTables()
        self.printList(tables)

        # rows = driver.getListing("users")
        # util.printList(rows)
        # rows = driver.getdesc()
        # util.printList(rows)

        # rows = driver.getListing("keystroke_datas")
        # util.printList(rows)

        users = driver.gettopusers(top=21)
        #print users
        self.userlist = self.getuserlist(users)
        self.userlist.remove(1)
        self.printList(self.userlist)
        driver.createdataset(self.userlist)
        driver.closeDb()

    def getusers(self):
        return self.userlist