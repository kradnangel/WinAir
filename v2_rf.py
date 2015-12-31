import math
import csv
from collections import defaultdict
import datetime

### read .csv file and return a list of list, a line in file is a list.
def readCSV(filename):
    data = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data = map(lambda row: (''.join(row)).split(','), spamreader)
    print "Reading Done!"
    titles = data[0]
    return titles, data[1:]

def collect(titles, data):
    ttSets = defaultdict(set)
    for d in data:
        for i in [4] + range(6, len(titles)): # for i in xrange(len(titles)):
            title = titles[i]
            item = d[i]
            ttSets[title].add(item)
    return ttSets

def imap(ttSets):
    itemMap = defaultdict(dict)
    for title in ttSets:
        for i in xrange(len(ttSets[title])):
            itemMap[title][ttSets[title].pop()] = i
    return itemMap

## preprocess the train data
def preprocess(titles, raw, iiMaps, base):
    dac = datetime.date(2010,6,27)
    dfb = datetime.date(2010,1,1)
    tfa = 20090219043255
    data, X, y = [],[],[]
    j = base
    for row in raw:
        d = []
        for i in xrange(len(titles)):
            title = titles[i]
            item = row[i]
            if title == 'id':   #0
                new, j = j, j+1
            elif title == 'date_account_created':   #1
                year = int(item[0:4])
                month = int(item[5:7])
                day = int(item[8:10])
                now = datetime.date(year, month, day)
                new = (now - dac).days           
                new = d.pop(); ###
            elif title == 'date_first_booking': #3
                if len(item) < 10:
                    new = 0
                else:
                    year = int(item[0:4])
                    month = int(item[5:7])
                    day = int(item[8:10])
                    now = datetime.date(year, month, day)
                    new = (now - dfb).days
                new = d.pop();###
            elif title == 'timestamp_first_active': #2
                new = int(item) - tfa
            elif title == 'age': #5
                if item == '':
                    age = 0
                else:
                    age = int(float(item))
                if 10 < age < 120:
                    new = age
                elif age in xrange(1900,2000):
                    new = 2015 - age
                else:
                    new = 0
            else:
                new = iiMaps[title][item]
            d.append(new)
        data.append(d[:])
        X.append(d[:13])
        if len(d) > 13: y.append(d[13])
    print 'preprocess done!'
    return X, y, data

def writeCSV(filename, title, users, content):
    writer = open(filename,'w')
    writer.write(title + '\n')
    for i in range(len(content)):
        writer.write(users[i]+','+str(content[i]) + '\n')
    writer.close()
    print "Finished writing!"

### read training data from csv
titles, rawData = readCSV('train_users_2.csv')
n, m = len(rawData), len(titles)
print titles
print n, m

### read testing data from csv
testTitles, testRaw = readCSV('test_users.csv')

### collect all items in each field
ttSets = collect(titles, rawData)
ttSets2 = collect(testTitles, testRaw)
for tt in ttSets2:
    ttSets[tt] = ttSets[tt] | ttSets2[tt]
    # print tt, ttSets[tt]

### map item and index in each field
itemMap = imap(ttSets)
# for ii in itemMap:
    # print ii, itemMap[ii]

### preprocess
X, y, data = preprocess(titles, rawData, itemMap, 0)
print "After preprocess"

### divide the data into training data and validation data
bound = n / 10 * 9
X_train = X[:bound]
X_valid = X[bound:]
y_train = y[:bound]
y_valid = y[bound:]

### Random Forest
from sklearn.ensemble import RandomForestClassifier
estimator = RandomForestClassifier(n_estimators=100, n_jobs = -1, max_features = 'sqrt')
estimator.fit(X_train, y_train)

### Training error
from sklearn.metrics import mean_squared_error
yp_train = estimator.predict(X_train)
print 'Training error', sum(map(lambda y,yp: y != yp, y_train, yp_train)) * 1.0 / bound

### Validation error
yp_valid = estimator.predict(X_valid)
print 'Validation error', sum(map(lambda y,yp: y != yp, y_valid, yp_valid)) * 1.0 / (n-bound)

### Testing data
X_test, _, testData = preprocess(testTitles, testRaw, itemMap, n+1)
yp_test = estimator.predict(X_test)
countryMap = {}
for key in itemMap['country_destination']:
    countryMap[itemMap['country_destination'][key]] = key
writeCSV('submit.csv', 'id,country', [d[0] for d in testRaw], map(lambda y:countryMap[y], yp_test))

