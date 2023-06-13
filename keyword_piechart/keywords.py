import re
from collections import Counter
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------INTRO
"""
NAME: word_stats.py
AUTHOR: matt rayner

DESCRIPTION: Creates a pie chart of most commonly used words in a given simple
             "word_file.txt" file, excluding words in a "filter_list.txt".
             NOTE: update filter_list.txt for your own file, as the list
             provided is very limited

USAGE: no command line arguments or user input at runtime. Change/add words to
       "filter_list.txt" manually (separated by a space). Copy and paste the
       text you wish to analyse into "word_file.txt"
"""

#------------------------------------------------------------------------SET UP

#common words to avoid
filter_file = open("filter_list.txt", "r")
filterlist = filter_file.read().split()

#input text as simple text string to evaluate
text_file = open("word_file.txt", encoding="utf-8")
text = text_file.read()

#----------------------------------------------------------------FILTER + COUNT

#remove all but alphabetical characters
text = re.sub(r'[^a-zA-Z ]', '', text)

#convert to list of lower case words
words = list(text.lower().split())

#filter words
words_filt = []
for word in words:
  if word not in filterlist:
    words_filt.append(word)

#make list of words and count
counts = Counter(words_filt).most_common(10)

#----------------------------------------------------------------------MAKE PIE

labels = [i[0] for i in counts]
sizes = [i[1] for i in counts]
explode = [0] * len(counts)
explode[0] = 0.1
plt.pie(sizes, explode = explode, labels = labels, 
        autopct='%1.1f%%', shadow=False, startangle=140)
plt.axis('equal')
plt.savefig('pie.png')
