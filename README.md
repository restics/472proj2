# CSE472 Project 2 Type 1
> Rui Heng Foo (1226940821) and Michael Liu ()

## OS environment :computer:
OS env for

OS env for Foo
- Windows 10 / Powershell Major 5 Minor 1 Build 19041 Revision 5129
- Python 3.12.5
- pip 24.3.1

## Command lines :bookmark_tabs:
Prerequisites: current path of the directory is `...\472proj2`

1. Enter `pip install -r requirements.txt` to the command line of your terminal to install necessary python packages via pip.
2. Run both `python Alpha_Vantage_stocks_crawler.py` and `python prawscraper.py` in part1\
3. Run `python sentiment_analysis.py` in part2\
4. Run only `python processdatasets.py` in part3\
5. Run `python backtesting_program.py` in part4\



Further instructions are listed in the report.

## Directory Structure :deciduous_tree:
```
|   README.md
|   requirements.txt
|   
+---.idea
|   |   .gitignore
|   |   472proj2.iml
|   |   csv-editor.xml
|   |   discord.xml
|   |   misc.xml
|   |   modules.xml
|   |   vcs.xml
|   |   
|   \---inspectionProfiles
|           profiles_settings.xml
|           
+---part1
|   |   .env
|   |   Alpha_Vantage_stocks_crawler.py
|   |   Alpha_Vantage_stocks_crawler.py.bak
|   |   decade_daily_NVDA_prices.csv
|   |   prawscraper.py
|   |   year_daily_NVDA_prices.csv
|   |   
|   \---out
|           rdaytrading_nvda.csv
|           rinvesting_NVDA.csv
|           rstocks_NVDA.csv
|           rwallstreetbets_NVDA.csv
|           
+---part2
|   |   sentiment_analysis.py
|   |   sentiment_analysis.py.bak
|   |   
|   \---out
|           combined_sentiment_results.csv
|           daily_sentiment_score.csv
|           
+---part3
|   |   .env
|   |   brokerbot.py
|   |   brokerbot.py.bak
|   |   processdatasets.py
|   |   processdatasets.py.bak
|   |   
|   +---out
|   |       combined_sentiment_results.csv
|   |       
|   \---__pycache__
|           brokerbot.cpython-312.pyc
|           
\---part4
        backtesting_program.py
        backtesting_program.py.bak
```            





