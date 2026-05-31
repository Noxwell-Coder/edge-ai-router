# ⚡ Cascading Edge AI Router: LLM Infrastructure Cost Optimization

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Edge AI](https://img.shields.io/badge/Edge_AI-llama.cpp-green)
![Status](https://img.shields.io/badge/Status-MVP_Phase_1-orange)

## 🚨 The Problem: The Token Trap and Burned Budgets

The initial "honeymoon" phase of corporate AI adoption is over. The era of blindly hooking all internal workflows to top-tier cloud models (like GPT-4o or Claude 3.5 Sonnet) has led to an **explosive surge in API costs**.

Today, the industry faces three fundamental bottlenecks:
1. **Unsustainable Unit Economics:** Billing is strictly per-token. The more employees use AI for simple, repetitive tasks (formatting, basic syntax, search), the faster the server budget burns out.
2. **Compute Duplication:** Dozens of engineers ask the neural network the exact same basic questions, forcing the company to pay for generating identical responses repeatedly.
3. **Lack of Routing:** Using a massive, billion-parameter proprietary model to write a simple Regex expression is like using a microscope to hammer a nail.

## 💡 The Solution: Cost-Aware Cascading Architecture

The **Cascading Edge AI Router** is an intelligent request dispatcher that intercepts user prompts and dynamically routes them to the most cost-effective compute layer capable of solving the task.

This system reduces cloud API expenditures by **80-90%** by offloading the bulk of routine computational workloads to local company hardware (Edge Devices) and leveraging semantic caching.

## 🏗️ Pipeline Architecture (3-Tier Filtering)

The project implements a **"Cost-Aware AI"** paradigm through a three-level routing system:

### 🟢 Level 1: Semantic Cache ($0)
* **Technology:** Vector Database (SQLite / Redis + Embeddings).
* **Logic:** The algorithm searches for exact or semantically similar matches from previous queries (using Cosine Similarity).
* **Result:** Instant response with $O(1)$ search complexity. Zero cloud API calls.

### 🔵 Level 2: Local Micro-Model (Edge SLM) ($0)
* **Technology:** `llama.cpp` + 4-bit Quantized GGUF models (e.g., Gemma-2B / Qwen-1.5B).
* **Logic:** If it's a cache miss, the router evaluates the prompt's complexity. Simple tasks (coding assistance, text formatting) are routed to a local model running directly on the user's CPU (or Unified Memory on Apple Silicon).
* **Result:** Free generation utilizing the company's existing hardware infrastructure.

### 🔴 Level 3: Cloud LLM ($$$)
* **Technology:** API Gateway (Anthropic Claude / OpenAI).
* **Logic:** Only highly complex, resource-intensive tasks (deep R&D, architecture analysis, security audits) are routed to premium proprietary models.
* **Result:** Strategic token investment reserved exclusively for high-value tasks.

## 📊 Financial Dashboard (Cost Control UI)

The project features a built-in **Streamlit** interface styled as a modern chat client. A permanently visible Sidebar acts as a real-time financial analytics dashboard for C-level stakeholders:
* 💰 **Total Money Saved:** Tracks the budget retained by handling requests via Level 1 and Level 2.
* 💸 **Cloud Spending:** Monitors the active expenditure from Level 3 routing.
* 📈 **Efficiency Rate:** The percentage of total requests handled locally.

## 🚀 Quick Start

### 1. Clone & Setup Environment
```bash
git clone [https://github.com/yourusername/edge-ai-router.git](https://github.com/yourusername/edge-ai-router.git)
cd edge-ai-router

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
