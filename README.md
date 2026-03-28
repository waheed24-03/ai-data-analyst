

  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=AI%20Data%20Analyst%20Agent&fontSize=80&animation=fadeIn&fontAlignY=38&desc=GenAI%20•%20Automated%20Insights%20•%20Local%20Inference&descAlignY=55&descAlign=50" alt="AI Data Analyst Header" />

  <br />

  <p>
    <img src="https://img.shields.io/badge/LangChain-Integration-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" />
    <img src="https://img.shields.io/badge/Streamlit-UI_Framework-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
    <img src="https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge" alt="ChromaDB" />
  </p>

  <h3>🤖 Your Personal Data Scientist, Powered by LLMs</h3>
  
  <p align="center">
    <i>"A conversational intelligence platform that allows you to chat with your dataset, generate visualizations on the fly, and export professional reports."</i>
  </p>
</div>

---

## 🏗️ System Architecture

The system follows a robust **modular design**, ensuring maintainability and scalability for real-world data tasks.

<div align="center">
  <img src="images/architecture_diagram.png" alt="System Architecture" width="800" style="border-radius: 10px; border: 1px solid #ddd;" />
</div>

<br />

| Module | Functionality |
| :--- | :--- |
| **Streamlit App** | Interactive UI for upload, chat, and visualization. |
| **LLM Engine** | **LangChain + Ollama** translates natural language into Python analysis code. |
| **Executor** | Safely executes generated code on the dataframe. |
| **Knowledge Layer** | **RAG (ChromaDB)** + Web Search fallback for context-aware answers. |
| **Persistence** | Manages Chat history, schema caching, and session memory. |

---

## 🚀 Why This Project?

Data analysis is often manual, repetitive, and requires coding skills. This **AI Agent** bridges the gap by combining **Local LLMs and Python** into a single workflow.

* **Privacy First:** Runs locally using Ollama (no data leaves your machine).
* **Not a Toy:** Handles CSVs up to **100MB**, includes error handling, and structured logging.
* **End-to-End:** From raw data upload to a downloadable PDF report.

---

## ✨ Key Features

- 📂 **Smart Ingestion**: Upload large CSV files (up to 100MB) with auto-schema detection.
- 💬 **Natural Language Querying**: Ask "What is the sales trend?" and get a coded answer.
- 📊 **Auto-Visualization**: Generates Matplotlib/Seaborn charts automatically based on queries.
- 📝 **RAG-Powered Insights**: Uses Vector Search to find semantic context within text columns.
- 💾 **Professional Exports**: Download analysis as **CSV**, **Plots**, or **PDF Reports**.
- ⚡ **Performance**: Implements **Caching** for repeated queries and persistent chat memory.
- 🔎 **Web Aware**: Fallback to Web Search if the dataset lacks specific context.

---

## 🖼️ Visual Walkthrough

<div align="center">
  <table>
    <tr>
      <td align="center"><b>1️⃣ Upload Dataset</b></td>
      <td align="center"><b>2️⃣ Chat with Data</b></td>
    </tr>
    <tr>
      <td><img src="images/image1.png" width="400" /></td>
      <td><img src="images/image2.png" width="400" /></td>
    </tr>
    <tr>
      <td align="center"><b>3️⃣ Automated Analysis</b></td>
      <td align="center"><b>4️⃣ Visualizations</b></td>
    </tr>
    <tr>
      <td><img src="images/image3.png" width="400" /></td>
      <td><img src="images/image4.png" width="400" /></td>
    </tr>
    <tr>
      <td align="center"><b>5️⃣ Graph Generation</b></td>
      <td align="center"><b>6️⃣ Profiling Report</b></td>
    </tr>
    <tr>
      <td><img src="images/image5.png" width="400" /></td>
      <td><img src="images/image7.png" width="400" /></td>
    </tr>
     <tr>
      <td align="center"><b>7️⃣ Report Export</b></td>
      <td align="center"><b>8️⃣ Summary</b></td>
    </tr>
    <tr>
      <td><img src="images/image8.png" width="400" /></td>
      <td><img src="images/image9.png" width="400" /></td>
    </tr>
  </table>
</div>

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/-Streamlit-black?style=flat-square&logo=streamlit) | User Interface |
| **Orchestration** | ![LangChain](https://img.shields.io/badge/-LangChain-black?style=flat-square&logo=langchain) | LLM Chains & Agents |
| **Inference** | ![Ollama](https://img.shields.io/badge/-Ollama-black?style=flat-square&logo=ollama) | Local LLM Runner |
| **Data Ops** | ![Pandas](https://img.shields.io/badge/-Pandas-black?style=flat-square&logo=pandas) | Data Manipulation |
| **Vector Store** | ![ChromaDB](https://img.shields.io/badge/-ChromaDB-black?style=flat-square) | RAG / Semantic Search |
| **Reporting** | `PDFKit`, `wkhtmltopdf` | PDF Generation |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/Syed-Waheed/ai-data-analyst-agent.git](https://github.com/Syed-Waheed/ai-data-analyst-agent.git)
cd ai-data-analyst-agent

# 2. Create a virtual environment (Recommended)
conda create -n analyst_env python=3.10 -y
conda activate analyst_env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Ensure Ollama is running locally
ollama serve

# 5. Run the Application
streamlit run app.py

```
## 👤 Author

<div align="left">
  <img src="https://github.com/Syed-Waheed.png" width="100" align="left" style="margin-right: 20px; border-radius: 50%;" alt="Syed Abdul Waheed" />

  <strong>Syed Abdul Waheed</strong><br/>
  <em>Data Science Enthusiast | Python Developer | Automation Explorer</em>

  Focused on building concepts rather than memorizing syntax. Actively working on strengthening practical implementation skills in AI & ML.

  <br /><br />

  <a href="https://www.linkedin.com/in/syed-abdul-waheed/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn" />
  </a>

  <a href="https://github.com/Syed-Waheed">
    <img src="https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github" alt="GitHub" />
  </a>
</div>

<br clear="left"/>

---
