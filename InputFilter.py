# Reads txt file that you can add filter words to , then if they exist appends to the dictionary 
def ReadWords():
  rudewords = []
  txt = open('list.txt','r')
  for word in txt:
    word = word.strip()
    rudewords.append(word)
  return rudewords

rudewords= ReadWords()

#If word found then it is replaced with * 
UserWords = input(" Please Input ").lower()
for i in rudewords:
    if i in UserWords:
        UserWords = UserWords.replace(i, '*' * len(i))
print(UserWords)