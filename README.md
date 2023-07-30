# UNSW Arc Website Scraper

The data scraped is no longer relevant, and I am not interested in fixing this project. You may still have a look through it if you are interested. ARC updated its website.


python scraper to get club data from [https://www.arc.unsw.edu.au/](https://www.arc.unsw.edu.au/)

## How to run

```console
$ git clone git@github.com:HARI-PRMD/unsw-arc-scraper.git
$ pip install -r requirements.txt
$ python scraper.py
```

## How does it work?

1. the scraper first gets a full list of the clubs from [https://arc-discovery.linkupevents.com/](https://arc-discovery.linkupevents.com/club/) which is stored in `/data/all_club_names.json`
2. then it gets each club page by calling [https://arc-discovery.linkupevents.com/club/](https://arc-discovery.linkupevents.com/club/ClubNameHere)
3. then it gets the JSON object from the `<script>` tag of the page
4. finally this data is stored in `/data/all_club_data.json` for you to use however you want
