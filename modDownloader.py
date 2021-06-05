import wget
import csv
import os
import requests
import time

def downloadFile(url):
    r = requests.get(url)
    r.raise_for_status()
    print(r.status_code, wget.filename_from_url(url))
    with open("./files/" + wget.filename_from_url(url), "wb") as file:
        file.write(r.content)


print(f"started at {time.strftime('%X')}")

try:
    os.mkdir("./files")
except FileExistsError:
    pass

with open("links.csv") as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for line in reader:
        print(i, end=' ')
        downloadFile(line[0])
        i = i + 1

print(f"finished at {time.strftime('%X')}")