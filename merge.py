import pickle

filename = input('Enter base name of files to merge: ')
index = 1

data = []

while True:
    try:
        file = open(filename + str(index) + '.barnes','rb')
        print("Opened file " + filename + str(index))
        index += 1
        temp = pickle.load(file)
        data += temp
        file.close()
    except:
        print('Ended trying to open file ' + str(index))
        break

file = open(filename+'Merge1.barnes','wb')
pickle.dump(data,file,protocol=2)
file.close()
