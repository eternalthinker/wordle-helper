# python3

def get_5_letter_words():
  with open("corncob_lowercase.txt", 'r') as all_words_file, open("words_5letters.txt", 'w') as words_5letters_file:
    all_words = all_words_file.read().split('\n')
    for word in all_words:
      if len(word) == 5:
        words_5letters_file.write(word + '\n')

def get_5_letter_words_freq_csv():
  with open("corncob_lowercase.txt", 'r') as all_words_file,\
      open("unigram_freq.csv", 'r') as freq_words_file,\
      open("words_5letters_freq.txt", 'w') as words_5letters_file:
    all_words = all_words_file.read().split('\n')
    all_5letter_words = [word for word in all_words if len(word) == 5]
    
    word_freq_map = {}
    all_freq_lines = freq_words_file.read().split('\n')
    for line in all_freq_lines:
      if line.strip() == '':
        continue
      word, freq = line.split(',')
      if len(word) == 5:
        word_freq_map[word] = int(freq)
    
    def get_word_freq(w):
      if w in word_freq_map:
        return word_freq_map[w]
      return 0
    
    all_5letter_words.sort(reverse=True, key=get_word_freq)
    for word in all_5letter_words:
      words_5letters_file.write(word + '\n')
    

common_letters_map = {
  'e': 11.16,
  'a': 8.45,
  'r': 7.58,
  'i': 7.54,
  'o': 7.16,
  't': 6.95,
  'n': 6.65,
  's': 5.74,
  'l': 5.49,
  'c': 4.54,
  'u': 3.63,
  'd': 3.38,
}

def get_common_letter_score(word):
  score = 0
  # Push plurals down to the bottom
  if word.endswith('s'):
    return score
  for letter in word:
    if letter in common_letters_map:
      score += common_letters_map[letter]
  return score

def get_suggested_words(words_5letters, exclude_letters, exclude_positions, include_positions, limit=25):
  include_letters = set()
  for wrong_pos_letter_set in exclude_positions:
    include_letters |= wrong_pos_letter_set
  num_include_letters = len(include_letters)
  
  suggested_words = []
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

    for i, letter in enumerate(word):
      if include_positions[i] is not None and letter != include_positions[i]:
        skip_word = True
        break
    if skip_word:
      continue
    suggested_words.append(word)
  
  for letter in exclude_letters:
    if letter in common_letters_map:
      del common_letters_map[letter]

  selected_suggested_words = suggested_words[:25]
  selected_suggested_words.sort(reverse=True, key=get_common_letter_score)
  return suggested_words, selected_suggested_words


def suggest_words():
  exclude_letters = set(['r', 'k', 'l', 'c', 'n'])
  exclude_positions = [
    set(['b']),
    set([]),
    set(['e', 'a']),
    set(['a']),
    set(['e']),
  ]
  include_positions = [
    None,
    None,
    'b',
    None,
    None,
  ]

  with open('words_5letters.txt', 'r') as words_5letters_file:
    words_5letters = words_5letters_file.read().split('\n')
    print_suggested_words(words_5letters, exclude_letters, exclude_positions, include_positions)

def suggest_words_interactive():
  exclude_letters = set([])
  exclude_positions = [
    set([]),
    set([]),
    set([]),
    set([]),
    set([]),
  ]
  include_positions = [
    None,
    None,
    None,
    None,
    None,
  ]

  words_5letters = None
  with open('words_5letters_freq.txt', 'r') as words_5letters_file:
    words_5letters = words_5letters_file.read().split('\n')

  suggested_words = None
  while True:
    exclude_letters_new_ip = input("\nWhich new letters must be EXCLUDED in the word? (separate with space): ")
    exclude_letters_new = exclude_letters_new_ip.split()
    exclude_letters.update(exclude_letters_new)

    for pos in range(5):
      exclude_pos_new_ip = input("\nWhich new letters must be EXCLUDED in position {}? (separate with space): ".format(pos+1))
      exclude_pos_new = exclude_pos_new_ip.split()
      exclude_positions[pos].update(exclude_pos_new)

    for pos in range(5):
      include_pos_new_ip = input("\nWhich letter must be INCLUDED in position {}? (separate with space): ".format(pos+1))
      include_pos_new = include_pos_new_ip.strip()
      include_positions[pos] = None if include_pos_new == '' else include_pos_new

    print("\nSuggested words are:")
    words_list = words_5letters if (suggested_words is None) else suggested_words
    suggested_words, selected_suggested_words = get_suggested_words(
        words_list,
        exclude_letters,
        exclude_positions,
        include_positions,
    )
    for word in selected_suggested_words:
      print(word)

    should_continue = input("\nContinue? (Enter 'n' to exit): ")
    if should_continue.strip().lower() == 'n':
      break

#get_5_letter_words()
#get_5_letter_words_freq_csv()
#suggest_words()
suggest_words_interactive()

