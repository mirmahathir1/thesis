import os
from nltk.corpus import words
import re
from os.path import exists
from textblob import Word
import requests
from .secret.apikey import api_key


def api_call(word):
    print(f"calling API for word: {word}...")
    # response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=da023940-e5a4-410c-a5dd-d26c9628b941")
    # print(f"content length: {len(response.content)}")
    # return response.status_code == 200 and len(response.content) > 2
    response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
    return response.status_code == 200

def suggest_word(word):
    response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}")
    if len(response.json()) == 0:
        return 'unknown'
    if type(response.json()[0]) == dict:
        return response.json()[0]['meta']['stems'][0].lower()
    return response.json()[0].lower()


def remove_punctuation(sentence):
    sentence = sentence.replace('\'', "")
    return re.sub(r'[^\w\s]', ' ', sentence)


def remove_multiple_whitespaces(sentence):
    return re.sub(' +', ' ', sentence)


def convert_to_small_letter(sentence):
    return sentence.lower()


class CustomDictionary:
    def __init__(self):
        self.nltk_words = set(words.words())
        dictionary_file = open('./dictionary_data/dictionary_data.txt', 'r', encoding='utf-8')
        self.all_words = [word.strip() for word in dictionary_file.readlines()]
        not_found_dictionaryapi_file = open('./dictionary_data/dictionaryapi_not_found.txt', 'r', encoding='utf-8')
        self.not_found_in_dictionary_api = [word.strip() for word in not_found_dictionaryapi_file.readlines()]
        print("all words: ", " ".join(self.all_words))
        dictionary_file.close()

        self.replacement_words = dict()

        if not exists('./dictionary_data/dictionary_discarded.txt'):
            replacement_words_file = open('./dictionary_data/dictionary_discarded.txt', 'a', encoding='utf-8')
            replacement_words_file.close()
            return

        replacement_words_file = open('./dictionary_data/dictionary_discarded.txt', 'r', encoding='utf-8')
        replacement_word_lines = [line.strip() for line in replacement_words_file.readlines()]

        for replacement_word_line in replacement_word_lines:
            word_infos = replacement_word_line.split(' ')
            # first word is the word having errors, the remaining words are replacements
            self.replacement_words[word_infos[0]] = word_infos[1:]

        replacement_words_file.close()

    def save_word(self, new_word):
        if self.has_in_local_memory(new_word):
            print("word already exists in dictionary")
            return
        self.all_words.append(new_word)
        dictionary_file = open('./dictionary_data/dictionary_data.txt', 'a', encoding='utf-8')
        dictionary_file.write(new_word + "\n")
        dictionary_file.close()
    
    def has_in_local_memory(self, new_word):
        return new_word in self.all_words or new_word in self.nltk_words
    
    def save_not_found_word_of_dictionary_api(self, new_word):
        if new_word in self.not_found_in_dictionary_api:
            return
        self.not_found_in_dictionary_api.append(new_word)
        dictionary_not_found_file = open('./dictionary_data/dictionaryapi_not_found.txt', 'a', encoding='utf-8')
        dictionary_not_found_file.write(new_word + "\n")
        dictionary_not_found_file.close()

    def has(self, query_word):
        has_in_memory = query_word in self.all_words or query_word in self.nltk_words
        if has_in_memory:
            return True
        if query_word in self.not_found_in_dictionary_api:
            return False
        if not api_call(query_word):
            self.save_not_found_word_of_dictionary_api(query_word)
            return False
        self.save_word(query_word)
        return True

    def save_replacement_word(self, error_word, list_of_words):
        if error_word in self.replacement_words:
            print("replacement word already exists in database. skipping...")
            return
        if not type(list_of_words) == list:
            print("second argument of save_replacement_word is not a list. Exiting")
            exit(0)
        replacement_words_file = open('./dictionary_data/dictionary_discarded.txt', 'a', encoding='utf-8')
        replacement_words_file.write(f"{error_word} {' '.join(list_of_words)}\n")
        replacement_words_file.close()
        self.replacement_words[error_word] = list_of_words

    def has_replacable_words(self, query_error_word):
        return query_error_word in self.replacement_words

    def get_replacable_words(self, query_error_word):
        return self.replacement_words[query_error_word]


myDictionary = CustomDictionary()

# Prints all possible word breaks of given string

