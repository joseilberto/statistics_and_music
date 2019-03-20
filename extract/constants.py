ordinary_table = "//table[@class='midi']"

RELEVANT_COLS = ["part", "duration", "date"]

XPATHS = {
    "table": ordinary_table,
    "lines_table": "{}/tr".format(ordinary_table),
    "cols_table": "//tr/t{}/text()".format,
    "link_midi": "//tr/td[1]/a/@href",
    "links_table": "{}//a/@href".format(ordinary_table),
    "artist": "//h1[contains(@class, 'head')]/text()",
    "songs": "{}/preceding::h2[1]/text()".format(ordinary_table),
}
