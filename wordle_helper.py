# python3

def get_5_letter_words():
  with open("corncob_lowercase.txt", 'r') as all_words_file, open("words_5letters.txt", 'w') as words_5letters_file:
    all_words = all_words_file.read().split('\n')
    for word in all_words:
      if len(word) == 5:
        words_5letters_file.write(word + '\n')

def suggest_words():
  exclude_letters = set(['r', 'k', 'l', 'c', 'n'])
  include_letters = set(['b', 'a', 'e'])
  exclude_positions = [
    set(['b']),
    set([]),
    set(['e', 'a']),
    set(['a']),
    set(['e']),
  ]

  with open('words_5letters.txt', 'r') as words_5letters_file:
    words_5letters = words_5letters_file.read().split('\n')
    num_include_letters = len(include_letters)

    for word in words_5letters:
      word = word.lower()
      skip_word = False
      word_set = set(word)

      if len(word_set.intersection(exclude_letters)) > 0:
        continue

      if len(word_set.intersection(include_letters)) != num_include_letters:
        continue

      for i, letter in enumerate(word):
        if letter in exclude_positions[i]:
          skip_word = True
          break
      if skip_word:
        continue

      print(word)

def suggest_words_interactive():
  exclude_letters = set([])
  include_letters = set([])
  exclude_positions = [
    set([]),
    set([]),
    set([]),
    set([]),
    set([]),
  ]

  words_5letters = None
  with open('words_5letters.txt', 'r') as words_5letters_file:
    words_5letters = words_5letters_file.read().split('\n')

  while True:
    exclude_letters_new_ip = input("\nWhich new letters must be excluded in the word? (separate with space): ")
    exclude_letters_new = exclude_letters_new_ip.split()
    exclude_letters.update(exclude_letters_new)

    include_letters_new_ip = input("\nWhich new letters must be included in the word? (separate with space): ")
    include_letters_new = include_letters_new_ip.split()
    include_letters.update(include_letters_new)
    num_include_letters = len(include_letters)

    for pos in range(5):
      exclude_pos_new_ip = input("\nWhich new letters must be excluded in position {}? (separate with space): ".format(pos+1))
      exclude_pos_new = exclude_pos_new_ip.split()
      exclude_positions[pos].update(exclude_pos_new)

    print("\nSuggested words are:")

    for word in words_5letters:
      word = word.lower()
      skip_word = False
      word_set = set(word)

      if len(word_set.intersection(exclude_letters)) > 0:
        continue

      if len(word_set.intersection(include_letters)) != num_include_letters:
        continue

      for i, letter in enumerate(word):
        if letter in exclude_positions[i]:
          skip_word = True
          break
      if skip_word:
        continue

      print(word)

    should_continue = input("\nContinue? (Enter 'n' to exit): ")
    if should_continue.strip().lower() == 'n':
      break

#get_5_letter_words()
#suggest_words()
suggest_words_interactive()

