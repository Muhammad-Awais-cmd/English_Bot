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

async def get_synonyms(word: str) -> str:
    """Enhanced synonyms with detailed explanations and examples"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                word_data = data[0]
                word_title = word_data.get("word", word).capitalize()
                all_synonyms = []
                part_of_speech = ""
                word_definition = ""
                for meaning in word_data["meanings"]:
                    if not part_of_speech:
                        part_of_speech = meaning["partOfSpeech"]
                        word_definition = meaning["definitions"][0]["definition"]
                    for definition in meaning["definitions"]:
                        if "synonyms" in definition and definition["synonyms"]:
                            all_synonyms.extend(definition["synonyms"])
                unique_synonyms = list(set(s.lower() for s in all_synonyms if s.lower() != word.lower()))
                if unique_synonyms:
                    selected_synonyms = unique_synonyms[:4]
                    response = f"\U0001F501 **Synonyms of '{word_title}'**\n\n"
                    response += f"**Original Word:** {word_title} ({part_of_speech}) - {word_definition}\n\n"
                    response += "**Similar Words:**\n"
                    for i, syn in enumerate(selected_synonyms, 1):
                        response += f"{i}. **{syn.capitalize()}** - Used similarly to '{word.lower()}'\n"
                        response += f"   *Example: \"You can use '{syn}' instead of '{word.lower()}' in most contexts.\"*\n\n"
                    response += f"\U0001F4A1 *Tip: Try /Define {selected_synonyms[0]} to learn more about these alternatives.*"
                    return response
    except Exception:
        pass

    try:
        synsets = wordnet.synsets(word.lower())
        if synsets:
            synset = synsets[0]
            lemmas = [lemma.name().replace('_', ' ') for lemma in synset.lemmas()]
            synonyms = [l for l in lemmas if l.lower() != word.lower()]
            if synonyms:
                selected_synonyms = synonyms[:4]
                pos = synset.pos()
                pos_full = {'n': 'noun', 'v': 'verb', 'a': 'adjective', 's': 'adjective', 'r': 'adverb'}.get(pos, 'word')
                response = f"\U0001F501 **Synonyms of '{word.capitalize()}'**\n\n"
                response += f"**Original Word:** {word.capitalize()} ({pos_full}) - {synset.definition()}\n\n"
                response += "**Similar Words:**\n"
                for i, syn in enumerate(selected_synonyms, 1):
                    response += f"{i}. **{syn.capitalize()}** - Alternative word for '{word.lower()}'\n"
                    response += f"   *Example: \"'{syn.capitalize()}' can replace '{word.lower()}' in sentences.\"*\n\n"
                return response
    except Exception:
        pass

    return f"❌ Sorry, I couldn't find synonyms for '{word}'. Please verify the spelling and try again."

