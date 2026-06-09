# 📊 Sales Intelligence Dashboard

Natural language analytics tool for e-commerce sales data.  
Ask questions in plain language — get data-driven insights instantly.

![Python](https://img.shields.io/badge/Python-3.8+-blue) 
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--nano-green)

---

## 🎯 Problem Statement

Business analysts need sales insights but don't always know SQL or Python.  
This tool bridges that gap — upload your CSV, ask in natural language, get answers.

---

## ✨ Features

- **Interactive Dashboard** — KPI cards, monthly trend, channel split, top products, city breakdown
- **CSV Upload** — plug in any sales CSV that follows the template
- **Natural Language Q&A** — powered by GPT API with structured context injection
- **Multi-domain ready** — works for fashion, electronics, F&B, or any retail data

---

## 🏗️ Architecture

```
CSV File
   ↓
pandas (aggregation + summary)
   ↓
Structured Context (text)
   ↓
GPT API (interpretation + recommendation)
   ↓
User
```

**Design decision:** LLM acts as the *interpretation layer*, not the *calculation layer*.  
All numerical aggregations are handled by pandas — ensuring accuracy.  
LLM only receives pre-computed summaries, not raw data.

---

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/sales-intelligence-dashboard.git
cd sales-intelligence-dashboard

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
cp .env.example .env
# Edit .env → fill in your OPENAI_API_KEY

# 5. Run
streamlit run app.py
```

---

## 📁 Project Structure

```
sales_dashboard/
├── app.py                        # Main Streamlit application
├── requirements.txt
├── .env.example                  # API key template
└── data/
    ├── sales_data.csv            # Sample: fashion e-commerce
    ├── sample_elektronik_2024.csv # Sample: electronics store
    ├── sample_fnb_2024.csv       # Sample: F&B / healthy food
    └── generate_data.py          # Script to regenerate sample data
```

---

## 📋 CSV Template

Your CSV must include these columns:

| Column | Description | Example |
|---|---|---|
| `order_id` | Unique transaction ID | ORD-10001 |
| `date` | Transaction date (YYYY-MM-DD) | 2024-01-15 |
| `product` | Product name | Sepatu Lari Nike |
| `category` | Product category | Footwear |
| `qty` | Units sold | 2 |
| `revenue` | Total transaction revenue (IDR) | 1700000 |
| `channel` | Sales channel | Tokopedia |
| `city` | Buyer city | Jakarta |
| `discount_pct` | Discount percentage (0–100) | 10 |
| `rating` | Product rating (1.0–5.0) | 4.5 |

> Download the template directly from the app sidebar.

---

## ⚠️ Known Limitations

- Data is synthetic — not validated against real business scenarios
- LLM may give inaccurate answers for multi-dimensional queries  
  (e.g. channel × month × product combinations not in pre-computed context)
- No authentication — not production-ready as-is
- Context is re-sent on every query — not optimized for large datasets
- Chat history resets on page refresh

---

## 🔮 Roadmap

| Version | Feature |
|---|---|
| v1.0 | Static context, CSV upload, NL Q&A ✅ |
| v2.0 | Dynamic context — LLM generates pandas queries on demand |
| v3.0 | Agentic mode — function calling, multi-step reasoning |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Data:** pandas, Plotly
- **AI:** OpenAI API (gpt-4.1-nano)
- **Config:** python-dotenv

---

## 👤 Author

**Erlangga Nursyahbani**  
Informatics Engineering · Machine Learning Path  
[LinkedIn](https://linkedin.com/in/YOUR_USERNAME) · [GitHub](https://github.com/YOUR_USERNAME)
