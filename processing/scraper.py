import requests
from bs4 import BeautifulSoup
import re
import datetime
import time

lines = open("data/links.txt", "r").readlines()
with open("data/smiles.txt","r") as out:
    startIndex = len(out.readlines())
curIndex = startIndex
for url in lines[startIndex:]:
    start = time.time()
    try:
        response = requests.get(url.strip())
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        contents = soup.prettify()

        pattern = r"setClipboard\('([^']+)'\)"

        match = re.search(pattern, contents)

        if match:
            result = match.group(0)
            with open("data/smiles.txt", "a") as f:
                f.write(result[14:-2] + "\n")
            print(result[14:-2])
        else:
            with open("data/smiles.txt", "a") as f:
                f.write("\n")
            print("No match found")
    except:
        with open("data/smiles.txt", "a") as f:
            f.write("\n")
        print("404")
        pass
    
    end = time.time()
    curIndex += 1

    print(f"~{str(datetime.timedelta(seconds = (end - start)*(len(lines) - curIndex)))} left.")