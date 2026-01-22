import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page config
st.set_page_config(
    page_title="Gaming Market Dashboard",
    page_icon="🎮",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/clean/vg_data_cleaned.csv')
    # Filter for reliable 2010-2019 data
    df_reliable = df[df['release_year'].between(2010, 2019)].copy()
    return df_reliable

df = load_data()

# Sidebar navigation
st.sidebar.title("🎮 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Platform Analysis", "Genre Intelligence", "Regional Trends", "Market Insights"]
)

# Chart styling
def style_chart():
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette('husl')

# Overview Page 
if page == "Overview":
    st.title("🎮 Gaming Market Overview (2010-2019)")
    st.markdown("""
    This dashboard looks at the video game market from 2010 to 2019. It focuses on PS3, PS4, XBox 360, XBox One era. 
    The data is designed to help developers, publishers and investors make better choices about witch platforms to target, 
    which genre to focus on and how to plan for different regions.
    """)
    
  
  # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Games", f"{len(df):,}")
    
    with col2:
        st.metric("Total Sales", f"{df['total_sales'].sum():.0f}M units")
    
    with col3:
        st.metric("Average Sales", f"{df['total_sales'].mean():.2f}M units")
    
    with col4:
        st.metric("Median Sales", f"{df['total_sales'].median():.2f}M units")
    
    st.markdown("---")

# Quick insights
    st.subheader("Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Market Reality**")
        st.write(f"The gap between average ({df['total_sales'].mean():.2f}M) and median ({df['total_sales'].median():.2f}M) sales tells us that most games sell poorly, while a few blockbusters make up the majority of revenue.")
        
        st.markdown("**Top Platform**")
        top_platform = df.groupby('console')['total_sales'].sum().idxmax()
        top_sales = df.groupby('console')['total_sales'].sum().max()
        st.write(f"{top_platform} dominated with {top_sales:.0f}M units sold.")
    
    with col2:
        st.markdown("**Biggest Genre**")
        top_genre = df.groupby('genre')['total_sales'].sum().idxmax()
        genre_sales = df.groupby('genre')['total_sales'].sum().max()
        st.write(f"{top_genre} games led with {genre_sales:.0f}M units sold.")
        
        st.markdown("**Largest Market**")
        na_share = (df['na_sales'].sum() / df['total_sales'].sum()) * 100
        st.write(f"North America accounts for {na_share:.0f}% of global sales, making it the primary market to target.")


