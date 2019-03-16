import csv

path="data.csv"
data=[]
with open(path, newline='') as file:
	reader=csv.reader(file)
	for row in reader:
		datum=int(row[0])
		data.append(datum)
print(data)

print('after append')
print(data)

with open(path, 'w') as file:
	writer=csv.writer(file)
	print('write')
	for i in range(len(data)):
		writer.writerow([data[i]])
		
		print([data[i]])
		
data=[]
print('relod')
print(data)
with open(path, newline='') as file:
	reader=csv.reader(file)
	for row in reader:
		datum=int(row[0])
		data.append(datum)
print(data)
print(data[3:])

