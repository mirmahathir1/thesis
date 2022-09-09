# A recursive program to print all possible
# partitions of a given string into dictionary
# words

# A utility function to check whether a word
# is present in dictionary or not.  An array of
# strings is used for dictionary.  Using array
# of strings for dictionary is definitely not
# a good idea. We have used for simplicity of
# the program
def dictionaryContains(word):
    dictionary = {"mobile", "samsung", "sam", "sung", "man",
                  "mango", "icecream", "and", "go", "i", "love", "ice", "cream"}
    return word in dictionary


# Prints all possible word breaks of given string
def wordBreak(string):
    # Last argument is prefix
    wordBreakUtil(string, len(string), "")


# Result store the current prefix with spaces
# between words
def wordBreakUtil(string, n, result):
    # Process all prefixes one by one
    for i in range(1, n + 1):

        # Extract substring from 0 to i in prefix
        prefix = string[:i]

        # If dictionary contains this prefix, then
        # we check for remaining string. Otherwise
        # we ignore this prefix (there is no else for
        # this if) and try next
        if dictionaryContains(prefix):

            # If no more elements are there, print it
            if i == n:
                # Add this element to previous prefix
                result += prefix
                print(result)
                return
            wordBreakUtil(string[i:], n - i, result + prefix + " ")


# Driver Code
if __name__ == "__main__":
    print("First Test:")
    wordBreak("iloveicecreamandmango")

    print("\nSecond Test:")
    wordBreak("ilovesamsungmobile")