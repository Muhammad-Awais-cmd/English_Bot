import httpx
from nltk.corpus import wordnet

async def define_word(word: str) -> str:
    """Enhanced word definition with professional formatting"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                word_data = data[0]
                word_title = word_data.get("word", word).capitalize()

                phonetic = ""
                if "phonetics" in word_data and word_data["phonetics"]:
                    for p in word_data["phonetics"]:
                        if "text" in p and p["text"]:
                            phonetic = f" /{p['text']}/"
                            break

                meaning_block = word_data["meanings"][0]
                part_of_speech = meaning_block["partOfSpeech"]
                definition = meaning_block["definitions"][0]["definition"]
                example = meaning_block["definitions"][0].get("example", "")

                response = f"\U0001F4D6 **Definition of '{word_title}'**{phonetic}\n\n"
                response += f"**Part of Speech:** {part_of_speech.capitalize()}\n\n"
                response += f"**Meaning:** {definition}\n\n"
                if example:
                    response += f"**Example:** \"{example}\"\n\n"
                else:
                    response += f"**Example:** \"The word '{word_title.lower()}' is commonly used in English.\"\n\n"
                if len(meaning_block["definitions"]) > 1:
                    response += f"**Additional Context:** {meaning_block['definitions'][1]['definition']}"
                return response
    except Exception:
        pass

    try:
        synsets = wordnet.synsets(word.lower())
        if synsets:
            synset = synsets[0]
            meaning = synset.definition()
            examples = synset.examples()
            pos = synset.pos()
            pos_full = {'n': 'noun', 'v': 'verb', 'a': 'adjective', 's': 'adjective', 'r': 'adverb'}.get(pos, 'word')
            response = f"\U0001F4D6 **Definition of '{word.capitalize()}'**\n\n"
            response += f"**Part of Speech:** {pos_full.capitalize()}\n\n"
            response += f"**Meaning:** {meaning.capitalize()}\n\n"
            if examples:
                response += f"**Example:** \"{examples[0]}\""
            else:
                response += f"**Example:** \"The word '{word.lower()}' is used in English literature.\""
            return response
    except Exception:
        pass

    return f"❌ Sorry, I couldn't find the definition for '{word}'. Please check the spelling and try again."

async def get_datamuse_synonyms(word: str) -> list[str]:
    """Fetch synonyms using Datamuse API"""
    try:
        url = f"https://api.datamuse.com/words?rel_syn={word.lower()}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return [entry["word"] for entry in data if "word" in entry]
    except Exception:
        pass
    return []

async def get_synonyms(word: str) -> str:
    """Return clean and professional synonyms for a word from multiple sources"""
    word_lower = word.lower()
    word_cap = word.capitalize()

    # 1. Try dictionaryapi.dev
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_lower}"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                meanings = data[0].get("meanings", [])
                all_synonyms = []
                for meaning in meanings:
                    for definition in meaning.get("definitions", []):
                        all_synonyms.extend(definition.get("synonyms", []))
                unique_synonyms = sorted(set(s for s in all_synonyms if s.lower() != word_lower))
                if unique_synonyms:
                    selected = unique_synonyms[:4]
                    response_text = f"\U0001F501 **Synonyms of '{word_cap}'**\n\n"
                    for i, syn in enumerate(selected, 1):
                        response_text += f"{i}. **{syn.capitalize()}**\n"
                    return response_text
    except Exception:
        pass

    # 2. Try Datamuse API
    datamuse_synonyms = await get_datamuse_synonyms(word_lower)
    if datamuse_synonyms:
        selected = datamuse_synonyms[:4]
        response_text = f"\U0001F501 **Synonyms of '{word_cap}'** (via Datamuse)\n\n"
        for i, syn in enumerate(selected, 1):
            response_text += f"{i}. **{syn.capitalize()}**\n"
        return response_text

    # 3. Final fallback: WordNet
    try:
        synsets = wordnet.synsets(word_lower)
        if synsets:
            lemmas = [lemma.name().replace('_', ' ') for syn in synsets for lemma in syn.lemmas()]
            synonyms = sorted(set(l for l in lemmas if l.lower() != word_lower))
            if synonyms:
                selected = synonyms[:4]
                response_text = f"\U0001F501 **Synonyms of '{word_cap}'** (via WordNet)\n\n"
                for i, syn in enumerate(selected, 1):
                    response_text += f"{i}. **{syn.capitalize()}**\n"
                return response_text
    except Exception:
        pass

    # If all sources fail
    return f"❌ Sorry, I couldn't find synonyms for '{word}'. Please check the spelling and try again."
