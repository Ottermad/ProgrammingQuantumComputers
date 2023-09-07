N = 15
precision_bits = 4
coprime =2

work = 1

max_loops = 2**precision_bits

i = 0
while i < max_loops:
    work = (work * coprime) % N
    if work == 1:
        print("found")
        print(i + 1)
        break

    i+=1