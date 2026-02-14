import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Import Ingestion & Retrieval modules
from src.Ingestion.yahoo_finance import fetch_stock_data
from src.Retriever.retriever import retrieve
from src.Retriever.generator import generate_answer

# Import Vector Store modules
from src.Embedding.vector_store import load_faiss_index, create_faiss_index 
from src.Embedding.embedder import create_embeddings

# -----------------------------
# Enhanced Financial Report
# -----------------------------
def display_financial_report(df, ticker, years):
    # Ensure numeric columns only
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    latest_close = float(df['Close'].iloc[-1])
    first_close = float(df['Close'].iloc[0])

    total_return = ((latest_close - first_close) / first_close) * 100
    cagr = ((latest_close / first_close) ** (1 / years) - 1) * 100

    highest_price = float(df['High'].max())
    lowest_price = float(df['Low'].min())
    avg_volume = float(df['Volume'].mean())

    daily_returns = df['Close'].pct_change()
    volatility = float(daily_returns.std() * np.sqrt(252) * 100)

    rolling_max = df['Close'].cummax()
    drawdown = (df['Close'] - rolling_max) / rolling_max
    max_drawdown = float(drawdown.min() * 100)

    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    latest_ma50 = float(df["MA50"].iloc[-1])
    latest_ma200 = float(df["MA200"].iloc[-1])
    
    # Handle NaN in MAs if history is short
    latest_ma50 = latest_ma50 if not np.isnan(latest_ma50) else 0.0
    latest_ma200 = latest_ma200 if not np.isnan(latest_ma200) else 0.0

    trend = "Bullish (Golden Cross Structure)" if latest_ma50 > latest_ma200 else "Bearish (Death Cross Structure)"
    performance_status = "Positive Growth" if total_return > 0 else "Negative Performance"

    st.markdown("## 📑 Financial Performance Report")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest Close", f"${latest_close:,.2f}")
    col2.metric("Total Return", f"{total_return:,.2f}%")
    col3.metric("Volatility", f"{volatility:,.2f}%")
    col4.metric("Max Drawdown", f"{max_drawdown:,.2f}%")

    st.markdown("---")

    st.markdown("### 📊 Executive Overview")

    st.markdown(f"""
    Over the last **{years} year(s)**, **{ticker}** generated a cumulative return of **{total_return:,.2f}%**, 
    with a compounded annual growth rate (CAGR) of **{cagr:,.2f}%**, reflecting **{performance_status}**.

    During this period, the stock traded between **${lowest_price:,.2f}** and **${highest_price:,.2f}**, 
    demonstrating measurable price variability.

    Average daily trading volume stood at **{avg_volume:,.0f} shares**, 
    indicating consistent market participation.
    """)

    st.markdown("### ⚠ Risk & Stability Assessment")

    st.markdown(f"""
    The stock exhibited an annualized volatility of **{volatility:,.2f}%**, 
    over the selected **{years}-year period**.

    The maximum drawdown observed was **{max_drawdown:,.2f}%**, 
    representing the largest peak-to-trough correction

    These metrics suggest the stock 
    {'carries elevated risk characteristics' if volatility > 40 else 'maintains moderate risk exposure'}.
    """)

    st.markdown("### 📈 Technical Trend Analysis")

    st.markdown(f"""
    The 50-day moving average is **${latest_ma50:,.2f}**, 
    while the 200-day moving average is **${latest_ma200:,.2f}**.

    This indicates a **{trend}**, 
    widely interpreted as a momentum signal.

    Investors 
    {'may maintain constructive positioning' if total_return > 0 else 'are adopting defensive positioning'}.
    """)

    st.markdown("### 🔮 Forward-Looking Commentary")

    if total_return > 15 and volatility < 35:
        outlook = "constructive with balanced return generation and manageable risk"
    elif total_return > 0:
        outlook = "moderately positive, though volatility should be monitored"
    else:
        outlook = "cautious given negative performance"

    st.markdown(f"""
    Based on historical indicators over the past **{years} year(s)**, 
    the outlook appears **{outlook}**.

    Future performance will depend on earnings, macroeconomic trends, 
    and broader market sentiment.
    """)

    st.markdown("---")


# ==========================================
# UI CONFIGURATION
# ==========================================

st.set_page_config(page_title="Financial RAG", page_icon="📈", layout="wide")

col1, col2 = st.columns([1, 6])
with col1:
    # Ensure this image path exists or use a placeholder
    st.image("images/logo.jpg", use_container_width=True) 
     # Placeholder icon

