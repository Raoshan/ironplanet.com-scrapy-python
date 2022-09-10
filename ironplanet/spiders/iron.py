import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.ironplanet.com/jsp/s/search.ips?pstart=0&ms=G|I|M|S|T&sm=0&k={}&mf=1'

class IronSpider(scrapy.Spider):
    name = 'iron'
    # allowed_domains = ['ironplanet.com.au']
    def start_requests(self):        
        for index in df:            
            yield scrapy.Request(base_url.format(index),cb_kwargs={'index':index})

    def parse(self, response, index):
        print("***************")
        print(response.url, index)
        # print(response.css('.sr_results_header strong::text').get())        
        # links = response.css(".sr_equip_desc a::attr(href)")
        # for link in links:            
        #     yield response.follow("https://www.ironplanet.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})
        
        page = response.css('a.sr_pagination::attr(href)').get() 
        print(page)              
        if page is not None:   
            next_url = "https://www.ironplanet.com"+page        
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, cb_kwargs={'index':index})
    # def parse_item(self, response, index): 
    #     print("........................")
    #     link = response.url
    #     print(link)
    #     item_type = index
    #     print(item_type)
    #     image = response.xpath('//*[@id="photoBlock1"]/@src').extract()[0]
    #     print(image)
    #     name = response.css("h1.itemdesc::text").extract()[0]
    #     print(name)
    #     auction_date = response.css(".IP_PriceMsg::text").get()
    #     print(auction_date)
        


       

        