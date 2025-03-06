import pickle 

data = []

for i in range(20):
    data.append(i)

with open('data.pkl', 'wb') as file:
    pickle.dump(data, file)

with open('data.pkl', 'rb') as file_loaded:
    print(pickle.load(file_loaded))

