import wikipedia
import warnings

warnings.filterwarnings("ignore")
title = input("What do you want to look up?: ")
try:
    page = wikipedia.page(title)
    print(page.summary)
except:
    topics = wikipedia.search(title)
    choice = 1
    assert choice in range(len(topics))
    print(wikipedia.summary(topics[choice]))


