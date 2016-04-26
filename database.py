import sqlite3


class DBDriver:
    def connectDb(self):
        self.conn = sqlite3.connect('keystroke.db')
        self.cursor = self.conn.cursor()
        print "Opened database successfully"

    def getTables(self):
        self.cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        return list(self.cursor.fetchall())

    def getListing(self,tablename):
        querystr = "SELECT * FROM "+tablename
        self.cursor.execute(querystr)
        return list(self.cursor.fetchall())

    def getdesc(self):
        querystr = "SELECT * FROM sqlite_master"
        self.cursor.execute(querystr)
        return list(self.cursor.fetchall())

    def gettopusers(self,top = 11):
        querystr = "SELECT user_id , COUNT(keystroke_datas_id) as count FROM keystroke_typing GROUP BY user_id HAVING success = '1' ORDER BY count DESC LIMIT "+str(top);
        self.cursor.execute(querystr)
        return list(self.cursor.fetchall())

    def createdataset(self, users):

        for user in users:

            filepath1 = "data/train/"+str(user)+".txt"
            filepath2 = "data/test/" + str(user) + ".txt"
            trainfile = open(filepath1,'w')
            testfile = open(filepath2, "w")
            querystr = "SELECT kd.ppTime,kd.time_to_type FROM keystroke_datas as kd , keystroke_typing as kt WHERE kt.user_id = kd.user_id AND kt.keystroke_datas_id = kd.id AND kt.user_id = "+str(user)
            self.cursor.execute(querystr)
            rows = list(self.cursor.fetchall())

            index = 0
            for row in rows:
                index = index + 1

                if index <= 50:
                    content = str(row[0]) + " " + str(row[1]) + " " + str(1) + "\n"
                    trainfile.write(content)
                else:
                    content = str(row[0]) + " " + str(row[1]) + "\n"
                    testfile.write(content)

            file = "train.txt"
            mix = open(file, "r+")
            for i in mix:
                trainfile.write(i)

            file = "test.txt"
            mix = open(file, "r+")
            for i in mix:
                testfile.write(i)
        trainfile.close()
        testfile.close()



    def closeDb(self):
        self.conn.close()








