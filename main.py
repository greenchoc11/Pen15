import tkinter as tk
from tkinter import filedialog
import re
import csv

images=[]
root = tk.Tk()
root.withdraw()

def class_cal(price):
    if(price<20):
        return 'lowerclass'
    if(price>20 and price<100):
        return 'middleclass'
    if(price>100):
        return 'upperclass'

class Post:
    def __init__(self, title, path, tags, price):
        self.title = title
        self.path = path
        self.tags = tags
        self.price = price
        self.classtype = class_cal(price)
    def show(self):
        print("Title", self.title)
        print("Path", self.path)
        print("Tags", self.tags)

def assign_tags():
    #store a list properly in CVS files
    tags = input("What hashtags would you like? ")
    return re.findall(r"#(\w+)", tags)

def upload():
#assign the path the users choses[1] and then the tags they chose[2]
    Path=filedialog.askopenfilename()
    Title=input("What the title? ")
    Price=input("What the price? ")

    p1 = Post(Title, Path, assign_tags(), Price)
    images.append([p1.title, p1.path, p1.tags])
    write_db(p1.title, p1.path, p1.tags, p1.price, p1.classtype)

def search():
    title_search = input("What is the title of the image you are trying to find")
    found=False
    i=0
    for i in range(len(images)):
        print(images[i][0], " == ", title_search)
        if(images[i][0]==title_search):
            print(images[i])
            found=True
            i+=1

    if(found==False):
        print('Not found')

def write_db(title, path, tags, price, classtype):
    with open('database.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title, path, tags, price, classtype])

def read_file():
    with open('database.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            li = list(' '.join(row).split(" "))
            images.append(li)

def main():
    read_file()
    print(images)
    choice = input("What would you like to do? ")
    if(choice == 'upload'):
        upload()
        #images[0].show()
    if(choice == 'search'):
        search()
    main()

main()
