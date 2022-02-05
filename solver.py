import random, re, requests

response = requests.get('https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt')
ru_text = list(filter(lambda word: len(word) == 5, response.text.split()))

response = requests.get('https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/5d752e5f0702da315298a6bb5a771586d6ff445c/wordle-answers-alphabetical.txt')
en_text = response.text.split()

lang = input("Choose your language (en, ru):\n")
if lang == 'en':
    words = en_text
elif lang == 'ru':
    words = ru_text
else:
    raise ValueError("Incorrect language")

bad = set()
good = [None, None, None, None, None]
miss = set()
exist = set()
guesses = 0

while True:
    guess_type = input("Choose your next guess type (c for custom, r for random):\n")
    if guess_type == 'r':
        word = random.choice(words)
        print(word)
    elif guess_type == 'c':
        word = input("Your guess: ")
        if word not in words:
            print("Incorrect guess, try again")
            continue
    else:
        print("Incorrect type, try again")
        continue

    guesses += 1

    ans = input("Your result: ")
    if ans == 'bad':
        words.remove(word)
        continue
    if not re.fullmatch('[gwy]{5}', ans):
        print("Incorrect result")
        continue
    if ans == 'ggggg':
        print(f"We made it in {guesses} guesses")
        break

    for i in range(5):
        if ans[i] == 'w':
            bad.add(word[i])
        if ans[i] == 'g':
            good[i] = word[i]
        if ans[i] == 'y':
            miss.add((i, word[i]))
            exist.add(word[i])

    words = filter(lambda word: all([word[i] not in bad if good[i] is None else word[i] == good[i] for i in range(5)]), words)
    words = filter(lambda word: len(set(word).intersection(exist)) == len(exist), words)
    words = filter(lambda word: all([word[t[0]] != t[1] for t in miss]), words)

    words = list(words)
