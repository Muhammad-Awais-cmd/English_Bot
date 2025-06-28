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
