import re
from banglanum2words import num_convert
# https://github.com/dv66/bangla-number-in-words
class BanglaDigit:
    bangla_digits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
    bangla_digit_words = ['শূন্য', 'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়', 'সাত', 'আট', 'নয়']

    @staticmethod
    def get_english_digit(bangla_digit):
        if not bangla_digit in BanglaDigit.bangla_digits:
            print(f"{bangla_digit} is not a bangla digit. code will exit.")
            exit(0)
        return BanglaDigit.bangla_digits.index(bangla_digit)

    bangla_place_value_system = ['', 'দশক', 'শতক', 'হাজার', 'অযুত', 'লক্ষ', 'নিযুত', 'কোটি']

    @staticmethod
    def bangla_number_spell_string(bangla_number_string):
        if len(bangla_number_string) > 9:
            print(f"{bangla_number_string} is of length greater than 9. code will exit.")
            exit(0)
        number_string = ""
        length_of_digits = len(bangla_number_string)
        for i in range(length_of_digits):
            english_digit = BanglaDigit.get_english_digit(bangla_number_string[length_of_digits-i-1])
            if english_digit == 0:
                continue
            bangla_digit_word = BanglaDigit.bangla_digit_words[english_digit]
            bangla_place_value_word = BanglaDigit.bangla_place_value_system[i]
            number_string = bangla_digit_word + ' ' + bangla_place_value_word + ' ' + number_string
        
        return number_string
    @staticmethod
    def replace_bangla_number_in_sentence(sentence):
        found_numeric_bangla_numbers = re.findall(f'[{"".join(BanglaDigit.bangla_digits)}]+', sentence)
        for found_numeric_bangla_number in found_numeric_bangla_numbers:
            spelled_number = num_convert.number_to_bangla_words(found_numeric_bangla_number)
            # spelled_number = BanglaDigit.bangla_number_spell_string(found_numeric_bangla_number)
            sentence = sentence.replace(found_numeric_bangla_number, spelled_number, 1)

        sentence = " " + " ".join(sentence.split()) + " "
        return sentence
    @staticmethod
    def has_number_more_than_nine_digits(sentence):
        found_numeric_bangla_numbers = re.findall(f'[{"".join(BanglaDigit.bangla_digits)}]+', sentence)
        for found_numeric_bangla_number in found_numeric_bangla_numbers:
            if len(found_numeric_bangla_number) > 9:
                return True
        return False


# print(num_convert.number_to_bangla_words("১২৩৪"))
# print(num_convert.number_to_bangla_words("৩৪১২৩৪"))
