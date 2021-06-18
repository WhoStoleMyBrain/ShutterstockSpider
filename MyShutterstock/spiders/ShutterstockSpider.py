#!/usr/bin/python3

import scrapy
import sys
#sys.path.append('/home/ubedl/MachineLearning/Bilderkennung/MyShutterstock')
from MyShutterstock.items import MyShutterstockItem

class ShutterstockSpider(scrapy.Spider):
	name = "ShutterstockSpider"
	start_urls = [
			#'http://quotes.toscrape.com/page/1',
			#'http://quotes.toscrape.com/page/2',
			'https://www.shutterstock.com/search/nestle+product',
	]
	#self.start_urls = start_urls
	
	def parse(self, response):
		#for href in response.xpath("//div[contains(., 'mosaic-grid-cell-')]"):
		for ref in response.xpath("//a[@data-automation='mosaic-grid-cell-anchor']"):

			#img = ref.css("div a img").xpath("@src")
			#img = ref.css("img[data-automation='mosaic-grid-cell-image']").xpath("@src")
			img = ref.css("img[data-automation='mosaic-grid-cell-image']").xpath("@src")
			#print('ref:', ref.css("img[data-automation='mosaic-grid-cell-image']"), 'img:', img)
			#div.z_g_63ded:nth-child(2) > div:nth-child(1) > a:nth-child(2)
			imageURL = img.extract_first()
			yield MyShutterstockItem(file_urls = [imageURL])
			#yield scrapy.Request(href.xpath("@href").extract_first(), self.parse_covers)

#/html/body/div[1]/div[2]/div/div[2]/div[2]/main/div/div[2]/div[2]/div
#/html/body/div[1]/div[2]/div/div[2]/div[2]/main/div/div[2]/div[2]/div
		next = response.css(".o_n_38556").xpath(".//div//a[@aria-label='Next page']")#o_n_d3df5 b_aI_4257a
		#next = response.css("div[data-automation=SearchResultsTopNav_paginationContainer]").xpath("//div//a[@label='Next page']")#o_n_d3df5 b_aI_4257a
		#print('next:', next, 'url:', "/".join(self.start_urls[0].split('/')[:3]))
		yield scrapy.Request("/".join(self.start_urls[0].split('/')[:3]) + next.xpath("@href").extract_first(), self.parse)

	def parse_covers(self, response):
		#img = response.css(".art-cover-photo figure a img").xpath("@src")
		#img = response.css(".z_g_63ded z_h_b900b z_h_81767 img").xpath("@src")
		img = response.css("div[data-automation='mosaic-grid-cell-'] div a img").xpath("@src")
		imageURL = img.extract_first()

		title = response.css(".content-main-aside h1::text").extract_first()
		#year = response.css(".content-main-aside h1 time a:text").extract_first()
		#month = response.css(".content-main-aside h1 time::text").extract_first()[:-2]

		#date = "{} {}".format(month, year).replace(".", "")
		#d = datetime.datetime.strptime(date, "%b %d %y")
		#pub = "{} {} {}".format(d.year, str(d.month).zfill(2), str(d.day).zfill(2))

		#yield MyShutterstockItem(title=title, pubDate = pub, file_urls = [imageURL])
		yield MyShutterstockItem(title=title, file_urls = [imageURL])

	'''

	def parse(self, response):
		#url = response.css("div.refineCol ul li").xpath("a[contains(., 'Nestle')]")
		url = response.css("div.content z_g_d65b1").xpath("z_g_63ded")
		yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_page)

	def parse_page(self, response):
		for href in response.xpath("//a[contains(., 'LargeCover')]"):
			yield scrapy.Request(href.xpath("@href").extract_first(), self.parse_covers)

		next = response.css("div.pages").xpath("a[contains(., 'Next')]")
		yield scrapy.Request(next.xpath("@href").extract_first(), self.parse_page)
#####################
	def start_requests(self):
		urls = [
			#'http://quotes.toscrape.com/page/1',
			#'http://quotes.toscrape.com/page/2',
			'https://www.shutterstock.com/search/nestle+product',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = f'quotes-{page}.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		self.log(f'Saved file {filename}')
	'''

#https://www.shutterstock.com/search/nestle+product