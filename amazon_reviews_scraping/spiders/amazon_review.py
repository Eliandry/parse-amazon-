import scrapy
import time
import re


class AmazonReviewSpider(scrapy.Spider):
    name = "amazon_review"
    allowed_domains = ['amazon.ae']

    def __init__(self, my_base_url='', *args, **kwargs):
        super(AmazonReviewSpider, self).__init__(*args, **kwargs)
        self.my_base_url = my_base_url

        self.start_urls = []

        k = self.my_base_url.split(sep='/')
        name = k[3]
        id = k[5]

        self.start_urls.append(self.my_base_url)

        sec = f'https://www.amazon.ae/{name}/product-reviews/{id}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2'

        self.start_urls.append(sec)

        for i in range(3, 11):
            if i < 7:
                next = f'https://www.amazon.ae/{name}/product-reviews/{id}/ref=cm_cr_getr_d_paging_btm_next_{i}?ie=UTF8&reviewerType=all_reviews&pageNumber={i}'
            else:
                next = f'https://www.amazon.ae/{name}/product-reviews/{id}/ref=cm_cr_getr_d_paging_btm_next_{i}?ie=UTF8&reviewerType=all_reviews&pageNu&pageNumber={i}'
            self.start_urls.append(next)


    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        star_rating = data.css('.review-rating')

        comments = data.css('.review-text')
        count = 0
        co = []
        for review in comments:
            time.sleep(2)
            d = ''.join(star_rating[count].xpath(".//text()").extract())
            star = "".join(c for c in d if c.isdecimal())[0]
            co.append(star)

            all_text = ''.join(review.xpath(".//text()").extract())
            text = re.sub(r'[^a-zA-Z0-9 ]', '', all_text)
            yield {'star': star, 'comment': text}
            count = count + 1
# .xpath(".//text()").extract()
