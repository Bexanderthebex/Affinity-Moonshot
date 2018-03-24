

f = open('train.csv', 'r')
f.readline()
for line in f.readlines():
    print(line.strip())
    break