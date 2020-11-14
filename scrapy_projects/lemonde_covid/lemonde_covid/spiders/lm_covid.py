import scrapy
from scrapy import FormRequest
import re

class LmLoginSpider(scrapy.Spider):
    date_start = '01/01/2020'
    date_end = '01/04/2020'
    page_number = 1
    url_list = f"https://www.lemonde.fr/recherche/?search_keywords=covid&start_at={date_start}&end_at={date_end}&search_sort=date_asc&page="
    name = 'lm_covid'
    allowed_domains = ['lemonde.fr']
    start_urls = ['https://secure.lemonde.fr/sfuser/connexion']

    def parse(self, response):
        print('\n')
        csrf_token = response.xpath("//input[@id='connection__token']/@value").get()
        yield FormRequest.from_response(response,
          formxpath="//form[@name='connection']",
          formdata={'connection[_token]':csrf_token, 
         'connection[mail]':'flabastie@hotmail.com', 
         'connection[password]':'93WestburyRoad', 
         'connection[stay_connected]':'1'},
          callback=(self.after_login))

    def after_login(self, response):
        if response.xpath("//span[@class='login-info']/text()").get():
            print('\n---------------')
            print('  logged in')
            print(f"  User-Agent : {response.request.headers['User-Agent']}")
            print('---------------\n')
        else:
            print('\n---------------')
            print('  ERROR')
            print('---------------\n')
        print('URL: ' + response.request.url)
        url = self.url_list + str(self.page_number)
        return response.follow(url, self.parse_links_list)

    def parse_links_list(self, response):
        last_page = response.xpath("(//a[@class='river__pagination river__pagination--page-search ' ])[last()]/text()").get()
        rows = response.xpath("//section[@class='teaser teaser--inline-picture ']")
        for item in rows:
            document_title = item.xpath(".//h3[@class='teaser__title']/text()").get()
            document_link = item.xpath(".//a[@class='teaser__link teaser__link--kicker']/@href").get()
            document_teaser = item.xpath(".//p[@class='teaser__desc']/text()").get()
            splitted_link = re.split('/', document_link)
            document_date = splitted_link[5] + '-' + splitted_link[6] + '-' + splitted_link[7]
            document_section = splitted_link[3]
            document_type = splitted_link[4]
            document_author = item.xpath(".//span[@class='meta__author meta__author--page']/text()").get()
            yield response.follow(url=document_link, callback=(self.parse_document),
              meta={'document_link':document_link, 
             'document_date':document_date, 
             'document_section':document_section, 
             'document_type':document_type, 
             'document_title':document_title, 
             'document_teaser':document_teaser, 
             'document_author':document_author})

        if self.page_number < int(last_page):
            print('\n--------------------')
            print(f"    Page {self.page_number}")
            print('--------------------\n')
            self.page_number += 1
            new_url = self.url_list + str(self.page_number)
            yield scrapy.Request(url=new_url, callback=(self.parse_links_list))
        else:
            print('\n--------------------')
            print(f" {self.page_number} pages scrapped")
            print('--------------------\n')

    def parse_document(self, response):
        document_link = response.request.meta['document_link']
        document_date = response.request.meta['document_date']
        document_section = response.request.meta['document_section']
        document_type = response.request.meta['document_type']
        document_title = response.request.meta['document_title']
        document_teaser = response.request.meta['document_teaser']
        document_author = response.request.meta['document_author']
        document_html = response.xpath('//article/p | //article/h2').getall()
        if len(document_html) == 0:
            document_html = response.xpath("//article[@class='article article--longform  article--content']\n                                                    /section[@class='article__content']/p |\n                                                //article[@class='article article--longform  article--content']\n                                                    /section[@class='article__content']/h2 |\n                                                //article[@class='article article--longform  article--content']\n                                                    /section[@class='article__content']/blockquote").getall()
        if len(document_html) == 0:
            document_html = response.xpath("//article[@class='article article--longform article--longform-nocover  article--content']\n                                                    /section[@class='article__content']/p |\n                                                //article[@class='article article--longform article--longform-nocover  article--content']\n                                                    /section[@class='article__content']/h2 |\n                                                //article[@class='article article--longform article--longform-nocover  article--content']\n                                                    /section[@class='article__content']/blockquote").getall()
        yield {'document_link':document_link, 
         'document_date':document_date, 
         'document_section':document_section, 
         'document_type':document_type, 
         'document_title':document_title, 
         'document_teaser':document_teaser, 
         'document_author':document_author, 
         'document_html':document_html, 
         'document_text':'', 
         'document_all':''}