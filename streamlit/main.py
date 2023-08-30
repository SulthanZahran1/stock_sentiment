import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import datetime
import praw
stock_symbol = None
# Initialize the Reddit client with your credentials
reddit = praw.Reddit(
    client_id="VP-UReniosV25DXYPAzLfA",
    client_secret="_1mc1-QvcuZKx50TzUPmhaNy0At8LQ",
    user_agent="u/bottori stock"
)

def get_latest_stock_mentions(stock_symbol, subreddit_name="stocks", limit=5):
    """
    Get the latest posts mentioning the stock_symbol from the specified subreddit.

    Args:
    - stock_symbol (str): The stock symbol to search for (e.g., "AAPL").
    - subreddit_name (str): The subreddit to search within.
    - limit (int): The maximum number of posts to return.

    Returns:
    - list: Pairs (title, url) of the latest posts mentioning the stock symbol. Empty list if no posts found.
    """
    mentions = []
    
    # Search the subreddit for the stock_symbol
    posts = reddit.subreddit(subreddit_name).search(stock_symbol, limit=limit)

    for post in posts:
        if stock_symbol in post.title or stock_symbol in post.selftext:
            mentions.append((post.title, post.url))
    
    return mentions


# Placeholder usage in Streamlit:

def graph_column():
    global stock_symbol
    stock_symbol = st.text_input("Enter Stock Symbol:", value='AAPL').upper()
    stock_data = yf.Ticker(stock_symbol)
    now = datetime.datetime.now()
    month_back = datetime.timedelta(days=30)
    start_date = st.date_input("Start Date", now-month_back)
    end_date = st.date_input("End Date", now)
    df = stock_data.history(start=start_date, end=end_date)


    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'])])
    fig.update_layout(title=f'{stock_symbol} Stock Data',
                    xaxis_title='Date',
                    yaxis_title='Price (in USD)',
                    xaxis_rangeslider_visible=False)  # Disable the default rangeslider

    # Display graph in Streamlit
    st.plotly_chart(fig)

col1, col2 = st.columns(2)
with col1:
    st.header("Stock Data")
    graph_column()
with col2:
    st.header("Reddit Mentions")
    latest_mentions = get_latest_stock_mentions(stock_symbol)
    if latest_mentions:
    # Construct a markdown string with tighter spacing
        markdown_string = ""
        for title, url in latest_mentions:
            title_escaped = title.replace('$', '\$')
            link = f"[{title_escaped}]({url})"
            st.write(link, unsafe_allow_html=True)  # display each link
    else:
        st.write(f"No recent mentions of {stock_symbol} found in r/stocks.")
    

    # Display sentiment analysis
