***DESKTOP GUI***

For controlling a number of mini-projects from the same place and visualising data

<img src="https://i.imgur.com/MMiERer.jpg" alt="alt text" title="image Title" />


Features:
1. Property scraper

- Gathers property listings from a chosen city, to a certain radius, and stores them in a DB
<img src="https://i.imgur.com/tbXg7kC.jpg" alt="alt text" title="image Title" />

- Displays properties with details of bedrooms, price, agent contact, link, etc
<img src="https://i.imgur.com/R1pEEqY.jpg" alt="alt text" title="image Title" />

- Stores average price per city and plots line chart over time
<img src="https://i.imgur.com/sOwMHxF.jpg" alt="alt text" title="image Title" />


- Displays average price/bedroom per area


2. Polscraper - WARNING: 4chan users use ***extremely*** offensive language which is searched for by this application


- Scrapes 4chan and stories threads/posts to JSON "reports"
<img src="https://i.imgur.com/ZmBMzRH.jpg" alt="alt text" title="image Title" />


- Scraper can be run once per click or set to run at intervals
<img src="https://i.imgur.com/xM850V6.jpg" alt="alt text" title="image Title" />


- Analyses/scans each report for offensive language and common topics
<img src="https://i.imgur.com/2lmDotW.jpg" alt="alt text" title="image Title" />


- Displays data from these reports in multiple formats (most frequent topics by nationality, time, etc)
<img src="https://i.imgur.com/rqp9XN2.jpg" alt="alt text" title="image Title" />

<img src="https://i.imgur.com/67vx7sZ.jpg" alt="alt text" title="image Title" />


4. News scraper
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
