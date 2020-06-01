from itertools import groupby

def parsePHPVersions(links):
    names = [link.get('href').split('/')[-1] for link in links]

    names = [n for n in names if n.startswith('php-7') and n.endswith('.zip') and "nts" in n]
    names.sort()

    def keyf(text):
        minorVersion = text.split("-")[1].split('.')[0:2]
        return '.'.join(minorVersion)

    res = [list(items) for gr, items in groupby(names, key=keyf)]

    phpVersions = list()

    for item in res:
        phpVersions.append(item[-2:])

    return phpVersions
