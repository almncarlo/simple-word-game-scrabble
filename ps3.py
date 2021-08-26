import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # initializes word string all in lowercase
    w = word.lower()
    # first case of second component
    second_score = 7*len(w) - 3*(n-len(w))
    total_score = 0
    # if there are no letters in word, automatically return 0 score
    if len(w) == 0:
        total_score = 0
    # for each char in word, determine score from given dictionary
    for char in w:
        total_score += SCRABBLE_LETTER_VALUES[char]
    # if first case is greater than 1, multiply it to total score
    if second_score > 1:
        total_score *= second_score
    # if first case is less than 1, multiply 1 total score
    else:
        total_score *= 1
    return total_score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    #take one slot from vowels
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    #replace taken slot with an asterisk as a wildcard
    hand['*'] = 1

    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # creates copy of hand dictionary
    new_hand = hand.copy()
    # iterates over each letter in lowercase word
    for char in word.lower():
        # .get() returns value of key which in this case is char
        # for each char in new_hand dictionary used in word.lower(),
        # subtract one to its value and set it to new_hand[char]
        new_hand[char] = new_hand.get(char,0) - 1
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # valid word -> must be in word_list and is composed of letters available from hand
    # sets input words to all lower cases
    new_word = word.lower()
    new_new_word = new_word
    f = 0
    # if word does not have an '*'
    if new_word in word_list:
            for char in new_word:
                # if char is in hand and occurs in hand more than or
                # equal to in the word itself, add 1 to counter, else
                # return false
                if char in hand and hand[char] >= new_word.count(char):
                    f += 1
                else:
                    return False
            # if f counter is equal to length of the word,
            # that means every character in the word is in hand
            # and is available in dictionary
            if f == len(new_word):
                return True
    # if word is not in word_list initially (check for wildcard case)
    else: 
        # if word has '*' wildcard in it
        if '*' in new_word:
            # iterates through each vowel
            for x in VOWELS:
                # set w as word to replace wildcard with vowel in iteration
                w = new_word.replace('*', x)
                # if w is in word_list, return True
                if w in word_list:
                    return True
        # if the word is not in word_list and does not have a wildcard,
        # return false since it is invalid
        else:
            return False



def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    num_letters = 0
    for x in hand:
        if hand[x] > 0:
            num_letters += 1
    return num_letters



def play_hand(hand, word_list, num_hands):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print('Current Hand:')
        display_hand(hand)
        # Ask user for input
        inp = str(input('Enter word, or "!!" to indicate that you are finished: '))
        # If the input is two exclamation points:
        if inp == '!!':
            # if user inputs '!!', reduce num of hands
            num_hands -= 1
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(inp, hand, word_list) == True:
                # Tell the user how many points the word earned,
                # and the updated total score
                round_score = get_word_score(inp, calculate_handlen(hand))
                total_score += round_score
                print('"' + inp + '"', 'earned', round_score, 'points. Total:', total_score, 'points')
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('That is not a valid word. Please choose another word.')
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, inp)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if inp == '!!':
        print('Total score:', total_score)
    elif calculate_handlen(hand) == 0:
        print('Ran out of letters. Total score:', total_score, 'points')
    # Return the total score as result of function
    return total_score



def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    # if letter is in hand, change
    if letter in hand:
        # choose a random replacement until the random selection
        # cannot be found in current hand
        replacement = random.choice(VOWELS+CONSONANTS)
        while replacement in hand:
            replacement = random.choice(VOWELS+CONSONANTS)
        # sets the value of letter-to-be-replaced in hand
        # to the new letter, which will serve as the new key with same value
        value = hand[letter]
        del(new_hand[letter])
        new_hand[replacement] = value
        # returns a copy of the hand with replaced letter
        return new_hand
    # if letter not in hand, return same hand
    else:
        return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # initializing fresh hand and total score
    hand = {}
    total_score = 0
    # score 1 for non-replay score
    score1 = 0
    # score 2 for replay score
    score2 = 0
    # ask the user for input
    num_hands = int(input('Enter total number of hands: '))
    # initializing counter for number of times a letter substitution
    # is called by player (max. = 1 time)
    sub_count = 0
    # initializing counter for replays (max. = 1)
    replay_count = 0

    # while there are still hands to be played, run game loop
    while num_hands > 0:
        hand = deal_hand(HAND_SIZE)
        print()
        print('Current Hand: ')
        display_hand(hand)

        # run if no subs and hand replays were used up
        if sub_count == 0 and replay_count < 1:
            sub = str(input('Would you like to substitute a letter? '))
            sub = sub.lower()
            if sub == 'yes':
                replacement = str(input('Which letter would you like to replace: '))
                hand = substitute_hand(hand, replacement)
                # add 1 to sub_count so it never runs if-loop again
                sub_count = 1
            else:
                print()
        
        # runs hand set to score1 (non-replay score)
        score1 = play_hand(hand, word_list, num_hands)
        print()
        print('Total score for this hand: ' + str(score1))
        print('----------')
    
        # ask if user wants to replay the hand (no subs allowed)
        if replay_count == 0:
            replay = str(input('Would you like to replay the hand? '))
            replay = replay.lower()
            # if user wants to replay the hand, play another hand to set to second score
            if replay == 'yes':
                score2 = score1
                # set replay count to 1 to prevent the if-loop from running again
                replay_count = 1
            # if user does not want to replay, deduct one hand and add original score to total
            else:
                num_hands -= 1
                total_score += score1
        
        # if user decided to replay hand, check which score is higher
        # and set that as the final score for the hand
        if replay_count == 1:
            if score2 > score1:
                total_score += score2
            else:
                total_score += score1
            # add 1 to replay_count to prevent the loop comparing the scores again after adding
            replay_count += 1


    # print the final message after while loop is done
    print('Total score over all hands is:', str(total_score))


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