class WordSplit:
    def __init__(self):
        self.min_word_count = 9999
        self.accepted_split = []

    def wordBreak(self, string):
        self.min_word_count = 9999
        self.accepted_split = []
        # Last argument is prefix
        return self.wordBreakUtil(string, len(string), "")

    # Result store the current prefix with spaces
    # between words
    def wordBreakUtil(self, string, n, result):
        # Process all prefixes one by one
        for i in range(1, n + 1):

            # Extract substring from 0 to i in prefix
            prefix = string[:i]

            # If dictionary contains this prefix, then
            # we check for remaining string. Otherwise
            # we ignore this prefix (there is no else for
            # this if) and try next
            if myDictionary.has(prefix):

                # If no more elements are there, print it
                if i == n:
                    # Add this element to previous prefix
                    result += prefix
                    if len(result.split(" ")) < self.min_word_count:
                        self.min_word_count = len(result.split(" "))
                        self.accepted_split = result.split(" ")
                    return

                self.wordBreakUtil(string[i:], n - i, result + prefix + " ")


word_split = WordSplit()

text_file_paths = []
for path, subdirs, files in os.walk('../extractedbdhandspeakskeletons/texts'):
    for name in files:
        file_path = os.path.join(path, name)  # change to your own video path
        if '.txt' in file_path:
            text_file_paths.append(file_path)

def read_clean(single_text_file_path):
    text_file = open(single_text_file_path, encoding='utf-8')
    lines = text_file.readlines()
    text_file.close()
    cleaned_lines = []
    line_times = []
    for line in lines:
        raw_line_data = line.strip().split('||')
        if len(raw_line_data) == 1:
            continue
        cleaned_line = convert_to_small_letter(
            remove_multiple_whitespaces(remove_punctuation(raw_line_data[0])))
        line_time = raw_line_data[1]
        if len(cleaned_line) == 0:
            continue
        cleaned_lines.append(cleaned_line)
        line_times.append(line_time)
    return cleaned_lines, line_times


def check_one_file(single_text_file_path):
    print(single_text_file_path)
    text_file = open(single_text_file_path, encoding='utf-8')
    lines = text_file.readlines()
    for line in lines:
        cleaned_line = convert_to_small_letter(
            remove_multiple_whitespaces(remove_punctuation(line.strip().split('||')[0])))
        if len(cleaned_line) == 0:
            continue

        print("-----------main line: ", cleaned_line)
        words_in_line = cleaned_line.split(' ')
        for single_word in words_in_line:
            cleaned_word = single_word.strip()
            if len(cleaned_word) == 0 or cleaned_word.isnumeric() or myDictionary.has_replacable_words(cleaned_word) or myDictionary.has(cleaned_word):
                continue

            print(f"word: {cleaned_word} not found in dictionary. ")
            # print(f"suggestion: {Word(cleaned_word).spellcheck()}. ")
            # word_split.wordBreak(cleaned_word)
            # print(f"possible word split: {word_split.accepted_split}")
            suggestion = suggest_word(cleaned_word)
            print(f"suggestion: {suggestion}")

            if suggestion == cleaned_word:
                command = 's'
            else:
                command = input('enter command. type \'s\' to accept the suggestion, type \'d\' to delete word, or type replacement: ')

            if command == 's':
                print(f"saving error word: {cleaned_word} and replacement: {suggestion.split(' ')} to file")
                myDictionary.save_replacement_word(cleaned_word, suggestion.split(' '))
                continue

            if command == '':
                print(f"saving only to dictionary: {cleaned_word}")
                myDictionary.save_word(cleaned_word)
                continue

            if command == 'd':
                print(f"saving error word: {cleaned_word}  to replacement file")
                myDictionary.save_replacement_word(cleaned_word, [])
            else:
                replacement_words = command.split(' ')
                print("saving replacements")
                for replacement_word in replacement_words:
                    print(f"saving replacement word to dictionary: {replacement_word}")
                    myDictionary.save_word(replacement_word)
                print(f"saving error word: {cleaned_word} and replacement: {replacement_words} to file")
                myDictionary.save_replacement_word(cleaned_word, replacement_words)

    text_file.close()


def refine_all_texts_using_dictionary(text_file_path):
    [directory, file_name] = text_file_path.split('\\')
    all_lines, line_times = read_clean(text_file_path)
    refined_text_file = open('cleaned_texts/'+file_name,'w',encoding='utf-8')
    for i in range(len(all_lines)):
        word_list = all_lines[i].split(" ")
        for key in myDictionary.replacement_words.keys():
            if key in word_list:
                word_list = list(
                    map(lambda x: x.replace(key, " ".join(myDictionary.get_replacable_words(key))), word_list))
        print(" ".join(word_list).strip() + " || time: " + line_times[i], file=refined_text_file)
    
    refined_text_file.close()


for text_file_path in text_file_paths:
    print(f"text file: {text_file_path}")
    check_one_file(text_file_path)
    refine_all_texts_using_dictionary(text_file_path)
