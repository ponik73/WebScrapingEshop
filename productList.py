import requests
from bs4 import BeautifulSoup, element
from urllib import parse

PAGE = "https://www.otto.de"
URI_SMARTPHONES = "technik/smartphone"

def extractAnchorFromElement(element):
    try:
        return element.find("a")
    except Exception:
        return None

def extractAnchors(rs: element.ResultSet):
    anchors = []
    for item in rs:
        anchor = extractAnchorFromElement(item)
        if anchor is None:
            continue
        anchors.append(anchor)
    return anchors

def extractLinkFromAnchor(anchor):
    try:
        return anchor.get('href')
    except Exception:
        return ""

def extractLinks(rs: element.ResultSet, dist: list):
    for item in rs:
        link = extractLinkFromAnchor(item)
        if not link or link.isspace():
            continue
        dist.append(link)

def getProductLinks(soup: BeautifulSoup):
    links = []

    while len(links) + 1 < 100:
        try:
            productTable = soup.find(id="reptile-search-result")
            products = productTable.find_all("article", class_="product")
            anchors = extractAnchors(products)
            extractLinks(anchors, links)

            nextPageBtn = soup.find(id="reptile-paging-bottom-next")
            nextPageBtn = nextPageBtn.find("button")
            nextPageQuery = eval(nextPageBtn.get("data-page"))
            nextPageQuery = {k: v for k, v in nextPageQuery.items() if k and v}
            page = requests.get(f'{PAGE}/{URI_SMARTPHONES}/?{parse.urlencode(nextPageQuery)}')
            soup = BeautifulSoup(page.content, "html.parser")
        except Exception as ex:
            return False, ex
        
    return True, links

def print_items_url_into_file(items):
    for url in items:
        print(f'{PAGE}{url}')

def main():
    page = requests.get(f'{PAGE}/{URI_SMARTPHONES}')

    soup = BeautifulSoup(page.content, "html.parser")

    valid, data = getProductLinks(soup)

    if not valid:
        print(data)
        exit(-1)

    print_items_url_into_file(data)

if __name__ == "__main__":
    main()
