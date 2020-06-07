import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from packaging.version import Version, parse
import os, os.path
import zipfile
from shutil import copyfile

if not os.path.exists("PHP/"):
    os.makedirs("PHP/")

installDir = "PHP"
installedPHP = list(filter(lambda x: os.path.isdir(os.path.join(installDir, x)), os.listdir(installDir)))

def extractLinks(URL):
    # extract links web scraping
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.find_all('a')
    links = [link.get('href').split('/')[-1] for link in links]
    return links

def clearData(data, latestPath = True):
    data = {
        "path": data
    }

    df = DataFrame(data)

    # Select windows related datas
    df = df[df["path"].str.contains("Win")]
    df = df[df["path"].str.endswith('.zip')]

    # Remove all .zip in the end of string
    paths = Series(df["path"]).apply(str)
    paths = paths.apply(lambda x: x[:-4])
    df["path"] = paths

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

    if latestPath:
        # Groupe by minor releases
        idx = df2.groupby(['minor'])['version'].transform(max) == df['version']
        phpReleases = DataFrame(df2[idx])
        return phpReleases.groupby('minor')

    return df2.groupby('minor')

def download(url, name):
    path = 'PHP/' + name
    r = requests.get(url, allow_redirects=True, stream=True)

    if r.status_code == 200:
        with open(path + '.zip', 'wb') as f:
            for chunk in r:
                # print('Writing chunk') # Uncomment this to show that the file is being written chunk-by-chunk when parts of the data is received
                f.write(chunk) # Write each chunk received to a file
            # f.write(r.content)
        with zipfile.ZipFile(path + '.zip', 'r') as zip_ref:
            zip_ref.extractall(path)

        os.remove(path + '.zip')
        copyfile(path + '/php.ini-development', path + '/php.ini')