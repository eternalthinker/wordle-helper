import random

def words_to_comma_list(src, randomize=False):
  with open(src, 'r') as words_letters_file,\
      open("comma_" + src,'w') as listfile:
    words_letters = words_letters_file.read().split('\n')
    if randomize:
      random.shuffle(words_letters)
    for word in words_letters:
      if word == "":
        continue
      listfile.write("'" + word + "'," + "\n")

#words_to_comma_list("words_6letters.txt", randomize=False)
#words_to_comma_list("words_6letters_freq.txt", randomize=True)
words_to_comma_list("all_words_6.txt", randomize=False)
