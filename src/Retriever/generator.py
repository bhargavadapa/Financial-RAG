#GENERATOR.PY
import os
from groq import Groq
from dotenv import load_dotenv
from src.Utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query, context_chunks):
    """
    Sends retrieved stock data to Groq and generates professional financial responses.
    """
    context_text = "\n\n".join(context_chunks)
    
    # Check if the query is for a full report to adjust the tone
    is_report = "comprehensive financial report" in query.lower()
    
    system_prompt = (
        "You are a Senior Financial Analyst. Use the provided Market Data Context "
        "(which includes daily prices and a DATASET SUMMARY) to answer questions.\n\n"
    )
    
    if is_report:
        system_prompt += (
            "You are an Equity Research Analyst at a top-tier investment bank. "
            "Your goal is to provide a 'Professional Equity Research Report' based on the provided data.\n\n"
            "Format the report with the following EXACT sections:\n"
            "1. INVESTMENT SUMMARY : A high-level 'Executive Summary' of the stock's performance.\n"
            "2. TECHNICAL PERFORMANCE : Analyze the 1-year price trajectory, 52-week High/Low, and momentum.\n"
            "3. VOLATILITY & RISK PROFILE : Discuss standard deviation (if apparent), volume spikes, and potential downside risks.\n"
            "4. QUANTITATIVE INSIGHTS : Discuss the Average Price, growth/decline percentages, and volume trends.\n"
            "5. ANALYST OUTLOOK: A 12-month outlook based on historical price action (Bull vs Bear cases).\n\n"
            "Use professional Markdown formatting, tables where appropriate, and bold key financial terms."
            "You are an Equity Research Analyst. Provide a 'Professional Equity Research Report'.\n\n"
            "STRICT FORMATTING RULES:\n"
            "6. DO NOT use asterisks (**) or any markdown bolding symbols.\n"
            "7. Use UPPERCASE plain text for headers.\n"
            "8. Use a line of dashes (------) under each header for structure.\n"
            "9. Use the following sections: INVESTMENT SUMMARY, TECHNICAL PERFORMANCE, "
            "VOLATILITY & RISK PROFILE, and ANALYST OUTLOOK.\n"
            "10. Keep the numbers precise and the tone formal."
        )
    else:
        system_prompt += "You are a professional financial assistant. Be precise, concise, and factual."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": f"Market Data Context:\n{context_text}\n\nQuestion: {query}"
                }
            ],
            temperature=0.1  # Low temperature for factual consistency
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq Generation Error: {e}")
        return "I encountered an error. Please verify your API key and connection."