with col2:
    st.title("Financial RAG - Stock Intelligence")
    st.caption("AI-powered Retrieval Augmented Generation for Stock Analysis")

st.markdown("---")

if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = None
if "last_built_config" not in st.session_state:
    st.session_state.last_built_config = None

with st.form("stock_form"):
    stock_input = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TCS.NS):")

    years = st.selectbox(
        "Select Analysis Period (Years)",
        [1, 2, 3, 4, 5],
        index=0
    )

    submitted = st.form_submit_button("Analyze Stock")

if submitted and stock_input:
    st.session_state.selected_stock = stock_input.upper()

# ------------------------------------------
# MAIN LOGIC BLOCK
# ------------------------------------------
if st.session_state.selected_stock:

    ticker = st.session_state.selected_stock
    st.success(f"Loaded: {ticker} ✅")

    # Fetch Data
    df = fetch_stock_data(ticker, years)

    if df is not None and not df.empty:

        st.subheader("Market Overview")

        # ✅ Ensure index is datetime
        df.index = pd.to_datetime(df.index)

        # ✅ Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # ✅ Ensure numeric columns
        required_cols = ["Open", "High", "Low", "Close", "Volume"]

        for col in required_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # ✅ Drop NaN rows
        df = df.dropna(subset=["Open", "High", "Low", "Close"])

        # ✅ Create Candlestick chart safely
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=ticker
        ))

        fig.update_layout(
            title=f"{ticker} Price Chart ({years} Year Analysis)",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500,
            xaxis_rangeslider_visible=False,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Financial Report
        display_financial_report(df, ticker, years)

        # --------------------------------------------------------
        # INTELLIGENT PIPELINE MANAGEMENT (Fixes Slowness)
        # --------------------------------------------------------
        # We check if we already built the index for THIS stock & YEAR config
        current_config = f"{ticker}_{years}"
        
        if st.session_state.last_built_config != current_config:
            
            with st.status("Building AI Knowledge Base... (One Time)", expanded=True) as status:
                st.write("Aggregating financial data...")
                
                chunks = []
                
                # --- 1. Master Summary ---
                master_summary = (
                    f"STOCK SUMMARY FOR {ticker}\n"
                    f"Period: {years} Years\n"
                    f"Range: {df.index.min().date()} to {df.index.max().date()}\n"
                    f"All Time High: {df['High'].max():.2f}\n"
                    f"All Time Low: {df['Low'].min():.2f}\n"
                )
                chunks.append(master_summary)

                # --- 2. Monthly Grouping WITH Daily Details (Fixes Invisible Dates) ---
                monthly_groups = df.resample('M')
                
                for period, data in monthly_groups:
                    if data.empty: continue
                    
                    month_name = period.strftime('%B %Y') 
                    
                    # Create mini-list of all dates: "2023-03-01: Close 150.00 | ..."
                    daily_records = [
                        f"{date.strftime('%Y-%m-%d')}: Close {row['Close']:.2f}" 
                        for date, row in data.iterrows()
                    ]
                    daily_text = " | ".join(daily_records)
                    
                    chunk_text = (
                        f"### MONTHLY DATA: {month_name}\n"
                        f"Summary: High {data['High'].max():.2f}, Low {data['Low'].min():.2f}\n"
                        f"Daily Prices: {daily_text}\n"
                    )
                    chunks.append(chunk_text)

                st.write(f"Generated {len(chunks)} optimized knowledge blocks.")
                
                st.write("Generating embeddings...")
                embeddings = create_embeddings(chunks)
                
                st.write("Updating Vector Store...")
                create_faiss_index(embeddings, chunks, force_rebuild=True)
                
                # Mark this config as "Built" so we don't rebuild on next question
                st.session_state.last_built_config = current_config
                status.update(label="AI Knowledge Base Ready!", state="complete", expanded=False)

        # --------------------------------------------------------
        # Q&A INTERFACE
        # --------------------------------------------------------
        st.markdown("---")
        st.subheader("💬 Ask AI About This Stock")

        with st.form("question_form"):
            query = st.text_input("Type your question (e.g., 'What was the price on March 15, 2023?'):")
            ask = st.form_submit_button("Ask AI")

        if ask and query:
            with st.spinner("Analyzing market data..."):
                # Retrieval is now fast because index is already built
                results = retrieve(query) 
                answer = generate_answer(query, results)

            st.markdown("### 📌 AI Answer")
            st.info(answer)

            with st.expander("🔍 Retrieved Data Context"):
                for r in results:
                    st.write(r)

    else:
        st.error("No data available for this ticker.")