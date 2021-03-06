from .base import Scraper


class SeasonDataScraper(Scraper):
    url = 'https://en.wikipedia.org/wiki/List_of_Manchester_United_F.C._seasons'

    @classmethod
    def get_remark_from_bgcolor(cls, bgcolor):
        dct = {
            '#DDD': 'Runners-up',
            '#FCC': 'Relegated',
            '#FE2': 'Champions',
            '#DFD': 'Promoted',
        }
        if bgcolor in dct:
            return dct[bgcolor]
        return bgcolor

    @classmethod
    def get_remark_from_cell(cls, cell):
        return cls.get_remark_from_bgcolor(cls.get_style(cell, 'background-color'))

    @classmethod
    def scrape(cls):
        root = cls.get_root_tree()
        if root is not None:
            table = root.xpath('//h2/span[@id="Seasons"]/..//following-sibling::table')[0]
            rows = table.xpath('tr')[2:]
            dct = {}
            for row in rows:
                columns = row.getchildren()
                if columns:
                    year = columns[0].text_content()[0:4]
                    if columns[0].xpath('.//a'):
                        data = {'wiki_url': columns[0].xpath('.//a')[0].attrib['href']}
                        if cls.gwcc(columns[1]):
                            data['division'] = cls.gwcc(columns[1])
                        if cls.gwcc(columns[2]):
                            data['P'] = cls.gwcc(columns[2])
                        if cls.gwcc(columns[3]):
                            data['W'] = cls.gwcc(columns[3])
                        if cls.gwcc(columns[4]):
                            data['D'] = cls.gwcc(columns[4])
                        if cls.gwcc(columns[5]):
                            data['L'] = cls.gwcc(columns[5])
                        if cls.gwcc(columns[6]):
                            data['F'] = cls.gwcc(columns[6])
                        if cls.gwcc(columns[7]):
                            data['A'] = cls.gwcc(columns[7])
                        if cls.gwcc(columns[8]):
                            data['Pts'] = cls.gwcc(columns[8])
                        if cls.gwcc(columns[9]):
                            data['Pos'] = {'value': cls.gwcc(columns[9])}
                            if cls.get_style(columns[9], 'background-color'):
                                data['Pos']['remarks'] = cls.get_remark_from_cell(columns[9])
                        if cls.gwcc(columns[10]):
                            data['FA'] = {'value': cls.gwcc(columns[10])}
                            if cls.get_style(columns[10], 'background-color'):
                                data['FA']['remarks'] = cls.get_remark_from_cell(columns[10])
                        if cls.gwcc(columns[11]):
                            data['League'] = {'value': cls.gwcc(columns[11])}
                            if cls.get_style(columns[11], 'background-color'):
                                data['League']['remarks'] = cls.get_remark_from_cell(columns[11])
                        if cls.gwcc(columns[12]):
                            data['Community'] = cls.gwcc(columns[12])
                            data['Community'] = {'value': cls.gwcc(columns[12])}
                            if cls.get_style(columns[12], 'background-color'):
                                data['Community']['remarks'] = cls.get_remark_from_cell(columns[12])
                        if cls.gwcc(columns[13]):
                            # test for multiple achievements
                            if columns[13].xpath('*/ul'):
                                achievements = []
                                achievements_li = columns[13].xpath('*/ul')[0].getchildren()
                                for achievement_li in achievements_li:
                                    result = achievement_li.text_content().strip()
                                    result_splitted = result.split(u'\u2013')
                                    achievement = {'cup': result_splitted[0].strip(), 'value': result_splitted[1].strip()}
                                    if achievement_li.getchildren() and achievement_li.getchildren()[0].tag == 'div':
                                        achievement['remarks'] = cls.get_remark_from_cell(achievement_li.getchildren()[0])
                                    achievements.append(achievement)
                                data['International'] = achievements
                            else:
                                result = columns[13].getchildren()[1].text_content().strip()
                                result_splitted = result.split(u'\u2013')
                                data['International'] = [
                                    {'cup': result_splitted[0].strip(), 'value': result_splitted[1].strip()}
                                ]
                                if cls.get_style(columns[13], 'background-color'):
                                    data['International'][0]['remarks'] = cls.get_remark_from_cell(columns[13])

                        if cls.gwcc(columns[14]):
                            players = []
                            player_links = columns[14].xpath('.//a')
                            for player_link in player_links:
                                if player_link.getparent().tag == 'sup':
                                    continue
                                players.append({'name': player_link.text_content(), 'wiki_url': player_link.attrib['href']})
                            data['top_scorers'] = players

                        if cls.gwcc(columns[15]):
                            data['top_score'] = cls.gwcc(columns[15])

                        if 'division' in data and data['division'] == 'Not held':
                            pass
                        else:
                            dct[year] = data

            cls.data = dct

    @classmethod
    def save(cls):
        from apps.stats.models import SeasonData

        for season, data in cls.data.iteritems():
            season_data, created = SeasonData.objects.get_or_create(year=season)
            season_data.summary = data
            season_data.save()