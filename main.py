import tkinter as tk
from tkinter import filedialog
import re
import csv
import wikipedia
import requests
import shutil
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from PIL import Image
import warnings
import webbrowser

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#used to hold all posts
images=[]
#Class used to put art peices in different classes depending on their price. Just compare given price to 3 different values and
# then returns class.
def class_cal(price):
    if(int(price)<=20):
        return 'lowerclass'
    if(int(price)>20 and int(price)<100):
        return 'middleclass'
    if(int(price)>=100):
        return 'upperclass'

#created a class post so that a data type would represent each post
class Post:
    def __init__(self, title, path, tags, price):
        self.title = title
        self.path = path
        self.tags = tags
        self.price = price
        self.classtype = class_cal(price)
        #prints all contents of the class, testing purposes only
    def show(self):
        print("Title", self.title)
        print("Path", self.path)
        print("Tags", self.tags)

#asks user to input tags they want to relate to the image
def assign_tags():
    #store a list properly in CVS files
    tags = input("What hashtags would you like? Please ensure you put a # in front of each word other wise it wont be counted").lower()
    aligned_tags=re.findall(r"#(\w+)", tags)
    if tags =="":
        return " / "
    for i in range(len(aligned_tags)):
      aligned_tags[i]=word_filter(aligned_tags[i])
    return '/'.join(aligned_tags) + "/"

#Asks for the path to the image, then the  title and price of it
#pushes file to the CSV file/datavbase
def upload():
#assign the path the users choses[1] and then the tags they chose[2]
    Path=filedialog.askopenfilename()
    Title=input("What the title? ")
    Price=input("What the price as a whole number ? £ ")

    p1 = Post(Title, Path, assign_tags(), Price)
    images.append([p1.title, p1.path, p1.tags])
    write_db(p1.title, p1.path, p1.tags, p1.price, p1.classtype)

#seaches list of all images and then printsout ones that match the title
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

#code that writes to the database/CSV file
def write_db(title, path, tags, price, classtype):
    with open('database.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title, path, ("".join(''.join(tags).split())), price, classtype])

#converts the tag section of each post from the CSV file to an array, as commas do work too well with CSV file
def tags_to_list():
    for i in images:
        #images[i][2]=', '.join(images[i][2]).split()
        x=', '.join(i[2]).split('/')
        for e in range(len(x)):
            x[e]=x[e].replace(',','')
            x[e]=x[e].replace(' ','')

        i[2]=x
   # print(images)

#opens up the CSV file to be read
def read_file():
    with open('database.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            li = list(' '.join(row).split(" "))
            le=li[0].split(",")
            images.append(le)
    if(len(images)==0):
        print("Please add a post before you complete anything else")
        print("Please select the picture you wish to post")
        upload()
    tags_to_list()

   #SHows a list of all post to veiw so user can pick one to veiw in more depth
def show():
    print()
    for i in range(len(images)):
        print(images[i][0])
    print()
    search_title()

 #code that webscapes off wikipedia for a definition of each tag used to show the user
def wiki_search(title):
    print()
    warnings.filterwarnings("ignore")
    try:
        page = wikipedia.page(title)
        print(page.summary)
    except:
        topics = wikipedia.search(title)
        choice = 1
        assert choice in range(len(topics))
        print(wikipedia.summary(topics[choice]))
    print()

    #used to search through each tag on each post to compare to the. one the user is searching for if found it will display info on each images
def search_tag():
    choice = input("Which post do you want to view (tag)? ")
    wiki_search(choice)
    FOUND=False
    tag_list=[]
    for i in range(len(images)):
            for x in images[i][2]:
               if (x == choice):
                   FOUND=True
                   tag_list.append(images[i])
                   print("Tag Found!")
    if(FOUND==False):
        print("There are no posts with this hashtag! ")
    if(FOUND==True):
        open_choice = input("Would you like to view a post? ")
        if(open_choice == 'yes'):
            for i in range(len(tag_list)):
                print(i, tag_list[i])
                print()
            num_choice = input("type the number assigned to the post you  wish  to see? ")
            img = Image.open(images[int(num_choice)][1])
            img.show()

            #seaches through each posts title to see if it matches the search term the user set
def search_title():
    choice = input("Which post do you want to view (title)? ")
    found_image=0
    for i in range(len(images)):
        if (images[i][0] == choice):
            found_image=i
            print("Title: ", images[i][0])
            print("Path: ", images[i][1])
            print("Tags: ", images[i][2])
            print("Price: ", images[i][3])
            print("Class: ", images[i][4])
    choice = input("Do you wish to open the image? ").lower()
    choice2= input("Do you wish to view in mark up language HTML ?").lower()

    if (choice == 'yes'):
        print("SHOWING...")
        img = Image.open(images[found_image][1])
        img.show()

    if (choice2== "yes"): # s1e of higher mark up language, machine readable is where file saved as csv
        import tempfile
        import webbrowser
        HTML = """
        <html>
        <style>
		body {background-color: powderblue;}
		p    {color: green;}
		</style>
		<p>Your title is ...... 

        		Title: %s
        		</p>

        </html>
        """
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as x: # creates temp file
            link = 'file://' + x.name #location of temp file
            x.write(HTML % (images[i][0])) #writes temp file, then passes title
        webbrowser.open(link) #default browser opened , and displayed.

#filters out rude words from a list that the user tries to add into their tags
def word_filter(UserWords):
    def ReadWords():
        rudewords = []
        txt = open('list.txt', 'r')
        for word in txt:
            word = word.strip()
            rudewords.append(word)
        return rudewords

    rudewords = ReadWords()

    # If word found then it is replaced with *
    for i in rudewords:
        if i in UserWords:
            UserWords = UserWords.replace(i, '*' * len(i))

    return UserWords
#what is show on the start up of the app, also initiated read from file to get all stored posts
def init():
    read_file()
    print("Hi. Welcome to the SMARTIST terminal application!")
    main()

def main():
#displays all options the user can choice from
    print("SHOW         -Show all art pieces")
    print("ADD          -Upload an art piece")
    print("SEARCHTAG    -Searches art looking for tags")
    print("SEARCHTITLE  -Searches art looking for title")


    choice = input("What would you like to do? ").upper()

    if(choice == 'SHOW'):
        show()
    if (choice == 'ADD'):
        upload()
    if(choice == 'SEARCHTAG'):
        search_tag()
    if (choice == 'SEARCHTITLE'):
        search_title()

    main()

init()
