import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.ironplanet.com.au/jsp/s/search.ips?pstart=0&ms=G|I|M|S|T&sm=0&k={}&mf=1'

class IronSpider(scrapy.Spider):
    name = 'irons'
    allowed_domains = ['ironplanet.com.au']
    def start_requests(self):        
        for index in df:            
            yield scrapy.Request(base_url.format(index),cb_kwargs={'index':index})

    def parse(self, response, index):
        """Pagination"""
        total_pages = response.xpath("//*[@class='sr_page_numbers']/a[last()-1]//text()").get()
        current_page =response.css('.sr_curr_page_number::text').get()
        url = response.url      
        
        if total_pages and current_page:
            if int(current_page) ==1:
                pstart = 0
                min = 0
                for i in range(2, int(total_pages)+1):                     
                    pstart = pstart+60                    
                    if i>=3:   
                        min = min+60      
                        s2 =  'pstart='+str(min)  
                        s1 = 'pstart='+str(pstart)    
                        url = url.replace(s2,s1)
                        yield response.follow(url, cb_kwargs={'index':index})
                    else:        
                        url = url.replace('pstart=0','pstart=60')
                        yield response.follow(url, cb_kwargs={'index':index})

        links = response.css(".sr_equip_desc a::attr(href)")
        for link in links:            
            yield response.follow("https://www.ironplanet.com.au"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})
        
        
    def parse_item(self, response, index): 
        
        link = response.url        
        item_type = index
        lot_id = response.css('span.itemPropValue::text').extract()[0]
        try:
            image = response.xpath('//*[@id="photoBlock1"]/@src').extract()[0]            
        except:
            image = "https://www.ironplanet.com.au/images/space.gif"   

        name = response.css("h1.itemdesc::text").extract()[0] 
        location = response.css('div.itemPropValue::text').extract()[0]
        try:
            auction_date = response.css(".IP_TimeBox nobr::text").get()
        except Exception:
            try:
                auction_date = response.xpath("//div[2]/span/span[2]/text()").get()                
            except Exception:
                try:
                    auction_date = response.css(".IP_PriceMsg::text").get()                    
                except:
                    auction_date = ""        
    
        yield{
            'product_url' : link,
            'item_type' : item_type,
            'image_link' : image,
            'product_name': name,
            'auction_date' : auction_date,
            'location' : location,            
            'lot_id' : lot_id,
            'auctioner' : "",
            'website' : "ironplanet"
        }
        


   