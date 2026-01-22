# Gaming Market Dashboard

### Project overview

This project analyses video game sales data to help people in the gaming industry decide which games to develop and where to sell them. Around 80% of games don't recover their costs, so effective data analysis is essential.

The dashboard uses sales data from over 22,000 games released between 2010 and 2019. It highlights trends in top-selling games, the best development platforms, and regional differences in game preferences.

### Business Problem

The gaming industry is worth over £200 billion worldwide, but it is also very risky. Most studios, especially small indie ones, lack the market insights that big publishers have. This means they often have to guess which games to make or which platforms to target.

This project helps close that gap by giving clear, data-driven answers to practical questions. For example, is the shooter genre too crowded? Should I focus on North America or Japan? Do higher critic scores actually lead to better sales?

### Target Audience

The dashboard is built for several groups of users:

Indie game developers who want to understand market opportunities before spending years on a project. They need straightforward answers on which genres and platforms offer the best chance of success.

Studio executives and producers who decide which projects to fund. They need regional sales data and trend analysis to help with their budgets.

Publishers are deciding which games to sign and how to split marketing budgets across regions.

Investors who want to understand the market before funding game development. The visualisations are easy for non-technical users to follow, but detailed enough for analysts.

### Dataset

I used the "Video Game Sales 2024" dataset for this project. The data were initially collected by ASANICZKA and are available on Kaggle. 

To keep things clear and accurate, I only looked at games released between 2010 and 2019. This made the data more reliable and reduced the dataset to 22,782 games. I excluded data from 2020 onward because it had gaps, likely due to the pandemic's disruption of reporting. 

All the data used is public commercial information and does not include any personal details.

### Methodology

Data Cleaning

Below are the steps I took to clean the data set:

1. I removed the image URL column as it was not needed for the data analysis.
2. Next, the release dates were converted to the correct datetime format.
3. The release year was extracted as a separate column for easier analysis.
4. Any missing values in sales columns were handled by treating them as zero (meaning no recorded sales in that region)
5. Games with missing critic scores were removed in order to collect data for accuracy purposes. 
6. A strategic decision was made to exclude all games released after 2019, as there were data quality concerns

I excluded data between 2020 and 2024 because there were unusual patterns due to the pandemic and the collected information was incomplete. I chose the period from 2010 to 2019 because it had reliable, consistent information. 

### Analysis Approach

I applied an exploratory data analysis, starting with the main question and investigating further as I progressed to answer the remaining business questions. The analysis was performed entirely on Jupyter notebooks, with the main analysis divided into two notebooks:

The first notebook handled data exploration and cleaning. The second notebook conducted the detailed statistical analysis and created the visualisations.

For the analysis, I used descriptive statistics like means, medians, and standard deviations, along with correlation analysis. I did not use complex models because the business questions required a clear view of what actually happened in the market, not predictions.

I used bar charts for comparisons, line charts for trends, bubble charts and scatter plots to show relationships between different variables. 

Key libraries used:

I used Pandas for all data manipulation and cleaning. I chose Pandas over alternatives because it handles CSV files well and is well known for its methods of grouping and aggregating data.

Matplotlib and Seaborn for creating static visualisations in the notebooks. I used Matplotlib for basic plots and Seaborn for more polished statistical visualisations with less code.

I used Plotly for the interactive dashboard visualisations. I initially tried using Matplotlib in the dashboard; however, I switched to Plotly because it provides better visualisations of the data.

I used Streamlit for building the web dashboard instead of Flask, as Streamlit is designed specifically for data applications.

This is an observational study that looks at historical sales data. I am not running experiments or trying to prove cause and effect. I am just finding patterns and correlations in the market data. The study is quantitative, using numerical sales figures and critical scores as the main data points. All analysis was conducted on aggregated sales data at the game level, without analysing individual consumer behavior.

Key Findings

The analysis revealed several important insights:

* Platform lifecycles are clear in the data. PS3 and Xbox 360 dominated in the early 2010s but began to decline quickly after 2013, when PS4 and Xbox One launched. 
* The Wii declined even faster. This shows that choosing the right platform and timing is crucial. Genre saturation varies widely by type. 
* Action and shooter games have thousands of releases but still sell well, suggesting that market size matters more than competition in these genres. 
* Smaller genres like music and party games have low saturation, which could be an opportunity for developers to target niche markets. 
* Japan prefers role-playing games, while North America and Europe favor shooters and sports games. This affects where to focus marketing and whether to localise games for certain markets. 
* Games with higher ratings often sell better but the connection isn't strong enough to predict success. Many high scoring games don't sell well and some low scoring games do. Quality matters but marketing and timing are also more important.

### How to Run the Dashboard

1. Install the required packages:

    pip install -r requirements.txt

2. Run the Streamlit dashboard:

    streamlit run app.py

3. The dashboard will open in your web browser as Localhost

For further information, check out Streamlit documentation at https://streamlit.io/

### Where AI Helped

AI helped me with code debugging. When I encountered file path or data type errors, I would paste the error message and ask claude to explain what was wrong and suggest fixes. This saved hours of searching through documentation.

