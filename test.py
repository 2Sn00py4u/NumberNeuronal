with open("traindata\\train_numbers.csv") as file:
    for i, line in enumerate(file):
        print(f"{i}: {line}")