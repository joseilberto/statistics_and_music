ordinary_table = "//table[@class='midi']"
XPATHS = {
    "table": ordinary_table,
    "lines_table": "{}/tr".format(ordinary_table),
    "links_table": "{}//a/@href".format(ordinary_table),
    "artist": "//h1[contains(@class, 'head')]/text()",
    "songs": "{}/preceding::h2[1]/text()".format(ordinary_table),
}
