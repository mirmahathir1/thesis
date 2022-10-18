import requests
word = 'alumni'
x = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
print(x.status_code)