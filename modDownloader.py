from html.parser import HTMLParser

linkList = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global linkList
        if tag == 'a':
            linkList += [x[1] for _, x in enumerate(attrs) if x[0] == 'href']

parser = MyHTMLParser()