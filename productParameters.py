import requests
import sys
from bs4 import BeautifulSoup

class Product:
    def __init__(self, url):
        self.url = url
        self.name = ''
        self.price = ''
        self.resolutionPx = ''
        self.screenDiagonalInch = ''
        self.memorySizeRam = ''
        self.processorManufacturer = ''
    def setName(self, name):
        self.name = str(name)
    def setPrice(self, amount):
        self.price = str(amount)
    def setResolution(self, resolution):
        self.resolutionPx = str(resolution)
    def setDiagonal(self, diagonal):
        self.screenDiagonalInch = str(diagonal)
    def setRam(self, ram):
        self.memorySizeRam = str(ram)
    def setProcessorManufacturer(self, manufacturer):
        self.processorManufacturer = str(manufacturer)
    def printTsv(self):
        print(f'{self.url}\t{self.name}\t{self.price}\t{self.resolutionPx}\t{self.screenDiagonalInch}\t{self.memorySizeRam}\t{self.processorManufacturer}')


def scrapeValue(table, attribute):
    rows = table.find_all('tr')
    for tr in rows:
        data = tr.find_all('td')
        for td in data:
            attr = td.find('span')
            if not attr or attr.get_text(strip=True) != attribute:
                continue
            value = td.nextSibling
            return value.get_text(strip=True)

def getParameters(urls: list):
    products = []

    try:
        for url in urls:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            product = Product(url)

            nameHeading = soup.find("h1", class_="pdp_variation-name")
            if nameHeading:
                product.setName(nameHeading.get_text(strip=True))
            else:
                print(url)

            priceSpan = soup.find('span', class_='js_pdp_price__retail-price__value pl_headline300')
            if priceSpan:
                product.setPrice(priceSpan.get_text(strip=True))
            else:
                print(url)

            details = soup.find("div", class_="pdp_details__characteristics-html")
            if details:
                tables = details.find_all('table', class_='dv_characteristicsTable')
                for table in tables:
                    tableCaption = table.find('caption').get_text(strip=True)
                    if tableCaption == "Bildschirm":
                        diagonal = scrapeValue(table, "Bildschirmdiagonale in Zoll")
                        product.setDiagonal(diagonal)
                        resolution = scrapeValue(table, "Bildschirmauflösung in Pixel")
                        product.setResolution(resolution)
                    elif tableCaption == "Speicher":
                        ram = scrapeValue(table, "Arbeitsspeicher (RAM)")
                        product.setRam(ram)
                    elif tableCaption == "Prozessor":
                        manufacturer = scrapeValue(table, "Prozessorhersteller")
                        product.setProcessorManufacturer(manufacturer)

            products.append(product)
        return True, products
    except Exception as ex:
        return False, ex

def printParameters(products):
    for product in products:
        product.printTsv()

def main():
    try:
        test = len(sys.argv) == 2 and sys.argv[1] == "--test"
        urls = []

        for line in sys.stdin:
            urls.append(line.strip())
            # Test run - only 10 urls:
            if test and len(urls) == 10:
                break
        
        valid, data = getParameters(urls)

        if not valid:
            print(data)
            exit(-1)

        printParameters(data)

    except KeyboardInterrupt:
        exit(-1)

if __name__ == "__main__":
    main()