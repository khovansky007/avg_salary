from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as bs



class hh_analyst:
    

    def __init__(self, url = input()):
        self.url = url
        self.all_prices = []
    

    def __get_count_pages(self):
        responce = requests.get(self.url, headers = {'User-Agent': UserAgent().random})
        soup = bs(responce.text, 'lxml')
        nums_pages = []
        for i in soup.find_all('a', {'data-qa': 'pager-page'}):
            nums_pages.append(i.find('span').text)
        count_pages = int(nums_pages[-1])
        self.count_pages = count_pages

    
    def __get_prices(self, url):
        ua = UserAgent().random
        responce = requests.get(url, headers = {'User-Agent': ua})
        soup = bs(responce.text, 'lxml')
        prices = soup.find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        for item in prices:
            price = item.text
            price_encode = price.encode("ascii", "ignore")
            price = price_encode.decode()
            if '  ' in price:
                price = price.split('  ')
                price_var = []
                for i in price:
                    for symbol in i:
                        if symbol in '0123456789':
                            price_var.append(symbol)
                    price_var.append(' ')
                price_var = ''.join(price_var[:-1]).split()
                price = (int(price_var[0]) + int(price_var[1]))/2
            else:
                price = [symbol for symbol in price if symbol in '0123456789']
                price = ''.join(price)
                price = int(price)

            self.all_prices.append(price)


    def main(self):
        self.__get_count_pages()
        if '?' in self.url: char = '&'
        else: char = '?'
        for num_page in range(self.count_pages):
            url = f"{self.url}{char}page={num_page}"
            self.__get_prices(url)
            print(f"{num_page+1} page scanned")

        avg_price = sum(self.all_prices)/len(self.all_prices)
        return f"{int(avg_price)} ₽"



while True:
    url = input("Link: ")
    x = hh_analyst(url)
    print(x.main())
    input('End. Press any key to continue.')
