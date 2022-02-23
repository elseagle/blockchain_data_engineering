# Platform Scraping

<!-- MarkdownTOC -->

- [Platform Scraping](#platform-scraping)
    - [It allows you to do the following:](#it-allows-you-to-do-the-following)
- [Overview](#overview)
  - [Built With](#built-with)
- [Objectives](#objectives)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
  - [Get started for coingecko](#get-started-for-coingecko)
  - [Get started for rarity.tools](#get-started-for-raritytools)
- [Reasons for choosing Websites, toolkits and storage](#reasons-for-choosing-websites-toolkits-and-storage)


<!-- /MarkdownTOC -->


### It allows you to do the following:

- [x] Scrape coingecko for cryptocurrencies based on market cap rank and rarity.tools for Upcoming NFT sales.

- [x] Extract and save data to a postgresql database.

- [x] Functions that automate downloading for different topics/search queries.

- [x] Save extracted data to a csv file.




# Overview

This project scrapes both [coingecko](https://www.coingecko.com/) and [rarity.tools](https://rarity.tools/upcoming/) using different tools/methods based on how each website returns data to the web browser. 


## Built With

- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)



# Objectives

- To get real time information about cryptocurrencies listed on [coingecko](https://www.coingecko.com/) and to be able to update the information in the database.

    `For example:`
    <details>
    <summary></summary>

     ```json
        {
            "check_date": "2022-02-20",
            "time_of_check": "12:39:06",
            "currency_name": "Solana",
            "coin_gecko_url": "https://www.coingecko.com/en/coins/solana",
            "currency_website": "https://solana.com/",
            "currency_categories": ["Solana Ecosystem", "Smart Contract Platform"],
            "currency_price": "$89.77",
            "market_cap": "$28,798,066,069",
            "trading_volume": "$897,127,430",
            "market_cap_rank": "#8",
            "all_time_high": "$259.96",
            "all_time_low": "$0.500801",
            "one_day_low": "$86.20",
            "one_day_high": "$92.04",
            "seven_day_low": "$86.43",
            "seven_day_high": "$104.84",
        }
    ```

    </details>


- To search for cryptocurrencies on [coingecko](https://www.coingecko.com/) based on the category or currency name.

- To get the latest information on upcoming nft sales from [rarity.tools](https://rarity.tools/upcoming/).

    `For example:`

    <details>
    <summary></summary>

     ```json
        {
            "id": "animalgangproject",
            "Project": "Animal Gang Project",
            "Image Count": 4,
            "Short Description": "Animal gangs themed NFTs",
            "Max Items": "9999",
            "Price": "0.49",
            "Currency": "SOL",
            "Sale Date": "2022-03-14T17:00:00.000Z",
            "Website": "https://animalgangproject.com",
            "Discord": "https://discord.gg/m7caFHfW",
            "TwitterId": "AnimalGangGame",
            "Listed Date": "2022-02-10T00:00:00.000Z"
        }
    ```

    </details>


# Prerequisites

1. Python 3.8 ++

2. Clone this repository.

3. Setup virtual environment. Visit [here](https://docs.python.org/3/library/venv.html) for a detailed guide on how to setup virtualenv.

4. Install the project requirements:
    ```sh
    $ pip3 install -r requirements.txt
    ```

5. Set up postgres database locally for postgresql installation instructions please visit [here](https://www.postgresqltutorial.com/postgresql-getting-started/). For online database, it can be set up on [aws](https://aws.amazon.com/),  [heroku](https://dashboard.heroku.com/) or any other alternative.

6. Set up `.env` file, all the necessary environment variables can be found in `.env.example`. It is necessary to note the following during env setup:

    * SET DB_HOST, DB_PASSWORD, DB_USER, DB_NAME and DB_PORT to the appropriate details gotten from the previous step.


    * SET PROXY_URL to http proxy gotten from servies such as [geosurf](https://www.geosurf.com/) or [brightdata](https://brightdata.com/). This sub-step is not necessary but it is useful because it helps to prevent your IP getting blocked, This happens when a single IP makes multiple requests to the same site in a very short period of time. A protected website might interpret this as a DDOS attack and blacklist the IP address. Using a proxy server helps to avoid this.


    * Set PROJECT_DIRECTORY to the path that the project folder is saved in. e.g /Users/Desktop/blockchain_data_engineering


# Quickstart

## Get started for coingecko

1. Open a terminal and navigate to the directory of the cloned repository.

2. Create the necessary tables and initialize the database with the top 130 cryptocurrencies based on market rank.

    ```sh
        $ python3 scraper/coingecko/create_table/upload_initial_data.py
     ```

3. Search for a random category and it's coins and also search for a random coin. Upload the information to the database and csv file.

    ```sh
        $ python3 scraper/coingecko/search/upload_new_data.py
     ```

## Get started for rarity.tools

1. Open a terminal and navigate to the directory of the cloned repository.

2. Create the table and initialize the database with upcoming nft sales data.

    ```sh
        $ python3 scraper/rarity_tools/create_table/upload_initial_data.py
     ```

3. Update the database with new upcoming nft sales.

    ```sh
        $ python3 scraper/rarity_tools/upload_new_data.py
     ```


# Reasons for choosing Websites, toolkits and storage

- Coingecko was chosen because it is a leading website for gettng up to date information on crypto currency related data. 

- rarity.tools was chosen because it has up to date information on unlisted nfts that are yet to be sold.  

- For scraping coingecko it uses regular python requests along with beautiful soup because upon inspecting the web browser it was found that coingecko uses server side rendering and all the information is returned as an html response. The category urls and urls for each cryptocurrency is gotten by inspecting the html source. 

- Asyncio with aiohttp is being used to make multiple requests asynchronously to the url of each of the cryptocurrencies e.g. https://www.coingecko.com/en/coins/bitcoin. so as to get the extra information not listed on the homepage.

- For scraping rarity.tools it uses requests to get the json response because after inspecting the network panel in dev tools, the request that the web browser makes to rarity.tools api is mimicked via the scripts in this project. Since this is faster and more structured since it mimicks the actual requests and responses that lists the nfts on the platform. 
  
- Postgresql was chosen because it helps developers build applications, administrators to protect data integrity and also helps data analyst and data scientist to manage their data irregardless of the size of the dataset.


