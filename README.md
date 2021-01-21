Trading_Bot_HTN

Inspiration

Since the world went into lockdown, stock market has seen major ups and downs making it a very attractive investment opportunity. However, stock market requires a major time commitment which gave us the motivation to automate the process. It is rightly said that time is money and money is time. Our trading bot was made keeping in mind that it incorporates our strategy and earns profit while saving time.

Investing in stocks at an early age helps develop positive spending habit while ensuring financial stability. It also improves our ability to take risks as and when needed. However, history has shown us that people start taking major risks once their profits increase as they get carried away by emotions . Hence we made this bot which applies our strategy over real time data and keeps our potential risks in control by identifying potentially “good” stocks with stability to make the right investments.
What it does

Trading robots are programs that use mathematical algorithms in deciding whether to trade. From the market fluctuations, the trading robots are able to come up with signals that are translated to generate orders that make it easy to trade. Trading robots eliminate the psychological strains involved in the forex trade.

Our trading robot uses a quant trading algorithm in order to shortlist ideal stocks and trade using custom trigger point algorithms. It also has the capability of scraping minutely and daily data for a stock index and backtesting the strategies on any period of time.

How we built it

To make this project we divided it into 3 main parts. The first was to get the data which was done using a web scraper. The second part was the shortlist stocks that would be suitable for our algorithm, to do that we implemented 8 conditions(daily,weekly and monthly uptrend and stability of stocks) and tested them for accuracy. If the accuracy was above a certain percent we shortlisted it. Then we used the web scraper to get minutely data in the past month and tested out bot with it.

Lastly, a backtesting engine was created. A stock market simulator was created from scratch using the previously scraped daily and minutely data for each of the shortlisted stocks. Through this simulation, we demonstrated what the bot would look like in a live setting. We were able to see each of the individual transactions and trades the bot made, and it made steady profits throughout the month, proving it to be a success. Additionally, using this newfound transaction data, we prepared data frames and plots to analyze the financial performance and specifics.
Challenges we ran into

We faced a lot of challenges along the way. We initially struggled with making our own trading strategy. We also had a hard time keeping track of all the buy and sells because as our bot was trading at a very high frequency.
Accomplishments that we're proud of

We are extremely proud that our model was profitable and our strategy, stock filter, and back testing system worked.
What we learned

Through building this project, we gained a lot of financial knowledge, and refined our programming skills in the process. We learned about stock trading algorithms and financial analysis techniques, as well as experience handling large datasets, which were the price histories for each stock. With these large datasets, we performed various functions and analysis techniques, thus learning optimization techniques, data structures and algorithms as well. Finally, we learned how to scrape large datasets off of the internet and finding resources to do so.
Next steps for Incipere

Although we were able to link our model to an Alpaca paper trading account but were not able to run it. Since our bot trades in the long term, we were not able to test it live and showcase our work. Once that is done we would modify our strategy to diversify our trading portfolio and reduce the risk. By accumulating more and more data and making more trades, the bot will also get more credibility. Next, we will also work on making the strategies and triggers more customizable for users.
