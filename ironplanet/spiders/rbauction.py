import scrapy
import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.ironplanet.com.au/jsp/s/search.ips?pstart=0&l2=USA|CAN&sm=0&ms=R&k={}&mf=1'

class RbauctionSpider(scrapy.Spider):
    name = 'rbauction'
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

        products = response.xpath("//div[@class='sr_grid_tile sr_item ']")
        # print(len(products))
        for item in products:
            product_name = item.xpath("//div[@class='sr_photo_container sr_photo_grid_container']/a/img/@alt").get()
            # print(product_name)
            item_type = index
            # print(item_type)
            image = item.css(".sr_photo_container a img::attr(data-original)").get()          
            if "/images/space.gif" == image:
                image_link = "https://www.ironplanet.com.au/images/space.gif"                
            else:
                image_link = image
            product_url = item.css(".sr_grid_equip_desc a::attr(href)").get()  
            location = item.css("div.sr_price::text").get()
            # print(location) 
            auction_date = item.xpath("//*[@class='sr_grid_auc_info']/div[4]/text()").get()
            # print(auction_date) 
            lot_id = ""

    
            yield{
                'product_url' : product_url,
                'item_type' : item_type,
                'image_link' : image_link,
                'product_name': product_name,
                'auction_date' : auction_date,
                'location' : location,            
                'lot_id' : lot_id,
                'auctioner' : "",
                'website' : "rbauction"
            }
            


