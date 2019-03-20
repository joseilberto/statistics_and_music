import re
import unidecode


def remove_punctuation(string, removals, strip_it, separator):
    string = string.rstrip(strip_it)
    for removal in removals:
        string = string.replace(removal, "")
    year = re.search(r"\((\d+)\)", string)
    if year:
        year = year.group(1)
        string = string.replace("({})".format(year), "")
    string = string.replace(separator, "_")
    return unidecode.unidecode(string).lower()
