# immo_eliza_scraping

# Project Description
In that mission your first task is to build a dataset gathering information about at least 10.000 properties all over Belgium. This dataset will be used later as a training set for your prediction model.

# Program description (workflow)
Overall:  This program scrapes information about properties for sale in Belgium from the www.immoweb.be website and saves it to a CSV file.

1. The program has three main functions namely find_links, get_all_urls and get_property
2. The find_links function function takes a page number as an argument and returns a list of links from that page of search results on the www.immoweb.be website that contain the value of link_to_find.

<screnshot that displays the executing or output of the find_link function>

3. The get_all_urls function calls the find_links function for each page number in the range from 0 (start) to 300 (end) and combines the results into a single list of URLs
<screnshot that displays the executing or output of the get_all_urls function>


4. The get_property function takes a URL as an argument and returns a Pandas DataFrame containing information about the property at that URL
<screnshot that displays the executing or output of the get_property function>

5. The resulting DataFrames are combined into a single DataFrame called properties_df, which is then saved to a CSV file called ‘immoweb_data.csv

<screnshot that displays the executing or output of the CSV file>

# Installation
Create a phython virtual environement
Install libraries ( Requests, BeautifulSoup, Chain, Pandas)


Run the files working_scraper.py or launch the program, all that is needed is to run the following command in the terminal:

```bash
python working_scraper.py
```

# Usage
Make price predictions on real estate sales in Belgium.

The first task is to build a dataset gathering information about at least 10.000 properties all over Belgium. 
subsequently use the dataset to build a model for price prediction.

# Visuals


# Contributors
Hariharan<br>
Mahmoud<br>
Marco<br>
Natalia

# Timeline
- Duration: `4 days`

# Personal situation
This program was developed to work with both dynamic and static website for data collection


