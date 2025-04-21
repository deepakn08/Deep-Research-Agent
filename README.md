# 🧠 Deep Research AI Agent

This project is an interactive research assistant powered by LangGraph and autonomous agents. It allows users to input a query, after which the system crawls the web, extracts relevant information, and drafts an AI-generated answer — all using a dual-agent setup.

---

## 🔍 Methodology

The core idea is built on **LangGraph**, which enables agentic workflows using a graph of nodes (agents). Here's the process:

### 🔗 Agentic System Architecture:

1. **Query Input**  
   The user enters a question.

2. **Web Crawling Agent (Node 1)**  
   - Uses the **Tavily API** to perform a deep web search.
   - From Each URL we extract the content in it.
   - A list of document snippets is returned as `docs`.

3. **Answer Drafting Agent (Node 2)**  
   - Uses an **LLM (LLaMA-3 via Groq)** to draft an answer.
   - The LLM is prompted with the user query and the crawled content.

4. **Graph Execution**  
   - The graph is built using `langgraph`, with nodes for crawling and drafting.
   - Upon query submission, the state flows through the graph and the final response is shown.
---

## 🧰 Major Libraries Used

| Library              | Purpose |
|----------------------|---------|
| **LangGraph**        | Agentic workflows using graph-based state machines. |
| **LangChain**        | Prompt templates and message types for LLM interaction. |
| **Tavily API**       | Real-time web search and content fetching. |
| **Groq + LLaMA-3**   | High-speed LLM inference for answer generation. |

---

## 🚀 Getting Started

### 1. Install Requirements
```bash
pip install -r requirements.txt

```
---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Deep-Research-Agent.git
```
### 2. Run the file
```bash
python agents.py
```
