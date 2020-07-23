DESKTOP GUI

For doing useful python things easily. Work in progress, much more to be added. So far mostly used for displaying data from web scrapers (news, property data, basic sentiment/topic analysis of unmoderated online communities).

TRIGGER WARNING: POLSCRAPER scans 4chan, a website that contains highly offensive language. This module contains offensive terms that the script searches for in order to build statistical data on the use of such language. The file that contains the various words the script looks for has been deliberately excluded from this repository. The script will not function without this file. I may add it to the repo later.

To do:

- Add multithreading so scrapers can run at same time as using the GUI
    - Polscraper and property scraper put in separate threads. Need to do news scraper
- Add a popup to property scraper if there are more than 50 pages to confirm if you want to continue
- Add threads/replies as lists in polscraper file so that it can return the actual number of threads/replies it scans. Or just make them an integer and with each iteration of the for loop it adds 1 to it.
- ALSO just realised that the label in polscraper data display covers the "clear data" button and that's why I can't click it. Change the geometry of the label

- Somehow find out how to get cross-file function calls working without getting attribute error for local variables!!