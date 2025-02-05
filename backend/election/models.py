import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import folium
import json
import warnings
from common.models import FileDTO, Printer, Reader
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup


class Election_19th(Reader):

    def __init__(self):
        self.f = FileDTO()
        self.r = Reader()
        self.p = Printer()
        self.BORDER_LINES = [
            [(5, 1), (5,2), (7,2), (7,3), (11,3), (11,0)], # 인천
            [(5,4), (5,5), (2,5), (2,7), (4,7), (4,9), (7,9),
             (7,7), (9,7), (9,5), (10,5), (10,4), (5,4)], # 서울
            [(1,7), (1,8), (3,8), (3,10), (10,10), (10,7),
             (12,7), (12,6), (11,6), (11,5), (12, 5), (12,4),
             (11,4), (11,3)], # 경기도
            [(8,10), (8,11), (6,11), (6,12)], # 강원도
            [(12,5), (13,5), (13,4), (14,4), (14,5), (15,5),
             (15,4), (16,4), (16,2)], # 충청북도
            [(16,4), (17,4), (17,5), (16,5), (16,6), (19,6),
             (19,5), (20,5), (20,4), (21,4), (21,3), (19,3), (19,1)], # 전라북도
            [(13,5), (13,6), (16,6)], # 대전시
            [(13,5), (14,5)], #세종시
            [(21,2), (21,3), (22,3), (22,4), (24,4), (24,2), (21,2)], #광주
            [(20,5), (21,5), (21,6), (23,6)], #전라남도
            [(10,8), (12,8), (12,9), (14,9), (14,8), (16,8), (16,6)], #충청북도
            [(14,9), (14,11), (14,12), (13,12), (13,13)], #경상북도
            [(15,8), (17,8), (17,10), (16,10), (16,11), (14,11)], #대구
            [(17,9), (18,9), (18,8), (19,8), (19,9), (20,9), (20,10), (21,10)], #부산
            [(16,11), (16,13)], #울산
            [(27,5), (27,6), (25,6)],]
        self.election_result_raw = {'광역시도': [],
                                    '시군': [],
                                    'pop': [],
                                    'moon': [],
                                    'hong': [],
                                    'ahn': []}
        self.wait = WebDriverWait(self.driver, 10)
        self.sido_names_values = [
            '▷ 전 체',
            '서울특별시',
            '부산광역시',
            '대구광역시',
            '인천광역시',
            '광주광역시',
            '대전광역시',
            '울산광역시',
            '세종특별자치시',
            '경기도',
            '강원도',
            '충청북도',
            '충청남도',
            '전라북도',
            '전라남도',
            '경상북도',
            '경상남도',
            '제주특별자치도']

    @staticmethod
    def get_num(tmp):
        return float(re.split('\(', tmp)[0].replace(',', ''))

    def append_data(self, df, sido_name):
        data = self.election_result_raw
        for each in df[0].values[1:]:
            data['광역시도'].append(sido_name)
            data['시군'].append(each[0])
            data['pop'].append(each[2])
            data['moon'].append(self.get_num(str(each[3])))
            data['hong'].append(self.get_num(str(each[4])))
            data['ahn'].append(self.get_num(str(each[5])))
        self.election_result_raw = data

    def get_table(self):
        driver = self.driver
        actions = ActionChains(driver)
        driver.get(
            'http://info.nec.go.kr/main/showDocument.xhtml?electionId=0000000000&topMenuId=VC&secondMenuId=VCCP09')
        driver.implicitly_wait(2)
        driver.find_element_by_id('electionType1').click()
        menu1 = driver.find_element_by_id("electionName")
        menu1.send_keys("제19대")
        # when menu1 is not clicked, the code halts.
        menu1.click()
        # when chained as find().send_keys(), doesn't work
        menu2 = driver.find_element_by_id("electionCode")
        menu2.send_keys('대통령선거')
        # whether menu2 is clicked doesn't make any difference.
        # menu2.click()
        sido_list_raw = driver.find_elements_by_tag_name('select')
        for i in sido_list_raw:
            # don't know exactly why, but the below code seems to play a critical roll
            print(i.text)
        opt_elements = sido_list_raw[2].find_elements_by_tag_name('option')
        # the code right below seems to play a roll
        opt_elements[1].click()
        sido_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""")
        opt_elements_by_xpath = sido_list_raw.find_elements_by_tag_name('option')
        opt_elements_by_xpath[0].click()
        for i in opt_elements_by_xpath:
            print(i.text)
        opt_elements_by_xpath[1].click()
        opt_elements_by_xpath[1].click()
        opt_elements_by_xpath[1].click()
        opt_elements_by_xpath[1].click()
        opt_elements_by_xpath[1].click()
        sido_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""")
        opt_elements_by_xpath = sido_list_raw.find_elements_by_tag_name('option')
        for i in opt_elements_by_xpath:
            print(i.text)

        for i, each_sido in enumerate(self.sido_names_values):

            element = driver.find_element_by_id("cityCode")
            element.send_keys(each_sido)
            make_xpath = """//*[@id="searchBtn"]"""
            self.wait.until(EC.element_to_be_clickable((By.XPATH, make_xpath)))
            sido_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""")
            opt_elements_by_xpath = sido_list_raw.find_elements_by_tag_name('option')
            for i in opt_elements_by_xpath:
                print(i.text)
            driver.find_element_by_xpath(make_xpath).click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')

            df = pd.read_html(str(table))

            self.append_data(df, each_sido)

        temp_keys = list(self.election_result_raw.keys())
        temp_values = list(self.election_result_raw.values())
        for i, j in enumerate(temp_values):
            temp_values[i] = j[17:]

        election_result_trimmed = {}
        for i, j in enumerate(temp_keys):
            election_result_trimmed[j] = temp_values[i]

        self.election_result_raw = election_result_trimmed

        election_result = pd.DataFrame(self.election_result_raw,
                                       columns=['광역시도', '시군', 'pop', 'moon', 'hong', 'ahn'])

        election_result.to_csv('./data_saved/final_elect_data.csv', encoding='utf-8', sep=',')
        driver.close()

    def get_rate(self):
        election_result = pd.read_csv('./saved_data/election_result.csv', encoding='utf-8', index_col=0)
        # print(election_result.head())
        sido_candi = election_result['광역시도']
        sido_candi = [name[:2] if name[:2] in ['서울', '부산', '대구', '광주', '인천', '대전', '울산'] else '' for name in sido_candi]
        # print(sido_candi)
        sigun_candi = [''] * len(election_result)
        # print(sigun_candi)
        # print(type(sigun_candi))
        for n in election_result.index:
            each = election_result['시군'][n]
            if each[:2] in ['수원', '성남', '안양', '안산', '고양',
                            '용인', '청주', '천안', '전주', '포항', '창원']:
                sigun_candi[n] = re.split('시', each)[0] + ' ' + self.cut_char_sigu(re.split('시', each)[1])
            else:
                sigun_candi[n] = self.cut_char_sigu(each)
        '''
        print(len(sigun_candi))
        print(len(sido_candi))
        for i, j in enumerate(sido_candi):
            if j == '':
                print(f'{i}th element is empty')'''

        ID_candi = [sido_candi[n] + ' ' + sigun_candi[n] for n in range(0, len(sigun_candi))]

        ID_candi = [name[1:] if name[0] == ' ' else name for name in ID_candi]
        ID_candi = [name[:2] if name[:2] == '세종' else name for name in ID_candi]

        # print(ID_candi)

        election_result['ID'] = ID_candi

        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] \
            = election_result[['moon', 'hong', 'ahn']].div(election_result['pop'], axis=0)
        election_result[['rate_moon', 'rate_hong', 'rate_ahn']] *= 100

        draw_korea = pd.read_csv('./data/draw_korea.csv', encoding='utf-8', index_col=0)
        # print(draw_korea.head(10))

        election_result.loc[125, 'ID'] = '고성(강원)'
        election_result.loc[233, 'ID'] = '고성(경남)'

        election_result.loc[228, 'ID'] = '창원 합포'
        election_result.loc[229, 'ID'] = '창원 회원'

        # print(election_result.loc[85])
        # 부천이 3개 지역구로 나뉘어져서 (draw korea) 수는 나누고 rate 는 따로 temp 에 저장
        ahn_tmp = election_result.loc[85, 'ahn'] / 3
        hong_tmp = election_result.loc[85, 'hong'] / 3
        moon_tmp = election_result.loc[85, 'moon'] / 3
        pop_tmp = election_result.loc[85, 'pop'] / 3

        rate_moon_tmp = election_result.loc[85, 'rate_moon']
        rate_hong_tmp = election_result.loc[85, 'rate_hong']
        rate_ahn_tmp = election_result.loc[85, 'rate_ahn']

        # 꼬리에 부천을 소사, 오정, 원미 로 나누어서 추가
        election_result.loc[250] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp, '경기도', '부천시', '부천 소사',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[251] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp, '경기도', '부천시', '부천 오정',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]
        election_result.loc[252] = [ahn_tmp, hong_tmp, moon_tmp, pop_tmp, '경기도', '부천시', '부천 원미',
                                    rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp]

        # drop the original observation
        election_result.drop([85], inplace=True)

        # merge the election data and regional data
        final_elect_data = pd.merge(election_result, draw_korea, how='left', on=['ID'])

        final_elect_data['moon_vs_hong'] = final_elect_data['rate_moon'] - final_elect_data['rate_hong']
        final_elect_data['moon_vs_ahn'] = final_elect_data['rate_moon'] - final_elect_data['rate_ahn']
        final_elect_data['ahn_vs_hong'] = final_elect_data['rate_ahn'] - final_elect_data['rate_hong']
        self.final_table = final_elect_data

    def draw_data(self, tar_dara, campname):
        f = self.f
        r = self.r
        BORDER_LINES = self.BORDER_LINES
        f.context = './data_saved/'
        f.fname = 'final_elect_data'
        elec = r.csv(f)
        gamma = 0.75
        whitelabelmin = 20.
        datalabel = tar_dara
        tmp_max = max([np.abs(min(elec[tar_dara])),
                       np.abs(max(elec[tar_dara]))])
        vmin, vmax = -tmp_max, tmp_max
        mapdata = elec.pivot_table(index='y', columns='x', values=tar_dara)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
        plt.rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=campname,
                   edgecolor='#aaaaaa', linewidth=0.5)
        # 지역 이름 표시
        for idx, row in elec.iterrows():
            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시
            # (중구, 서구)
            if len(row['ID'].split()) == 2:
                dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
            elif row['ID'][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row['ID']
            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.
            annocolor = 'white' if np.abs(row[tar_dara]) > whitelabelmin else 'black'
            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)
        # 시도 경계
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)

        plt.gca().invert_yaxis()
        plt.axis('off')
        cb = plt.colorbar(shrink=.1, aspect=10)
        cb.set_label(datalabel)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def cut_char_sigu(name):
        return name if len(name) == 2 else name[:-1]

    def folium_map(self, tar_data):
        f = self.f
        r = self.r
        f.context = './data_saved/'
        f.fname = 'final_elect_data'
        elec = r.csv(f)
        warnings.simplefilter(action='ignore', category=FutureWarning)
        pop_folium = elec.set_index('ID')
        del pop_folium['광역시도']
        del pop_folium['시군']
        pop_folium.head()
        geo_path = 'data_saved/05. skorea_municipalities_geo_simple.json'
        geo_str = json.load(open(geo_path, encoding='utf-8'))
        map = folium.Map(location=[36.2002, 127.054], zoom_start=6)
        map.choropleth(geo_data=geo_str,
                       data=pop_folium[tar_data],
                       columns=[pop_folium.index, pop_folium[tar_data]],
                       fill_color='YlGnBu',  # PuRd, YlGnBu
                       key_on='feature.id')
        map.save(f'./data_saved/election_{tar_data}.html')

'''
    @staticmethod
    def main():
        e = Election_19th()
        while 1:
            m = input('0. break\n'
                      '1. moon_vs_hong\n'
                      '2. moon_vs_ahn\n'
                      '3. ahn_vs_hong\n'
                      '4. folium n.1\n'
                      '5. folium n.2\n'
                      '6. folium n.3\n')
            if m == '0':
                break
            elif m == '1':
                e.draw_data('moon_vs_hong', 'RdBu')
            elif m == '2':
                e.draw_data('moon_vs_ahn', 'RdBu')
            elif m == '3':
                e.draw_data('ahn_vs_hong', 'RdBu')
            elif m == '4':
                e.folium_map('moon_vs_hong')
            elif m == '5':
                e.folium_map('moon_vs_ahn')
            elif m == '6':
                e.folium_map('ahn_vs_hong')
            else:
                continue

'''
#Election_19th.main()