Visualisation code. I knew what charts I wanted but not always the exact Matplotlib or Plotly syntax to create them. Claude provided code examples that I then adapted to my specific data and requirements.

### Where I Made My Own Decisions

The entire analytical approach was mine. Claude didn't suggest what questions to ask or what analyses to run. Those came from my understanding of the business problem and what would be useful to the target audience.

All data quality decisions were my own. The decision to exclude data from 2020 to 2024, how to handle missing values and which games to keep or remove were all my judgment calls based on what I saw in the data.

Dashboard design and user flow was entirely my design. I decided what visualisations to include, how to arrange them and what would make sense to someone using the tool.

### Impact on the Project

Using AI tools made it possible to finish the project on a tight schedule. Without them, I would have spent much more time fixing errors and reading documentation, leaving less time for analysis and insights. AI can help you implement your ideas faster but you still need to understand what you are doing and why. Every piece of code Claude generated, I had to read, understand and check to make sure it did what I wanted. This experience showed me that AI tools are very helpful for data analytics, but they are assistants, not replacements for real analytical thinking.

This project only uses publicly available commercial data. There is no personal information, no individual consumer data, and no data that could be traced back to specific people. The sales figures are aggregated industry data that companies like VGChartz compile from various public sources.

Under GDPR, this project does not process any personal data, so the main privacy regulations do not apply. The data subjects here are commercial products (games) and companies (publishers and developers), not individuals.

### Potential Biases in the Data

Several biases exist in this dataset that users should be aware of:

Selection bias: The dataset likely overrepresents successful games because VGChartz tracks games that actually sold enough copies to be worth tracking. Many tiny indie games that sold only a handful of copies won't appear here.

Regional bias: The "other sales" category lumps together everywhere outside North America, Japan, and Europe. This means markets like South America, Africa, and parts of Asia are underrepresented in the analysis.

Platform bias: Mobile gaming is almost entirely absent from this dataset because VGChartz focuses on console and PC gaming. The conclusions here don't apply to the mobile market, which is actually larger than console gaming.

Temporal bias: More recent years in the dataset tend to have more complete data than older years. This is why I focused on data between 2010 and 2019, rather than trying to analyse all the way back to the 1970s.


### Fairness and Representation

The analysis treats all genres and platforms equally in terms of methodology, but the business context means some categories get more attention simply because they represent larger markets. This could reinforce existing industry trends rather than highlighting opportunities in underrepresented areas.

The dashboard doesn’t make recommendations about what games to make, it only presents data. This is deliberate because context matters a lot in game development and what works for one studio might not work for another.

### Social Implications

There's a risk that data analysis like this could contribute to standardisation in the gaming industry. If everyone looks at the same data and concludes that shooters and action games sell best, we might see even more of those genres and fewer experimental or niche games.

I have addressed this by showing that there is opportunities in less crowded genres and by being open about the data's limits. The goal is to help people make decisions, not to tell them what to do.

### Data Limitations

Currently, there is missing critic scores: About 30% of games don't have critic scores, which limits some analyses. These are typically smaller releases that didn't get reviewed by major outlets.

Sales data accuracy: VGChartz estimates some of their numbers, so the figures are not exact. They are good enough for spotting trends but should not be seen as precise.

Incomplete recent data: This is why I excluded 2020-2024, but it means the analysis doesn't reflect the current market state, only the recent past.

The dataset includes digital sales but doesn't separate them from physical sales. Given the industry's shift to digital, this would have been valuable information.

### Alternative Approaches Considered

i could have built a machine learning model to predict whether a game would be successful based on its attributes. I chose not to because the available features like genre, platform, publisher etc, aren't enough to make meaningful predictions. Success in gaming depends heavily on factors that are not in the data, for example, marketing budgets, development quality and timing.

### Future Enhancements

If I were to continue developing this project, I would add more recent data, especially data after 2020, with a specific focus on understanding how the pandemic permanently changed gaming markets. I would include a digital versus physical sales breakdown as this would reveal important trends about distribution channels. 

I would separate indie games from AAA titles, as they operate on different markets. I would build predictive features that lets the users test scenarios like "what if I launch this type of game on this platform in this region?". I would add more granular regional data to break down the "other sales" category and properly represent emerging markets, which include mobile gaming data, to provide a complete picture of the gaming market rather than just console and PC.

### Credits

ASANICZKA. (2024). Video Game Sales 2024 [Data set]. Kaggle. https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024

Data Sources:

- VGChartz (https://www.vgchartz.com) - Video game sales tracking
- Metacritic (https://www.metacritic.com) - Review score aggregation

Industry Context:

- Newzoo Global Games Market Reports - Industry size and trends
- Entertainment Software Association (ESA) - Industry statistics and demographics

### Repo Information

This project is maintained on GitHub, with regular commits that show the development process. All code is original work created for this capstone project, with AI assistance documented where used.

The project is licensed for educational use and portfolio demonstration. The underlying dataset remains under Kaggle's terms of use.

---

Author: Mitesh Kumar

Project Type: Data Analytics Bootcamp Capstone

Completion Date: January 2026

Tools Used: Python, Pandas, Matplotlib, Seaborn, Plotly, Streamlit, Jupyter, Git

