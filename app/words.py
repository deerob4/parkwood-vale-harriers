with open('sowpods.txt', 'r') as f:
    word_list = [line.lower().replace('\n', '') for line in f]


def generate_words(letters):
    found_words = []
    for word in word_list:
        word_as_list = list(word)
        for letter in letters:
            if letter in word_as_list:
                word_as_list.remove(letter)
        if len(word_as_list) == 0:
            found_words.append(word)
    for i, word in enumerate(sorted(found_words, key=len)):
        print('%s. %s' % (i, word))
    
    
generate_words(input('Letters: '))