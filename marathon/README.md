## MARATHONBET BASKETBALL CRAWLER TEST

# REQUIREMENTS [built on]
* Python 3.6.9
* Scrapy 1.8.0
* json-lines 0.5.0

# RUNNING
When inside directoy:
save data in data.jl
[$ scrapy crawl MarathonBasketball -o ./data.jl --nolog]

after uncommenting line 76 in spiders/basketball ... to view data without logs
[$ scrapy crawl MarathonBasketball --nolog]

... to view data and logs
[$ scrapy crawl MarathonBasketball]

