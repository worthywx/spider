# -*- coding: utf-8 -*-
import re
import urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, url, html_cont):
        if url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_url(url, soup)
        new_data = self._get_new_data(url, soup)
        return new_urls, new_data

    def _get_new_url(self, url, soup):
        new_urls = set()

        links = soup.find_all('a', href=re.compile(r'/item/.+'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(url, new_url)
            new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, url, soup):
        res = {}

        res['url'] = url

        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res['title'] = title_node.get_text()

        summary_node = soup.find('div', class_='lemma-summary')
        res['summary'] = summary_node.get_text()
        return res
