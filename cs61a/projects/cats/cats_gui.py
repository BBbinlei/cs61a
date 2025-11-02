

@route
def autocorrect(word=""):
    """Call autocorrect using the best score function available."""
    raw_word = word
    word = cats.lower(cats.remove_punctuation(raw_word))
    if word in WORDS_SET or word == "":
        return raw_word

    # Heuristically choose candidate words to score.
    letters = set(word)
    candidates = [w for w, s in LETTER_SETS if similar(s, letters, SIMILARITY_LIMIT)]

    # Try various diff functions until one doesn't raise an exception.
    for fn in [cats.final_diff, cats.minimum_mewtations, cats.furry_fixes]:
        try:
            guess = cats.autocorrect(word, candidates, fn, SIMILARITY_LIMIT)
            return reformat(guess, raw_word)
        except BaseException:
            pass

    return raw_word


def reformat(word, raw_word):
    """Reformat WORD to match the capitalization and punctuation of RAW_WORD."""
    # handle capitalization
    if raw_word != "" and raw_word[0].isupper():
        word = word.capitalize()

    # find the boundaries of the raw word
    first = 0
    while first < len(raw_word) and raw_word[first] in string.punctuation:
        first += 1
    last = len(raw_word) - 1
    while last > first and raw_word[last] in string.punctuation:
        last -= 1

    # add wrapping punctuation to the word
    if raw_word != word:
        word = raw_word[:first] + word
        word = word + raw_word[last + 1 :]

    return word


###############
# Multiplayer #
###############


@route
def request_id():
    if not cats.enable_multiplayer:
        return
    return Server.provide_id()


@route
def report_progress(id, typed, prompt):
    """Report progress to the multiplayer server and also return it."""
    typed = typed.split()  # A list of word strings
    prompt = prompt.split()  # A list of word strings

    return cats.report_progress(typed, prompt, id, sendto(Server.set_progress))


@route
def fastest_words(prompt, targets):
    """Return a list of word_speed values describing the match."""
    words = prompt.split()
    progress = Server.request_all_progress(targets=targets)
    start_times = [p[0][1] for p in progress]
    times_per_player = [[p[1] - s for p in ps] for s, ps in zip(start_times, progress)]
    match = cats.time_per_word(words, times_per_player)
    return cats.fastest_words(match)


multiplayer.create_multiplayer_server()

###############
# Favicons #
###############


@route
@route("favicon.ico")
def favicon():
    favicon_folder = "favicons"
    favicons = os.listdir(favicon_folder)
    path = os.path.join(favicon_folder, random.choice(favicons))
    with open(path, "rb") as f:
        data = f.read()
    image_b64 = base64.b64encode(data).decode("utf-8")
    return "data:image/png;base64," + image_b64


if __name__ == "__main__" or os.environ.get("ENV") == "prod":
    app = start(PORT, DEFAULT_SERVER, GUI_FOLDER, multiplayer.db_init)