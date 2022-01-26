words_5letters = None
with open('words_5letters_freq.txt', 'r') as words_5letters_file, open('wordslist.txt','w') as listfile:
  words_5letters = words_5letters_file.read().split('\n')
  for word in words_5letters:
    listfile.write("'" + word + "'," + "\n")
