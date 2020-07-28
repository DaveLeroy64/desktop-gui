DESKTOP GUI

For doing useful python things easily. Work in progress, much more to be added. So far mostly used for displaying data from web scrapers (news, property data, basic sentiment/topic analysis of unmoderated online communities).

TRIGGER WARNING: POLSCRAPER scans 4chan, a website that contains highly offensive language. This module contains offensive terms that the script searches for in order to build statistical data on the use of such language. The file that contains the various words the script looks for has been deliberately excluded from this repository. The script will not function without this file. I may add it to the repo later.

To do:

- General
    - Add multithreading so scrapers can run at same time as using the GUI
    - Polscraper and property scraper put in separate threads. Need to do news scraper
    - Somehow find out how to get cross-file function calls working without getting attribute error for local variables!!  

- News scraper
    - Make news scraper run at regular intervals. Home page display to display most recent stories in database for each outlet. 
    - Add button to enable/disable regular news scanning

- Property scraper
    - Add a popup to property scraper if there are more than 50 pages to confirm if you want to continue

- Polscraper
    - Boolean "apply weighting" tickbox to polscraper data to weigh down 'topics' that are ridiculously overused
    - B and C display options - add ability to display posts by country on table and as bar chart
    - Also add ability to show line plot of single country number of posts
    - Remove datagraph.clear() statements as default whenever graph is populated - only when button is hit. This way you can overlay different data maybe?
