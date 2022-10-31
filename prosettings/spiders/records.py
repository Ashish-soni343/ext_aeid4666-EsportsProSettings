# importing required libraries
import scrapy
import datetime

from os import environ
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ProsettingsItem

# Here a spider named "RecordsSpider" is created and start url of the website are defined
class RecordsSpider(CrawlSpider):
    name = 'aeid-4666_prosettings_products'
    start_urls = ['https://prosettings.net/cs-go-pro-settings-gear-list/']

    # Mandatory data
    # AEID_project_id = ''
    site = 'https://prosettings.net/'
    source_country = 'Global'
    context_identifier = ''
    record_created_by = ""
    execution_id = "621614"  # This will be taken automatically from zyte, for now this is hardcoded
    feed_code = "AEID-4666"
    type = ""


    # settings for Crawling
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'COOKIES_DEBUG': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 500,
        'DOWNLOAD_DELAY': 0,
        'AUTOTHROTTLE_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 20,
        'DUPEFILTER_DEBUG': True,
    }
    # rule method to fetch url for different game listed in website
    rules = (
        Rule(LinkExtractor(
            restrict_css='li.menu-item.menu-item-type-custom.menu-item-object-custom.current-menu-ancestor.current-menu-parent.menu-item-has-children.menu-item-241 a', ),
             callback='parse_games'),
    )

    def parse_games(self, response):  # funtion to process data for each game

        item = ProsettingsItem()  # object to store data in "items.py"
        # list to take index of the data in the table
        list = [[2,4,13,15,19,20,21], [3,4,10,12,14,15,16], [2,4,11,13,16,17,18], [2,3,15,17,20,21,22], [2,4,13,15,18,19,20], [3,8,12,'a',9,10,11], [2,6,10,'a',7,8,9], [2,3,9,11,13,14,15]]
        # loop to identify table number which carries data within website
        for i in range(50, 70):
            table_order = f'#table_{i}_row_'
            t = 0
            if i == 55:
                listed = list[0]
            elif i == 57:
                listed = list[7]
            elif i == 53 or i == 64:
                listed = list[1]
            elif i == 58:
                listed = list[2]
            elif i == 59:
                listed = list[3]
            elif i == 60:
                listed = list[4]
            elif i == 66:
                listed = list[5]
            elif i == 68:
                listed = list[6]
            else:
                listed = list[0]
            try:
                if len(response.css(table_order + '1 td').extract()) != 0:
                    t = 100
                    if i == 61:
                        t = 0

            except:
                pass

            if t == 100:
                # loop to identify the length of row and fetch data from each row of the table
                for j in range(600):
                    row_no_n = f'{table_order}{j} td'
                    m = 0
                    try:
                        if len(response.css(row_no_n).extract()) != 0:
                            m = 100
                            print("m======j", j)
                    except:
                        pass
                    if m == 100:
                        try:
                            item["Feed_code"] = self.feed_code
                            item["Site"] = self.site
                            item["Source_country"] = self.source_country
                            item["Context_identifier"] = response.url.replace('https://prosettings.net/', "").replace('pro-settings-gear-list/', "").replace('-', " ")
                            item["Record_create_by"] = self.name
                            item['Execution_id'] = environ.get('SHUB_JOBKEY', None)
                            #item["Execution_id"] = self.execution_id
                            item["Page_Link"] = response.url
                            item["Record_create_dt"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')
                            item["Type"] = response.url.replace('https://prosettings.net/', "").replace('pro-settings-gear-list/', "").replace('-', " ")
                            str3, str4 = '<a href="', '" target='
                            # conditional logics to fetch player name, mouse, moniter, mouse_pad, keyboard, headset, GPU and their urls
                            if '</a></td>' in response.css(row_no_n).extract()[listed[0]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str1), response.css(row_no_n).extract()[listed[0]].index(str2)
                                item["Player_Name"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str3), response.css(row_no_n).extract()[listed[0]].index(str4)
                                item["Player_Link"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str3): idx2]
                            elif '</a> </td>' in response.css(row_no_n).extract()[listed[0]]:
                                str1, str2 = 'target="_blank">', '</a> </td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str1), response.css(row_no_n).extract()[listed[0]].index(str2)
                                item["Player_Name"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str3), response.css(row_no_n).extract()[listed[0]].index(str4)
                                item["Player_Link"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str3): idx2]
                            elif 'dth: 30px;">' in response.css(row_no_n).extract()[listed[0]]:
                                str1, str2 = 'dth: 30px;">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str1), response.css(row_no_n).extract()[listed[0]].index(str2)
                                item["Player_Name"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str1): idx2]
                                item["Player_Link"] = ""
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[0]].index(str1), response.css(row_no_n).extract()[listed[0]].index(str2)
                                item["Player_Name"] = response.css(row_no_n).extract()[listed[0]][idx1 + len(str1): idx2]
                                item["Player_Link"] = ""

                            if '</a></td>' in response.css(row_no_n).extract()[listed[1]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[1]].index(str1), response.css(row_no_n).extract()[listed[1]].index(str2)
                                item["Mouse_Name"] = response.css(row_no_n).extract()[listed[1]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[1]].index(str3), response.css(row_no_n).extract()[listed[1]].index(str4)
                                item["Mouse_Link"] = response.css(row_no_n).extract()[listed[1]][idx1 + len(str3): idx2]
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[1]].index(str1), response.css(row_no_n).extract()[listed[1]].index(str2)
                                item["Mouse_Name"] = response.css(row_no_n).extract()[listed[1]][idx1 + len(str1): idx2]
                                item["Mouse_Link"] = ""

                            if '</a></td>' in response.css(row_no_n).extract()[listed[2]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[2]].index(str1), response.css(row_no_n).extract()[listed[2]].index(str2)
                                item["Monitor_Name"] = response.css(row_no_n).extract()[listed[2]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[2]].index(str3), response.css(row_no_n).extract()[listed[2]].index(str4)
                                item["Monitor_Link"] = response.css(row_no_n).extract()[listed[2]][idx1 + len(str3): idx2]
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[2]].index(str1), response.css(row_no_n).extract()[listed[2]].index(str2)
                                item["Monitor_Name"] = response.css(row_no_n).extract()[listed[2]][idx1 + len(str1): idx2]
                                item["Monitor_Link"] = ""
                                if 'href' in response.css(row_no_n).extract()[listed[4]][idx1 + len(str1): idx2]:
                                    str1, str2 = '" target="_blank">', '</a></td>'
                                    str3, str4 = '</a><a href="', '" target='
                                    idx1, idx2 = (response.css(row_no_n).extract()[listed[2]][20:]).index(str1), (response.css(row_no_n).extract()[listed[2]]).index(str2)
                                    item["Monitor_Name"] = (response.css(row_no_n).extract()[listed[2]][20:])[idx1 + len(str1): idx2]
                                    idx1, idx2 = (response.css(row_no_n).extract()[listed[2]][20:]).index(str3), (response.css(row_no_n).extract()[listed[2]][20:]).index(str4)
                                    item["Monitor_Link"] = (response.css(row_no_n).extract()[listed[2]][20:])[idx1 + len(str3): idx2]

                            if listed[3] != 'a':
                                if '</a></td>' in response.css(row_no_n).extract()[listed[3]]:
                                    str1, str2 = '"_blank">', '</a></td>'
                                    idx1, idx2 = response.css(row_no_n).extract()[listed[3]].index(str1), response.css(row_no_n).extract()[listed[3]].index(str2)
                                    item["GPU_Name"] = response.css(row_no_n).extract()[listed[3]][idx1 + len(str1): idx2]
                                    idx1, idx2 = response.css(row_no_n).extract()[listed[3]].index(str3), response.css(row_no_n).extract()[listed[3]].index(str4)
                                    item["GPU_Link"] = response.css(row_no_n).extract()[listed[3]][idx1 + len(str3): idx2]
                                elif '</td>' in response.css(row_no_n).extract()[listed[3]]:
                                    str1, str2 = 'style="">', '</td>'
                                    idx1, idx2 = response.css(row_no_n).extract()[listed[3]].index(str1), response.css(row_no_n).extract()[listed[3]].index(str2)
                                    item["GPU_Name"] = response.css(row_no_n).extract()[listed[3]][idx1 + len(str1): idx2]
                                    item["GPU_Link"] = ""
                            else:
                                item["GPU_Name"] = ""
                                item["GPU_Link"] = ""

                            if '</a></td>' in response.css(row_no_n).extract()[listed[4]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[4]].index(str1), response.css(row_no_n).extract()[listed[4]].index(str2)
                                item["Mousepad_Name"] = response.css(row_no_n).extract()[listed[4]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[4]].index(str3),  response.css(row_no_n).extract()[listed[4]].index(str4)
                                item["Mousepad_Link"] = response.css(row_no_n).extract()[listed[4]][idx1 + len(str3): idx2]
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[4]].index(str1), response.css(row_no_n).extract()[listed[4]].index(str2)
                                item["Mousepad_Name"] = response.css(row_no_n).extract()[listed[4]][idx1 + len(str1): idx2]
                                item["Mousepad_Link"] = ""
                                if 'href' in response.css(row_no_n).extract()[listed[4]][idx1 + len(str1): idx2]:
                                    str1, str2 = 'target="_blank">', '</a></td>'
                                    str3, str4 = '<a href="', '" target='
                                    idx1, idx2 = response.css(row_no_n).extract()[listed[4]].index(str1), response.css(row_no_n).extract()[listed[4]].index(str2)
                                    item["Mousepad_Name"] = response.css(row_no_n).extract()[listed[4]][idx1 + len(str1): idx2]
                                    idx1, idx2 = response.css(row_no_n).extract()[listed[4]].index(str3), response.css(row_no_n).extract()[listed[4]].index(str4)
                                    item["Mousepad_Link"] = response.css(row_no_n).extract()[listed[4]][idx1 + len(str3): idx2]

                            if '</a></td>' in response.css(row_no_n).extract()[listed[5]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[5]].index(str1), response.css(row_no_n).extract()[listed[5]].index(str2)
                                item["Keyboard_Name"] = response.css(row_no_n).extract()[listed[5]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[5]].index(str3), response.css(row_no_n).extract()[listed[5]].index(str4)
                                item["Keyboard_Link"] = response.css(row_no_n).extract()[listed[5]][idx1 + len(str3): idx2]
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[5]].index(str1), response.css(row_no_n).extract()[listed[5]].index(str2)
                                item["Keyboard_Name"] = response.css(row_no_n).extract()[listed[5]][idx1 + len(str1): idx2]
                                item["Keyboard_Link"] = ""

                            if '</a></td>' in response.css(row_no_n).extract()[listed[6]]:
                                str1, str2 = '"_blank">', '</a></td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[6]].index(str1), response.css(row_no_n).extract()[listed[6]].index(str2)
                                item["Headset_Name"] = response.css(row_no_n).extract()[listed[6]][idx1 + len(str1): idx2]
                                idx1, idx2 = response.css(row_no_n).extract()[listed[6]].index(str3), response.css(row_no_n).extract()[listed[6]].index(str4)
                                item["Headset_Link"] = response.css(row_no_n).extract()[listed[6]][idx1 + len(str3): idx2]
                            else:
                                str1, str2 = 'style="">', '</td>'
                                idx1, idx2 = response.css(row_no_n).extract()[listed[6]].index(str1), response.css(row_no_n).extract()[listed[6]].index(str2)
                                item["Headset_Name"] = response.css(row_no_n).extract()[listed[6]][idx1 + len(str1): idx2]
                                item["Headset_Link"] = ""


                        except:
                            pass
                        yield item
