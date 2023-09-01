array = [1, 3, 5]

total = sum(array)

output = {}

for index, item in enumerate(array):
    output[bin(index)] = item / total

print(output)