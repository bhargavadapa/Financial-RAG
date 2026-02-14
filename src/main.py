#MAIN.PY
import streamlit as st
from src.main import build_pipeline
from src.Retriever.retriever import retrieve
from src.Retriever.generator import generate_answer
from src.Embedding.vector_store import load_faiss_index

st.set_page_config(page_title="Financial RAG", layout="wide")
st.title("📈 Financial RAG - Stock Intelligence")

if "stock_loaded" not in st.session_state:
    st.session_state.stock_loaded = False
    st.session_state.selected_stock = None

# -----------------------------
# Step 1: Select Stock
# -----------------------------
stock_input = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TCS.NS):")

if st.button("Load Stock Data") and stock_input:
    with st.spinner("Building RAG pipeline..."):
        build_pipeline(stock_input.upper())
        st.session_state.stock_loaded = True
        st.session_state.selected_stock = stock_input.upper()

# -----------------------------
# Step 2: Ask Questions
# -----------------------------
if st.session_state.stock_loaded:

    st.success(f"{st.session_state.selected_stock} Loaded Successfully ✅")

    query = st.text_input(
        f"Ask questions about {st.session_state.selected_stock}:"
    )

    if st.button("Get Answer") and query:
        with st.spinner("Retrieving relevant data..."):
            index, chunks = load_faiss_index()
            results = retrieve(query)
            answer = generate_answer(query, results)

        st.subheader("Answer:")
        st.write(answer)

        with st.expander("Retrieved Context"):
            for r in results:
                st.write(r)
