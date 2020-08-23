import random

wordlist = []
special_char = ['!','@','#','$','%','*','&']

with open("readable_pass.txt",'r') as file:
    data = file.readlines()

    for line in data:
        words = line.split()

        for item in words:
            if len(item) > 5:
                wordlist.append(item.capitalize())

word = random.choice(wordlist)
schar = random.choice(special_char)
num = str(random.randint(10,99))

psw = word+schar+num
print(psw)