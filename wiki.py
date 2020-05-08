import wikipedia
import warnings


warnings.filterwarnings("ignore")

title = input("What do you want to look up?: ")
try:
    page = wikipedia.page(title, auto_suggest=False)
    print(page.summary)
except:
    topics = wikipedia.search(title)
    print("May refer to: ")
    for i, topic in enumerate(topics):
        print(i, topic)
    choice = int(input("Enter a choice: "))
    assert choice in range(len(topics))
    print(wikipedia.summary(topics[choice]))
