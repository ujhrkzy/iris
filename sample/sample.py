print(150 // 150)
print(150 // 5)
print(150 // 3)
print(150 / 3)

print("------------")
skip = 150 // 40
print(skip)
output = [i for i in range(0, 150, skip)]
print(output)
output2 = [i % 2 for i in output]
print(output2)
output3 = [i % 3 for i in output]
print(output3)
