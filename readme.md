DESKTOP GUI

For doing useful python things easily. Work in progress, much more to be added. So far mostly used for displaying data from web scrapers (news, property data, basic sentiment/topic analysis of unmoderated online communities).

TRIGGER WARNING: POLSCRAPER scans 4chan, a website that contains highly offensive language. This module contains offensive terms that the script searches for in order to build statistical data on the use of such language. The file that contains the various words the script looks for has been deliberately excluded from this repository. The script will not function without this file. I may add it to the repo later.

Current Features:
- Polscraper: Scrapes the board and stores all the threads/replies, with a data display that allows different data to be displayed/manipulated/compared in tables and graphs
- Property: Scrape different property websites for properties is user-defined areas, save to database, display data and price trends/averages in tables and graph
- News scraper: Collects headlines from different outlets and displays them. Can be set to run periodically (hourly updates)
- Multithreading: all scrapers run in separate threads to allow multitasking
- Downloads manager: automatically (or on button press) sorts downloads into categories/folders, and logs all moves made to a text file

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
