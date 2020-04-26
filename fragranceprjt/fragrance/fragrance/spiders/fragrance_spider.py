from scrapy import Spider, Request
from fragrance.items import FragranceItem
import re

class FragranceSpider(Spider):
    name = 'fragrance_spider'
    allowed_domains = ['galerieslafayette.com']
    start_urls = ['https://www.galerieslafayette.com/c/beaute-parfum/tri/meilleures-ventes']
    #start_urls = ['https://www.galerieslafayette.com/c/beaute-parfum/ct/beaute-parfum-parfum+femme/tri/meilleures-ventes']''


    #start_urls = ['https://www.galerieslafayette.com/c/beaute-parfum-parfum+femme/ct/beaute-parfum-parfum+femme/f/parfum/tri/meilleures-ventes']

    def parse(self, response):
        





        number_pages = int(response.xpath('//*[@id="wrapper-Catalogue"]/section/div[4]/div[2]/div/ul/li[5]//text()').extract()[-2].strip())

        



        #number_pages = response.xpath('//*[@id="wrapper-Catalogue"]/section/div[4]/div[3]/div/ul/li[5]/a//text()').extract()  



       
        result_urls = ['https://www.galerieslafayette.com/c/beaute-parfum/tri/meilleures-ventes/p:{}'.format(x) for x in range(1,number_pages+1)]


        #result_urls = ['https://www.galerieslafayette.com/c/beaute-parfum-parfum+femme/ct/beaute-parfum-parfum+femme/f/parfum/tri/meilleures-ventes/p:{}'.format(x) for x in range(1,number_pages+1)]

      
        for url in result_urls:

            
            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):
        


   



        product_urls = response.xpath('//div[@class="pdt-details"]/a/@href').extract()
        product_urls = [f'https://www.galerieslafayette.com{url}' for url in product_urls]

        for url in product_urls:
            yield Request(url=url, callback=self.parse_product_page)

        




    def parse_product_page(self, response):

        

    

#brand name
            try:

                brand = response.xpath('//div[@class="product-page__content__information--title"]//text()')[3].extract()
            except IndexError:
                brand = response.xpath('//*[@id="brand-title"]//text()').extract_first()

#product name
            try:
                title = response.xpath('//div[@class="product-page__content__information--title"]//text()')[8].extract()
            except IndexError:
                title = response.xpath('//div[@class="h-product-title"]//text()').extract()[3]



#price 

        #result_price = response.xpath('//*[@id="current-price"]//text()').extract_first()
            try:

                result_price = response.xpath('//*[@id="current-price"]//text()').get() 
                price = re.sub("[^\d\,]","", result_price) 
                price = float(price.replace(',','.'))
            except TypeError:

                result_price = response.xpath('//span[@id="current-price"]//text()').extract()
                price = re.sub("[^.\d\,]","", str(result_price)) 
                price = float(price.replace(',','.'))





#description

            try:
                description = response.xpath('//*[@id="description-tabs-content"]//text()').extract()
                description = ' '.join(description).split()
            except:
                description = response.xpath('//*[@id="product-description"]/p[2]//text()').extract()



           




            item = FragranceItem()
            item['brand'] = brand
            item['title'] = title
            item['price'] = price
            item['description'] = description
                

            yield item