with open("traindata\\train_numbers.csv") as file:
    for i, line in enumerate(file):
        print(f"{i}: {line}")
        
        
liste = [(25,0),(1,30),(69,2),(3,33),(4,30)]
liste.sort(reverse=True)
print(liste)