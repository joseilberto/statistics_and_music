import re
import sys
import unidecode


def join_to_path(base, *args, **kwargs):
    bar = '/' if 'win' not in sys.platform else '\\'
    string = base if base.endswith(bar) else base + bar
    for arg in args:
        string += arg.replace(bar, "") + bar
    return string


def remove_punctuation(string, removals, strip_it, separator):
    string = string.rstrip(strip_it)
    for removal in removals:
        string = string.replace(removal, "")
    year = re.search(r"\((\d+)\)", string)
    if year:
        year = year.group(1)
        string = string.replace("({})".format(year), "")
    opus = re.search(r"(\d+)/(\d+)", string)
    if opus:
        opus = opus.group(1)
        string = string.replace("/", "-")
    string = string.replace(separator, "_")
    return unidecode.unidecode(string).lower()
