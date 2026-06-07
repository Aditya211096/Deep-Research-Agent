# Deep Research Agent (DRA)

> **Autonomous Macro-Corporate Intelligence & Policy Forensics Engine**

Deep Research Agent (DRA) is a state-of-the-art agentic framework designed to perform deep, qualitative, and quantitative research on complex corporate entities, industry sectors, policy structures, and regulatory filings. Built with an agent-first architecture, it bypasses traditional reactive text generation to orchestrate real-time web harvesters, document parsing engines, specialized virtual analyst panels, and a self-healing database builder to generate fully interactive, publication-ready research slide decks.

---

## 🌟 Key Capabilities

*   **Real-Time Real Harvester:** Expanded web crawling and index traversal via Tavily AI, retrieving high-fidelity intelligence and stripping away HTML noise.
*   **Direct Memory PDF Parsing:** Direct loading of remote PDFs (e.g. SEBI DRHPs, corporate postal ballots) into memory buffers utilizing PyMuPDF (`fitz`), bypasses local disk I/O bottlenecks.
*   **8-Agent Virtual Debate Panel:** Orchestrates a panel of 8 specialized virtual analysts (Growth Case, Unit Economics, Macro/Sovereign, Global Precedents, Labor Rights, Legal/Compliance, Operations, and Ecology) to dissect target corpora from conflicting angles.
*   **Self-Healing JSON Database Builder:** Validates generated report structures in Python and automatically executes targeted healers to generate missing fields (benchmarks, policy, sovereign, socioeconomic) when omitted.
*   **Automated Deep-Dive Pipeline:** Integrates a unified research pipeline that compiles the main report, caches a research backlog, and programmatically executes a deep-dive investigation into the highest-impact backlog anomaly in one command.
*   **Deterministic Model Auditing:** Builds advanced quantitative models including:
    *   *Beneish M-Score* (Earnings Manipulation Screen)
    *   *Sloan Ratio* (Cash Flow vs. Accrual Integrity Screen)
    *   *DuPont 5-Factor ROE* (ROE Profitability Driver Decomposition)
    *   *Kelly Criterion & EVT Tail Risk* (Investment Sizing and Extreme Market Risk Models)
    *   *Bass Diffusion & Power Law Alpha* (Adoption Velocity and Moat/Consolidation Indices)
    *   *Fermi TAM Check* (Sanity checks reported TAM against physical limits)

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** and **Node.js** (optional, for slide deck verification) installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/Deep-Research-Agent.git
cd Deep-Research-Agent
```

### 3. Install Dependencies
Install the required packages from PyPI:
```bash
pip install google-genai tavily-python pymupdf requests beautifulsoup4 pyyaml
```

---

## 🔑 Obtaining API Keys

The Deep Research Agent requires two API keys to execute its research loop:

### 1. Google Gemini API Key (underlying LLM)
Used to power the 8-agent virtual panels, the moderator synthesis agent, and the self-healing loops.
1. Visit **[Google AI Studio](https://aistudio.google.com/)**.
2. Sign in with your Google account.
3. Click the **"Create API Key"** button.
4. Copy the generated key.

### 2. Tavily API Key (web intelligence layer)
Used to perform real-time search queries and smart site crawls without getting blocked by bot-protection firewalls.
1. Go to **[Tavily AI](https://tavily.com/)**.
2. Sign up for a free developer account.
3. Copy your API key from the developer dashboard.

---

## 🚀 Execution Guide

### 1. Set Environment Variables

You must export your API keys to your shell session before running the orchestrator:

#### Windows (PowerShell)
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
$env:TAVILY_API_KEY="your_tavily_api_key_here"
```

#### Linux / macOS (Bash/Zsh)
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export TAVILY_API_KEY="your_tavily_api_key_here"
```

### 2. Run the Unified Research Command
Execute the orchestrator with your research query:
```bash
python forensics_orchestrator.py "Deconstruct the business model of Zepto's quick commerce dark store network in India, analyzing unit economics, store rent, labor costs, growth vs. burn, and comparing it against Blinkit."
```

This single command will:
1. Parse the target entity and run focused regulatory and context searches on Google indices.
2. Smart crawl top-priority files and PDFs, compressing their contents to fit token budgets.
3. Spawn the 8 virtual analyst subagents to debate findings.
4. Compile the slide deck database and trigger the healer to verify data integrity.
5. Automatically run the Deep-Dive merging step to add paged backlog details (generating a full 11-slide deck).

---

## 📊 Viewing the Slide Deck

Once compilation completes, the agent compiles a dedicated, self-contained dashboard folder under the `dashboard/` directory.

1. Navigate to the generated directory:
   ```bash
   cd dashboard/zepto_business_model/
   ```
2. Open **`index.html`** directly in any web browser (simply double-click it or open it via the `file://` protocol).
3. Use the **Left/Right Arrow Keys** or click the **Prev/Next Buttons** to navigate the premium dark-mode slide deck.
4. Click **"Share Summary"** to compile a social-ready markdown summary with custom headline choices.
