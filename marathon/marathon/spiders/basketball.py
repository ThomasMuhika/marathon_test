"""
Basketball spider test
target: https://www.marathonbet.com
data needed: game_url category gametime event_names/team_names game_odds overtime_in_match half_with_most_points
"""
import scrapy


class MarathonBasketball(scrapy.Spider):
    name = 'MarathonBasketball'

    pagination_url = 'https://www.marathonbet.com/en/popular/Basketball?page={}'
    start_urls = [pagination_url.format(0)]

    BASE_URL = 'https://www.marathonbet.com'

    def parse(self, response):
        links = response.xpath(".//a[@class='member-link']/@href").extract()
        links = list(dict.fromkeys(links))

        for link in links:
            absolute_url = self.BASE_URL + link
            # print(absolute_url)
            yield scrapy.Request(absolute_url, callback=self.parse_game, meta={'game_url': absolute_url})

    def parse_game(self, response):
        # game url
        absolute_url = response.meta.get('game_url')
        # print(absolute_url)

        # game category
        country = response.xpath(".//h1[@class='category-label ']/span/text()").extract_first().replace(".", "")
        league = response.xpath(".//h1[@class='category-label ']/span/text()").extract()[1:]

        category = [country, league]
        # print(category)

        # game time
        game_time = response.xpath(".//td[starts-with(@class, 'date')]/text()").extract_first().strip()
        # print(game_time)

        # team names
        teams = response.xpath(".//div[contains(@class, 'member-name nowrap')]/a/span/text()").extract()
        if len(teams) == 2:
            teams = str(teams[0]) + ' vs ' + str(teams[1])
        # print(teams)

        # game odds (1, 2)
        game_odds = response.xpath(".//td[@data-market-type='RESULT_2WAY']/span/text()").extract()
        # print(game_odds)

        market_headers = response.xpath(".//div[@class='name-field']/text()").extract()
        for market_header in market_headers:
            market_header_unstyled = market_header.strip().lower()

            # overtime in match
            if market_header_unstyled == 'overtime in match':
                ovm = response.xpath(".//div[.//table[@class='market-table-name' and .//tr[.//td[.//div[@class='name-field' and text()='" + market_header + "']]]]]/table[@class='td-border table-layout-fixed ']/tr/td/span/text()").extract()
                # print(ovm)

            # half with most points
            elif market_header_unstyled == 'half with most points':
                hwmp = response.xpath(".//div[.//table[@class='market-table-name' and .//tr[.//td[.//div[@class='name-field' and text()='" + market_header + "']]]]]/table[@class='td-border table-layout-fixed ']/tr/td[contains(@class, 'price')]/span/text()").extract()
                # print(hwmp)

            try:
                ovm
            except NameError:
                ovm = None

            try:
                hwmp
            except NameError:
                hwmp = None

            # print(str(absolute_url) + "\n" + str(category) + "\n" + str(game_time) + "\n" + str(teams) + "\n" + str(game_odds) + "\n" + str(ovm) + "\n" + str(hwmp) + "\n")

            yield {
                'url': absolute_url,
                'category': category,
                'game_time': game_time,
                'teams': teams,
                'game_odds': game_odds,
                'ovm': ovm,
                'hwmp': hwmp,
            }


