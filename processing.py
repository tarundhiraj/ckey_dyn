import csv
import sys

csv.field_size_limit(sys.maxsize)

def csv_writer(data, path):

    with open(path, "wb") as csv_file:

        writer = csv.writer(csv_file, delimiter=',')

        for line in data:

            writer.writerow(line)


def create_duration_file():

    with open('data/processed.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        index = 0
        list = []

        for row in readCSV:
            idx = 1
            anotherList = []
            for i in xrange(0, len(row), 2):
                if idx == 1:
                    anotherList.append(row[i])
                if idx < 3:
                    idx += 1
                    continue

                try:
                    c = row[i].split(" ")[0]
                    n = row[i + 1].split(" ")[0]
                    diff = float(n) - float(c)
                    anotherList.append(diff)
                    print diff
                except:
                    continue

            list.append(anotherList)

        path = "output/duration.csv"

        csv_writer(list, path)


def create_latency_file():

    with open('data/processed.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        index = 0
        list = []

        for row in readCSV:

            anotherList = []
            anotherList.append(row[0])
            for i in xrange(3, len(row), 2):

                try:
                    c = row[i].split(" ")[0]
                    n = row[i + 1].split(" ")[0]
                    diff = float(n) - float(c)
                    anotherList.append(diff)
                    print diff
                except:
                    continue

            list.append(anotherList)

        path = "output/latency.csv"

        csv_writer(list, path)


if __name__ == "__main__":
    create_duration_file()
    create_latency_file()


