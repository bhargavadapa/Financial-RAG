#CSV_TO_DOCS.PY
import pandas as pd

def csv_to_documents(csv_path):
    df = pd.read_csv(csv_path)

    # Ensure correct types
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df.dropna(subset=['Close', 'Date'])
    df = df.sort_values('Date')

    # ------------------------
    # CORE CALCULATIONS
    # ------------------------
    mean_price = df['Close'].mean()
    median_price = df['Close'].median()
    std_dev = df['Close'].std()
    high_price = df['Close'].max()
    low_price = df['Close'].min()

    # Moving Averages
    ma_50 = df['Close'].rolling(window=min(50, len(df))).mean().iloc[-1]
    ma_200 = df['Close'].rolling(window=min(200, len(df))).mean().iloc[-1]

    # ------------------------
    # DATE RANGE CALCULATION
    # ------------------------
    start_date = df['Date'].min().date()
    end_date = df['Date'].max().date()
    total_days = len(df)

    years_covered = (df['Date'].max() - df['Date'].min()).days / 365

    # ------------------------
    # PROFESSIONAL SUMMARY BLOCK
    # ------------------------
    summary_text = (
        "PROFESSIONAL FINANCIAL DATA REPORT\n"
        "----------------------------------\n"
        f"Data Coverage:\n"
        f"- Start Date: {start_date}\n"
        f"- End Date: {end_date}\n"
        f"- Total Trading Days: {total_days}\n"
        f"- Years Covered: {years_covered:.2f} Years\n\n"

        "Statistical Analysis:\n"
        f"- Mean Stock Price: {mean_price:.2f}\n"
        f"- Median Stock Price: {median_price:.2f}\n"
        f"- Standard Deviation: {std_dev:.2f}\n"
        f"- Highest Price Observed: {high_price:.2f}\n"
        f"- Lowest Price Observed: {low_price:.2f}\n\n"

        "Trend Indicators:\n"
        f"- 50-Day Moving Average: {ma_50:.2f}\n"
        f"- 200-Day Moving Average: {ma_200:.2f}\n"
    )

    documents = [summary_text]

    # Add daily rows as context
    for _, row in df.iterrows():
        documents.append(
            f"Date: {row['Date'].date()}, Close Price: {row['Close']:.2f}"
        )

    return documents
