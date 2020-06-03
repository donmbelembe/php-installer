import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from packaging.version import Version, parse

def extractLinks(URL):
    # extract links web scraping
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.find_all('a')
    links = [link.get('href').split('/')[-1] for link in links]
    return links

def clearData(data):
    data = {
        "path": data
    }

    df = DataFrame(data)

    # Select windows related datas
    df = df[df["path"].str.contains("Win")]
    df = df[df["path"].str.endswith('.zip')]

    # add version column
    df["version"] = df["path"].str.split("-").str[1]

    # Temporarly add a column that contains a bool if the version is a valid version
    for index, serie in df.iterrows():
        isVersion = isinstance(parse(serie["version"]), Version)
        df.at[index, "isValidVersion"] = isVersion

    # Select only the rows that contains a valid version and remove the isValidVersion column
    df = df[df["isValidVersion"]]
    del df["isValidVersion"]

    # make a clone of the dataframe
    df2 = DataFrame(df)
    # generate a series that contains only minor releases
    versions = Series(df["version"]).apply(str)
    minor = versions.apply(lambda x: "{}.{}".format(parse(x).major,parse(x).minor))
    df2["minor"] = minor

    # Groupe by minor releases
    idx = df2.groupby(['minor'])['version'].transform(max) == df['version']
    phpReleases = DataFrame(df2[idx])
    return phpReleases.groupby('minor')