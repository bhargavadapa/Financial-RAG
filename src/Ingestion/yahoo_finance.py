#YAHOO_FINANCE.PY
import datetime
import yfinance as yf
import pandas as pd
from src.Utils.config import RAW_DATA_DIR
from src.Utils.logger import get_logger

logger = get_logger(__name__)


def get_ticker_from_name(query):
    """
    Convert company name into valid Yahoo ticker.
    """
    try:
        search = yf.Search(query, max_results=1)
        if search.quotes:
            ticker = search.quotes[0]['symbol']
            logger.info(f"Search for '{query}' found ticker: {ticker}")
            return ticker
        return query.strip().upper()
    except Exception as e:
        logger.error(f"Search error for {query}: {e}")
        return query.strip().upper()


def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    news_docs = []

    for item in news[:5]:
        doc = f"News Headline: {item['title']} - Link: {item['link']}"
        news_docs.append(doc)

    return news_docs


import datetime
import yfinance as yf
import pandas as pd
from src.Utils.config import RAW_DATA_DIR
from src.Utils.logger import get_logger

logger = get_logger(__name__)

def fetch_stock_data(user_input, years=1):

    ticker_symbol = user_input.strip().upper()

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * years)

    try:
        df = yf.download(
            ticker_symbol,
            start=start_date,
            end=end_date,
            interval="1d",
            progress=False
        )

        if df is None or df.empty:
            return None

        # 🔥 CRITICAL FIX: Flatten columns if multi-index
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Ensure proper datetime index
        df.index = pd.to_datetime(df.index)

        df = df.sort_index()
        df = df.dropna()

        print("Columns:", df.columns)
        print("Date Range:", df.index.min(), "to", df.index.max())

        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        file_path = RAW_DATA_DIR / f"{ticker_symbol}.csv"
        df.to_csv(file_path)

        return df

    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None
