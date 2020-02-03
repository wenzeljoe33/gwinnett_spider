# gwinnett_spider
This is a scrapy-spider that extracts tax data from the gwinnett county tax assessor website using an excel spreadsheet with a list of parcel ids as input. In this current version, the parcel id must be in the first row of the excel spreadsheet and must be in the Gwinnett county parcel id format.

Navigate the terminal to the gwinnett_2 directory and run the command:

scrapy crawl properties

A prompt will request a excel file for input. Select the file. Note the excel file should have the Parcel Id in the B column.

