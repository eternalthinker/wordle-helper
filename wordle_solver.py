from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from wordle_helper import get_5letter_words, get_suggested_words
import time

CORRECT = "correct"
PRESENT = "present"
ABSENT = "absent"

class element_has_attribute(object):
  def __init__(self, element, attribute):
    self.attribute = attribute
    self.element = element

  def __call__(self, driver):
    return self.element.get_attribute(self.attribute) is not None

def solve_wordle():
  exclude_letters = set([])
  include_letters = set([])
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

  # Open website and get ready
  driver = webdriver.Chrome()
  driver.get("https://www.powerlanguage.co.uk/wordle/")
  game_tag = driver.execute_script('''
    return document
      .querySelector("game-app")
      .shadowRoot
      .querySelector("game-theme-manager")
      .querySelector("div#game");
  ''')

  # Close help popup
  close_button = driver.execute_script('''
    const gameTag = arguments[0];
    return gameTag
      .querySelector("game-modal")
      .shadowRoot
      .querySelector(".close-icon");
  ''', game_tag)
  close_button.click()

  # Get all empty row containers
  words_5letters = get_5letter_words()
  suggested_words = None
  attempt_count = 1
  current_row_idx = 0
  row_containers = game_tag.find_elements(By.CSS_SELECTOR, "div#board game-row")
  body = driver.find_element(By.CSS_SELECTOR, "body")

  # Game loop
  while True:
    words_list = words_5letters if (suggested_words is None) else suggested_words
    suggested_words, selected_suggested_words = get_suggested_words(
        words_list,
        exclude_letters,
        exclude_positions,
        include_positions,
        attempt_count,
    )

    # Enter word
    word = selected_suggested_words[0]
    print("Word attempt:", attempt_count, "->", word.upper())
    # actions = ActionChains(driver)
    # actions.send_keys(word)
    # actions.send_keys(Keys.ENTER)
    # actions.perform()
    body.send_keys(word)
    body.send_keys(Keys.ENTER)

    print("Waiting..")
    tiles = driver.execute_script('''
      const rowContainer = arguments[0];
      return rowContainer
        .shadowRoot
        .querySelectorAll("game-tile");
    ''', row_containers[current_row_idx])
    wait = WebDriverWait(driver, 10)
    wait.until(element_has_attribute(tiles[4], "evaluation"))
    # Extra time for keyboard state change
    # TODO: Change to webdriver wait
    time.sleep(2)

    # Update constraints
    correct_count = 0
    for i, tile in enumerate(tiles):
      letter = tile.get_attribute("letter")
      evaluation = tile.get_attribute("evaluation")
      print(letter, evaluation)
      if evaluation == CORRECT:
        correct_count += 1
        include_positions[i] = letter
        include_letters.update(letter)
      elif evaluation == PRESENT:
        exclude_positions[i].update(letter)
        include_letters.update(letter)
      elif evaluation == ABSENT:
        if letter in include_letters:
          exclude_positions[i].update(letter)
        else:
          exclude_letters.update(letter)

    if correct_count == 5:
      print("The solution is:", word)
      break;

    attempt_count += 1
    current_row_idx += 1
    if attempt_count > 6:
      print("Game over!")
      break

    #break

  # print('attempt out')
  # actions = ActionChains(driver)
  # actions.send_keys("robot")
  # actions.send_keys(Keys.ENTER)
  # actions.perform()
  # print("waiting..")
  # driver.implicitly_wait(5)

  input("Press any key to close..")
  driver.close()

solve_wordle()
