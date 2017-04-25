# -*- coding: utf-8 -*-
import scrapy
import sys
from urllib2 import quote

from urllib2 import quote
from foroOnmeda.items import forosOnmedaSpyder


class ForosPozSpider(scrapy.Spider):
    name = "onmeda"
    allowed_domains = ["onmeda.es"]
    custom_settings = {"SCHEDULER_DISK_QUEUE": 'scrapy.squeues.PickleFifoDiskQueue',
                       "SCHEDULER_MEMORY_QUEUE": 'scrapy.squeues.FifoMemoryQueue'}

    # constructor
    def __init__(self, *a, **kw):
        super(ForosPozSpider, self).__init__(*a, **kw)
        reload(sys)
        sys.setdefaultencoding("utf-8")

    # método que inicializa la url principal y la manda al método parse
    def start_requests(self):
        urls = 'http://www.onmeda.es/foros/'
        yield scrapy.Request(url=urls, callback=self.parse)

    # recibo la url de temas y empiezo el crawl
    def parse(self, response):
        # creo un xpath que recorre todos los titulos , textos  y url de cada tema
        items = response.xpath('//td[@class="cell-forum"]')
        item = forosOnmedaSpyder()
        for article in items:
            forum_url = article.xpath('.//div[@class="forum-info"]/a/@href').extract_first()
            forum_title = article.xpath('.//div[@class="forum-info"]/a/text()').extract_first()
            forum_text = article.xpath('.//div[@class="PhorumDescription"]/p/text()').extract_first()
            # creo un meta para ir insertando nuestros datos
            meta = {'forum_url': forum_url,
                    'forum_title': forum_title,
                    'forum_text': forum_text,
                    }
            # para probar solo con una url de un tema
            if forum_url == "http://www.onmeda.es/foros/contracepción":
                yield scrapy.Request(forum_url, callback=self.parse_urlsPagAsuntos, meta=meta)


    def parse_urlsPagAsuntos(self, response):
        # recibo  el meta
        meta = response.meta
        # creo un xpath que recorre todos los titulos de asuntos ,nombre de users que han creado el post y la url del post
        items = response.xpath('//td[@class="cell-topic js-cell-topic"]')
        for article in items:
            subject_url = article.xpath('.//a[@class="topic-title js-topic-title"]/@href').extract_first()
            subject_title = article.xpath('.//a[@class="topic-title js-topic-title"]/text()').extract_first()
            subject_user = article.xpath(
                './/div[@class="topic-info h-clear h-hide-on-small h-hide-on-narrow-column"]/a/text()').extract_first()
            # le añado al meta que recibo mas datos
            meta['subject_url'] = subject_url
            meta['subject_title'] = subject_title
            meta['subject_user'] = subject_user
            yield scrapy.Request(subject_url, callback=self.parse_urlsPagPost, meta=meta)

    def parse_urlsPagPost(self, response):
        # recibo los datos del  meta
        meta = response.meta
        # creo un xpath que recorre todos los userPost,totalMesUser,karma,date y textPost
        items = response.xpath('//div[@class="l-row l-row__fixed--left"]')
        for article in items:
            post_user = article.xpath('.//div[@class="author h-text-size--14"]//a/text()').extract_first()
            post_member_group = article.xpath('.//div[@class="usertitle"]/text()').extract_first().strip()
            post_date = article.xpath('.//div[@class="b-post__timestamp OLD__post-date"]/time/text()').extract_first()
            post_count = article.xpath('.//li[@class="b-userinfo__additional-info"][2]/span/text()').extract_first()
            post_text = article.xpath('.//div[@class="js-post__content-text OLD__post-content-text restore h-wordwrap"]//text()').extract()
            # cogemos el texto y lo metemos como parametro al metodo clean para que nos deje solo el texto sin espacios
            post_text = self.clean_and_flatten(post_text)
            # url de cada usuario para poder obtener los datos del usuario
            user_url = article.xpath('.//div[@class="author h-text-size--14"]//a/@href').extract_first()
            # le añado al meta que recibo mas datos
            meta['post_user'] = post_user
            meta['post_member_group'] = post_member_group
            meta['post_date'] = post_date
            meta['post_count'] = post_count
            meta['post_text'] = post_text
            meta['user_url'] = user_url
            meta['user_location'] = None
            meta['user_date_registered'] = None
            yield self.create_item(meta)


    # método para eliminar los espacios en blanco de los textos
    def clean_and_flatten(self, text_list):
        clean_text = []
        for text_str in text_list:
            if text_str == None:
                continue
            if len(text_str.strip()) > 0:
                clean_text.append(text_str.strip())

        return "\n".join(clean_text).strip()


    # método para armar el item con los datos que hemos ido añadiendo al meta
    def create_item(self, meta):
        item = forosOnmedaSpyder()
        item['forum_url'] = meta['forum_url']
        item['forum_title'] = meta['forum_title']
        item['forum_text'] = meta['forum_text']
        item['subject_url'] = meta['subject_url']
        item['subject_user'] = meta['subject_user']
        item['subject_title'] = meta['subject_title']
        item['post_user'] = meta['post_user']
        item['post_member_group'] = meta['post_member_group']
        item['post_date'] = meta['post_date']
        item['post_count'] = meta['post_count']
        item['post_text'] = meta['post_text']
        item['user_url'] = meta['user_url']
        item['user_location'] = meta['user_location']
        item['user_date_registered'] = meta['user_date_registered']

        return item



