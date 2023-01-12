from bangla_stemmer.stemmer import stemmer
wordlist = ['কবিরগুলিকে', 'আমাকে', 'নামাবার']
stmr = stemmer.BanglaStemmer()

with open('tmp/txt.vocab', encoding='utf-8') as file:
    lines = [line.rstrip() for line in file]

stem_file = open('tmp/stem_words.txt','w', encoding='utf-8') 

for line in lines:
    print(stmr.stem(line), file=stem_file)

stem_file.close()
