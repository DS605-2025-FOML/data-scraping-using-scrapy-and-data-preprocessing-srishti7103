import scrapy
from ..items import BooksScraperItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]
    
    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BooksScraperItem()  #if we add item here,we get fresh new objects(notthe other way where the single object is repeated everytime item is is run in the program)
            item["title"] = book.css("h3 a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            item["rating"] = book.css("p.star-rating::attr(class)").get().replace("star-rating ", "")
            item["available_stocks"] = " ".join(book.css(".availability::text").getall()).strip()
            item["image_url"] = book.css("img::attr(src)").get()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