# Platform Analysis Page
elif page == "Platform Analysis":
    st.title("Platform Performance Analysis")
    
    # Platform market share
    st.subheader("Platform Market Share (2010-2019)")
    
    platform_sales = df.groupby('console')['total_sales'].sum().sort_values(ascending=False).head(10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar chart
    style_chart()
    ax1.barh(range(len(platform_sales)), platform_sales.values)
    ax1.set_yticks(range(len(platform_sales)))
    ax1.set_yticklabels(platform_sales.index)
    ax1.set_xlabel('Total Sales (millions)')
    ax1.set_title('Top 10 Platforms by Sales')
    ax1.invert_yaxis()
    
    # Pie chart for top 5
    top5 = platform_sales.head(5)
    others = platform_sales[5:].sum()
    pie_data = pd.concat([top5, pd.Series({'Others': others})])
    
    ax2.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Market Share - Top 5 Platforms')
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    PlayStation consoles dominated the market, with PS3 alone capturing 22.8% of total sales. 
    Xbox consoles performed strongly in North America but had less global reach.
    """)

    
    # Year-over-year platform trends
    st.subheader("Platform Lifecycle Trends")
    
    yearly_platform = df.groupby(['release_year', 'console'])['total_sales'].sum().reset_index()
    top_platforms = df.groupby('console')['total_sales'].sum().nlargest(6).index
    yearly_top = yearly_platform[yearly_platform['console'].isin(top_platforms)]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    style_chart()
    
    for platform in top_platforms:
        data = yearly_top[yearly_top['console'] == platform]
        ax.plot(data['release_year'], data['total_sales'], marker='o', label=platform, linewidth=2)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Sales (millions)')
    ax.set_title('Platform Sales Over Time (2010-2019)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    The chart shows an average console's generation lifecycle. The PS3 and Xbox 360 were most popular around 2010 and 2011, 
    but their popularity dropped when the PS4 and Xbox One came out in 2013 and 2014. 
    This six to seven-year cycle matters when planning development schedules.
    """)

    # Platform game count vs sales
    st.subheader("Platform Efficiency: Games Released vs Total Sales")
    
    platform_stats = df.groupby('console').agg({
        'title': 'count',
        'total_sales': 'sum'
    }).rename(columns={'title': 'game_count'})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart()
    
    ax.scatter(platform_stats['game_count'], platform_stats['total_sales'], s=100, alpha=0.6)
    
    for idx, row in platform_stats.iterrows():
        ax.annotate(idx, (row['game_count'], row['total_sales']), 
                   xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax.set_xlabel('Number of Games Released')
    ax.set_ylabel('Total Sales (millions)')
    ax.set_title('Platform Efficiency Analysis')
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    Platforms in the upper left (high sales with fewer games) are more efficient markets. 
    This matters for developers with limited resources who need to choose where to invest.
    """)

    # GENRE INTELLIGENCE PAGE
elif page == "Genre Intelligence":
    st.title("Genre Market Intelligence")
    
    # Top genres by sales
    st.subheader("Genre Performance")
    
    genre_sales = df.groupby('genre')['total_sales'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        style_chart()
        
        ax.barh(range(len(genre_sales)), genre_sales.values)
        ax.set_yticks(range(len(genre_sales)))
        ax.set_yticklabels(genre_sales.index)
        ax.set_xlabel('Total Sales (millions)')
        ax.set_title('Total Sales by Genre (2010-2019)')
        ax.invert_yaxis()
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("**Top 3 Genres**")
        for i, (genre, sales) in enumerate(genre_sales.head(3).items(), 1):
            market_share = (sales / genre_sales.sum()) * 100
            st.write(f"{i}. **{genre}**")
            st.write(f"   {sales:.0f}M units ({market_share:.1f}%)")
        
        st.markdown("**Combined Impact**")
        top3_share = (genre_sales.head(3).sum() / genre_sales.sum()) * 100
        st.write(f"The top 3 genres account for {top3_share:.0f}% of all sales.")

        # Genre saturation analysis
    st.subheader("Market Saturation: Opportunity vs Competition")
    
    genre_stats = df.groupby('genre').agg({
        'title': 'count',
        'total_sales': 'sum'
    }).rename(columns={'title': 'game_count'})
    
    fig, ax = plt.subplots(figsize=(12, 6))
    style_chart()
    
    scatter = ax.scatter(genre_stats['game_count'], genre_stats['total_sales'], 
                        s=150, alpha=0.6, c=range(len(genre_stats)), cmap='viridis')
    
    for idx, row in genre_stats.iterrows():
        ax.annotate(idx, (row['game_count'], row['total_sales']), 
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    ax.set_xlabel('Number of Games Released')
    ax.set_ylabel('Total Sales (millions)')
    ax.set_title('Genre Saturation Analysis')
    ax.grid(True, alpha=0.3)

    # Add quadrant lines
    median_games = genre_stats['game_count'].median()
    median_sales = genre_stats['total_sales'].median()
    ax.axvline(median_games, color='red', linestyle='--', alpha=0.3)
    ax.axhline(median_sales, color='red', linestyle='--', alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    what this charts shows:\n
    • Top-left = High opportunity (few games, high sales)\n
    • Top-right = Competitive (many games, high sales)\n
    • Bottom-right = Oversaturated (many games, low sales)\n
    • Bottom-left = Niche (few games, low sales)\n
    """)

    # Average sales per game by genre
    st.subheader("Average Sales Performance by Genre")
    
    avg_sales = df.groupby('genre')['total_sales'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    style_chart()
    
    ax.barh(range(len(avg_sales)), avg_sales.values)
    ax.set_yticks(range(len(avg_sales)))
    ax.set_yticklabels(avg_sales.index)
    ax.set_xlabel('Average Sales per Game (millions)')
    ax.set_title('Which Genres Perform Best on Average?')
    ax.invert_yaxis()
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    This shows which genres that perform generally better per release. Genres with high average 
    sales but lower total counts might represent quality over quantity markets.
    """)

    # REGIONAL TRENDS PAGE
elif page == "Regional Trends":
    st.title("Regional Market Analysis")
    
    # Regional market share
    st.subheader("Global Market Distribution")
    
    regional_sales = {
        'North America': df['na_sales'].sum(),
        'Europe': df['pal_sales'].sum(),
        'Japan': df['jp_sales'].sum(),
        'Other': df['other_sales'].sum()
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 8))
        style_chart()
        
        colors = sns.color_palette('husl', len(regional_sales))
        ax.pie(regional_sales.values(), labels=regional_sales.keys(), autopct='%1.1f%%', 
               startangle=90, colors=colors)
        ax.set_title('Regional Market Share')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("**Regional Breakdown**")
        total = sum(regional_sales.values())
        for region, sales in sorted(regional_sales.items(), key=lambda x: x[1], reverse=True):
            percentage = (sales / total) * 100
            st.write(f"**{region}**: {sales:.0f}M units ({percentage:.1f}%)")
        
        st.markdown("---")
        st.write("""
        North America is the dominant market, accounting for nearly half of all sales. 
        Any global strategy must succeed in NA to be commercially viable.
        """)
    
    # Top genres by region
    st.subheader("Genre Preferences Vary by Region")
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    style_chart()
    
    regions = [
        ('na_sales', 'North America'),
        ('pal_sales', 'Europe'),
        ('jp_sales', 'Japan')
    ]
    
    for i, (col, name) in enumerate(regions):
        top_genres = df.groupby('genre')[col].sum().sort_values(ascending=False).head(5)
        
        axes[i].barh(range(5), top_genres.values)
        axes[i].set_yticks(range(5))
        axes[i].set_yticklabels(top_genres.index)
        axes[i].set_xlabel('Sales (millions)')
        axes[i].set_title(name)
        axes[i].invert_yaxis()
    
    plt.suptitle('Top 5 Genres by Region', y=1.02, fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    **Key regional differences:**
    - **Japan**: Strong preference for RPGs and unique game styles
    - **North America & Europe**: Action and Shooter games dominate
    - **Strategic implication**: A game that works in one region may not translate to others
    """)
    
    # Regional sales trends over time
    st.subheader("Regional Sales Trends (2010-2019)")
    
    yearly_regional = df.groupby('release_year').agg({
        'na_sales': 'sum',
        'pal_sales': 'sum',
        'jp_sales': 'sum',
        'other_sales': 'sum'
    })
    
    fig, ax = plt.subplots(figsize=(12, 6))
    style_chart()
    
    ax.plot(yearly_regional.index, yearly_regional['na_sales'], marker='o', label='North America', linewidth=2)
    ax.plot(yearly_regional.index, yearly_regional['pal_sales'], marker='s', label='Europe', linewidth=2)
    ax.plot(yearly_regional.index, yearly_regional['jp_sales'], marker='^', label='Japan', linewidth=2)
    ax.plot(yearly_regional.index, yearly_regional['other_sales'], marker='d', label='Other', linewidth=2)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Sales (millions)')
    ax.set_title('How Regional Markets Changed Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    st.write("""
    All regions show similar patterns, peaking in the early 2010s before declining. The consistent 
    proportions suggest global trends affect all markets, but the magnitude differences remain significant.
    """)

# MARKET INSIGHTS PAGE
elif page == "Market Insights":
    st.title("Market Intelligence & Insights")
    
    # Quality vs Sales
    st.subheader("Does Quality Matter? Critic Scores vs Sales")
    
    # Filter games with scores
    df_scored = df[df['critic_score'].notna()].copy()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create score bins
        df_scored['score_bin'] = pd.cut(df_scored['critic_score'], 
                                        bins=[0, 5, 6, 7, 8, 9, 10],
                                        labels=['0-5', '5-6', '6-7', '7-8', '8-9', '9-10'])
        
        avg_by_score = df_scored.groupby('score_bin', observed=True)['total_sales'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        style_chart()
        
        ax.bar(range(len(avg_by_score)), avg_by_score.values)
        ax.set_xticks(range(len(avg_by_score)))
        ax.set_xticklabels(avg_by_score.index)
        ax.set_xlabel('Critic Score Range')
        ax.set_ylabel('Average Sales (millions)')
        ax.set_title('Higher Scores = Higher Sales')
        ax.grid(True, alpha=0.3, axis='y')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        scored_pct = (len(df_scored) / len(df)) * 100
        st.metric("Games with Scores", f"{len(df_scored):,}")
        st.metric("% of Total", f"{scored_pct:.1f}%")
        
        st.write("""
        **The reality**: Only 11% of games have critic scores. 
        
        Quality matters, but mostly for games that get reviewed. 
        Many indie and smaller games never get scored, so marketing 
        and visibility matter just as much as quality.
        """)
    
    # Publisher analysis
    st.subheader("Top Publishers by Market Share")
    
    publisher_sales = df.groupby('publisher')['total_sales'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    style_chart()
    
    ax.barh(range(len(publisher_sales)), publisher_sales.values)
    ax.set_yticks(range(len(publisher_sales)))
    ax.set_yticklabels(publisher_sales.index)
    ax.set_xlabel('Total Sales (millions)')
    ax.set_title('Top 10 Publishers (2010-2019)')
    ax.invert_yaxis()
    
    st.pyplot(fig)
    plt.close()
    
    top10_share = (publisher_sales.sum() / df['total_sales'].sum()) * 100
    st.write(f"""
    The top 10 publishers control {top10_share:.1f}% of the market. This concentration shows 
    the challenge indie developers face in gaining market share.
    """)
    
    # Release timing
    st.subheader("When Do Games Launch? Release Patterns")
    
    yearly_releases = df.groupby('release_year').size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    style_chart()
    
    ax.bar(yearly_releases.index, yearly_releases.values)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Games Released')
    ax.set_title('Game Releases Over Time')
    ax.grid(True, alpha=0.3, axis='y')
    
    st.pyplot(fig)
    plt.close()
    
    peak_year = yearly_releases.idxmax()
    peak_count = yearly_releases.max()
    st.write(f"""
    Releases peaked in {int(peak_year)} with {peak_count:,} games. The decline in later years 
    reflects both market maturation and the approaching end of the console generation.
    """)

# Key takeaways
    st.subheader("Strategic Recommendations")
    
    st.markdown("""

These are the key points from the 2010-2019 market analysis for informed decisions.



**For Developers:**

1. Focus on North America first as it makes up 49% of the market.

2. Action, Shooter, and Sports games are popular, but competition in these genres is high.

3. Quality matters, but getting reviews is more important. Invest in marketing and PR.

4. Consider regional preferences. RPGs are popular in Japan, while Action games are favored in North America and Europe.



**For Publishers & Investors:**

1. PlayStation platforms have the best global performance.

2. Most games have low sales, so diversify your portfolio.

3. Timing matters. Remember the 6-7 year console cycle.

4. The top 10 publishers control more than half the market, making competition tough.



**Market Opportunities:**

1. Look for genres with high average sales and fewer games available (top-left quadrant).

2. Consider games that attract players from different regions to boost revenue. Games with scores of 8 or higher sell three to four times better than average.



**Data Quality:**

This analysis covers 2010 to 2019, when the data was checked. Reliability with incomplete data was excluded to keep the analysis accurate.
""")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source**: VGChartz 2024")
st.sidebar.markdown("**Analysis Period**: 2010-2019")
st.sidebar.markdown(f"**Total Games**: {len(df):,}")