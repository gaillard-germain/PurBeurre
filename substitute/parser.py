import unidecode
import re
from string import ascii_lowercase


class Parser:
    FORBID = ["un", "une", "au", "aux", "de", "des", "du", "le", "la", "les",
              "en", "mais", "ou", "et", "dont", "or", "ni", "car", "sans"]

    @classmethod
    def parse_entry(cls, entry):
        entry = unidecode.unidecode(entry)
        entry = re.split(r'\W+', entry.lower())
        result = []

        for word in entry:
            if word not in cls.FORBID and word not in ascii_lowercase:
                result.append(word)
        result = "+".join(filter(None, result))

        return result
