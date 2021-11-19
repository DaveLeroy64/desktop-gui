***DESKTOP GUI***

For controlling a number of mini-projects from the same place and visualising data


Features:
1. Property scraper

![Image of property main screen](https://imgur.com/tbXg7kC)

    - Gathers property listings from a chosen city, to a certain radius, and stores them in a DB
    - Displays properties with details of bedrooms, price, agent contact, link, etc
    - Stores average price per city and plots line chart over time
    - Displays average price/bedroom per area
2. Polscraper
    - Scrapes 4chan and stories threads/posts to JSON "reports"
    - Scraper can be run once per click or set to run at intervals
    - Analyses/scans each report for offensive language and common topics - WARNING: 4chan users use ***extremely*** offensive language which is searched for by this script
    - Displays data from these reports in multiple formats (most frequent topics by nationality, time, etc)
3. News scraper
    - Displays news items on main page
    - Stores to a local DB and replaces front page with newer stories

Each feature runs in its own thread to avoid interfering with others.

To do:

- General
    - Refresh Thread - it does sort of work but it doesn't change the status display. Fix this.

- News scraper
    - Home page display to display most recent stories in database for each outlet. 

- Property scraper
    - Add a popup to property scraper if there are more than 50 pages to confirm if you want to continue

- Polscraper
    - Boolean "apply weighting" tickbox to polscraper data to weigh down 'topics' that are ridiculously overused
    - Remove datagraph.clear() statements as default whenever graph is populated - only when button is hit. This way you can overlay different data maybe?

- HomeBot integration
    - Control computer remotely using telegram bot as authorised user.
