Architecting an Autonomous Agentic Research Prototype: A Step-by-Step Implementation Guide for the Google Antigravity Ecosystem
The Paradigm Shift Toward Agent-First Development
The software engineering landscape is currently undergoing a fundamental transition, moving away from reactive, autocomplete-based coding assistants and toward proactive, autonomous agentic platforms. For a developer aiming to rapidly prototype a system that highlights deep technical strength despite lacking a formal background in data analytics, leveraging an agent-first framework provides an immediate structural advantage. Google Antigravity represents the vanguard of this shift, designed from the ground up as a native platform for agentic development. Unlike legacy tools that merely predict the next line of code, Antigravity presupposes that artificial intelligence is an autonomous actor capable of planning, executing, validating, and iterating on complex engineering tasks with minimal human intervention.

The platform operates primarily through a "Mission Control" or Agent Manager interface. This dashboard acts as a high-level orchestration layer, enabling the developer to act as a systems architect who spawns, monitors, and interacts with multiple agents operating asynchronously across different workspaces. Rather than scrolling through raw tool execution logs, delegating work in Antigravity generates tangible "Artifacts"—such as implementation plans, task lists, code diffs, and validation walkthroughs—allowing for rapid verification and course correction via document-style feedback. For an individual targeting a strict June 7th delivery deadline, building a prototype using the Google Antigravity Python SDK, augmented by specialized web intelligence and document parsing libraries, offers the most direct path to demonstrating advanced engineering capabilities.

Strategic Prototype Definition: Autonomous Financial Forensics
To demonstrate "Highly In-Depth Research capabilities" without relying on traditional data science or statistical modeling expertise, the prototype must target a complex, qualitative research domain where AI agents naturally excel: document forensic analysis and web-based sentiment synthesis. A compelling application of this technology involves mirroring the analytical workflows of independent financial analysts and IPO researchers, such as Jayant Mundra, who manually decode dense financial filings to uncover hidden corporate maneuvers.

The objective of this prototype will be to architect an "Autonomous IPO and Financial Forensics Agent." This agent will be programmed to ingest massive, hundreds-of-pages-long Draft Red Herring Prospectuses (DRHPs), cross-reference claims against live web data, and highlight operational risks, related-party transactions, and predatory equity structures that standard retail investors routinely miss.

For example, independent analysis of the PhysicsWallah IPO DRHP revealed that while the company pitched an explosive growth story, it was simultaneously undergoing a massive and costly structural pivot from an online-first brand to a hybrid offline model, with significant internal control failures flagged by auditors and a high dependence on paid marketing for offline growth. Similarly, forensic analysis of OYO's corporate actions exposed a highly unethical "Bonus CCPS" postal ballot—a 50-page document wrapped in legal jargon offering a worthless default option of one bonus share per 6,000 owned, while hiding a highly lucrative 1,109-per-6,000 ratio behind a complex "Annexure B" form requiring submission within an impossibly short three-day window.

By programming an Antigravity agent to autonomously parse dense PDFs for these exact types of deceptive structures—and simultaneously crawling the web to gauge the ecosystem health of the entities involved—the resulting prototype will stand as a formidable demonstration of technical strength. The developer acts not as a data analyst, but as a systems architect who constructs the AI pipeline capable of performing the analysis.

Architectural Foundations of the Google Antigravity SDK
To prototype a highly capable agent, one must bypass standard graphical interfaces and utilize the Google Antigravity SDK. Launched as a Python library, the SDK provides programmatic access to Google's premier Antigravity coding agent, allowing developers to build on top of a secure, scalable, and stateful infrastructure layer. The SDK is designed to be agent-friendly, utilizing clean Python types based on Pydantic V2 models, natively supporting structured outputs, and maintaining clear naming conventions so that AI agents can read, write, and maintain the SDK code fluently.

Crucially, the SDK abstracts the complex machinery of the agentic loop—including state management, backend communication, and tool execution—freeing the developer to focus entirely on the agent's unique behavioral logic. The architecture is divided into three distinct operational layers.

SDK Layer

Designation

Key Classes

Core Purpose

Layer 1

Simplified API

Agent

Provides a high-level, batteries-included asynchronous context manager. It manages binary discovery, tool wiring, hook registration, and safety policy defaults automatically, exposing a simple agent.chat() method for interaction.

Layer 2

Session State

Conversation, ChatResponse, Step, ToolCall, HookRunner

Wraps the transport connection to add stateful session management. It accumulates step history, manages context compaction tracking, and monitors real-time token usage metrics dynamically.

Layer 3

Adapter

Connection, ConnectionStrategy, LocalConnection

The lowest infrastructural level, handling transport protocols. For local deployments, it uses WebSockets to communicate directly with a Go-based local harness via protobuf messages serialized to JSON.

Environment Provisioning and Sandbox Persistence
Every autonomous interaction orchestrated by the Antigravity SDK can provision a secure, Google-hosted Linux sandbox where the agent's iterative tool-use loop begins. Inside this isolated sandbox, the agent can execute Bash scripts, run Python code, and utilize Node.js commands natively. When defining the environment configuration for the prototype, the developer has three distinct architectural choices. Passing the string "remote" provisions a completely fresh sandbox with default settings, ideal for stateless tasks. Passing a specific identifier, such as "env_abc123", reuses an existing environment, preserving all internal files, previously downloaded datasets, and operational state across multi-turn sessions. Finally, providing a full EnvironmentConfig dictionary allows the developer to configure custom code sources such as Git repositories, dictate specific networking rules, and establish hard resource limits.

A critical element of this architecture for deep research purposes is the platform's automatic context compaction. To support long-running research tasks—such as an agent reading through a massive corporate DRHP without hitting the LLM token limits—the Antigravity agent automatically triggers context compaction at approximately 135,000 tokens, preserving the core operational context while freeing window space for continued processing.

Phase 1: Infrastructure Initialization and Dependency Resolution
The foundation of the prototype requires strict adherence to initialization protocols, as the architecture relies heavily on specific package distribution methods. The Google Antigravity SDK relies on a compiled runtime binary that is exclusively packaged within platform-specific wheels published to PyPI. Attempting to clone the GitHub repository directly is insufficient and will lead to critical failure; the compiled Go-based binary will be missing, and the LocalConnection harness will fail to instantiate.

The initialization protocol dictates the execution of specific shell commands to establish the primary environment, alongside the necessary auxiliary libraries required for deep research capabilities. The system utilizes the tavily-python package for intelligent web traversal, and the pymupdf (also known as fitz) library for high-performance PDF extraction.

# Core SDK Installation via PyPI to ensure binary inclusion
pip install google-antigravity

# Deep Research Dependency Resolution
pip install tavily-python pymupdf requests beautifulsoup4

Following the installation phase, environmental variables must be securely exported to authenticate both the core agent harness and the auxiliary research APIs. The system strictly requires a GEMINI_API_KEY to authenticate the underlying Antigravity agent models (typically Gemini 3.5 Flash), and a TAVILY_API_KEY to access the web intelligence layer.

Phase 2: Engineering the Web Intelligence Protocol
An agent's utility is entirely bounded by its available toolset. To fulfill the requirement of "Highly In-Depth Research," the standard built-in google_search tool provided by the SDK must be augmented with a programmatic execution layer capable of deep web traversal. General-purpose search APIs often return unstructured noise, HTML boilerplate, and advertisement data that rapidly pollutes an agent's context window. For autonomous workflows, optimized context retrieval is paramount.

The Tavily Python SDK serves this exact purpose, allowing the agent to execute real-time web searches, extract specific URL content, and perform smart website crawls, returning cleanly parsed data explicitly formatted for LLM ingestion. To integrate this into the Antigravity architecture, the developer must wrap the Tavily functionalities into distinct, strongly-typed Python functions. The Antigravity ToolRunner automatically inspects these type hints and docstrings via reflection to generate JSON schemas that the agent understands.

from tavily import TavilyClient
import os

# Instantiate the asynchronous or synchronous client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def deep_web_search(query: str, search_depth: str = "advanced") -> dict:
   """
   Executes a comprehensive web search to gather up-to-date market intelligence.
   Provides sources, answers, and context required for in-depth IPO analysis.
   """
   response = tavily_client.search(query=query, search_depth=search_depth)
   return response

def smart_site_crawl(url: str, instructions: str) -> dict:
   """
   Performs a smart crawl starting at a given URL.
   It navigates subpages to extract content matching the specific instructions provided.
   """
   response = tavily_client.crawl(url, instructions=instructions)
   return response

The crawl() method is particularly potent for the financial forensics use case. Instead of the agent writing a custom Python web scraper that may fail on modern single-page applications or encounter bot-protection walls, the agent simply provides a root URL and natural language instructions. For example, if the agent is researching the PhysicsWallah IPO, it can instruct the Tavily crawler to navigate NDTV Profit's domain with the instruction: "Find all pages discussing PhysicsWallah's operational risks, hybrid offline business model costs, and M&A failures". This returns highly condensed, relevant intelligence directly into the agent's reasoning loop.

Phase 3: Implementing the Document Parsing Engine
Researching corporate entities invariably entails parsing dense PDF documents, legal filings, and financial prospectuses. PyMuPDF is an exceptionally high-performance Python library engineered for data extraction and manipulation of PDF documents. Because the Antigravity agent operates within ephemeral, isolated sandboxes, writing downloaded PDFs to the local disk introduces unnecessary I/O latency and potential permission conflicts. The optimal architectural pattern utilizes the Python io.BytesIO stream buffer to load document bytes directly into memory.

import fitz  # PyMuPDF
import requests
import io

def extract_text_from_remote_pdf(pdf_url: str) -> str:
   """
   Downloads a PDF document from a provided URL entirely in-memory and extracts all textual content.
   Essential for parsing DRHPs, legal ballots, and corporate whitepapers.
   """
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
   }
   response = requests.get(pdf_url, headers=headers)
   
   if response.status_code!= 200:
       return f"Error: Unable to fetch document. HTTP Status {response.status_code}"
       
   filestream = io.BytesIO(response.content)
   extracted_text = ""
   
   with fitz.open(stream=filestream, filetype="pdf") as doc:
       for page in doc:
           extracted_text += page.get_text()
           
   return extracted_text

For highly granular data, PyMuPDF supports coordinate-based extraction. When an IPO analyst reviews a DRHP, the most critical data is rarely in the narrative text; it resides in complex tabular structures detailing related-party transactions or capitalization tables. The agent can be configured to pass a clip rectangle to the get_text() method, targeting precise coordinate points on a specific page (for example, clip=fitz.Rect(50, 100, 400, 300)) to extract isolated financial figures without ingesting surrounding legal boilerplate. This methodical approach to document parsing drastically reduces token consumption while maximizing signal-to-noise ratio.

Phase 4: Structuring Domain Expertise via Agent Skills
Equipping an agent with powerful Python tools is fundamentally insufficient without providing the deep domain knowledge of how and when to utilize them. Passing exhaustive, multi-page instructions in the primary system prompt is highly inefficient; it wastes tokens, dilutes the model's attention mechanism, and degrades reasoning quality over time. The architectural solution implemented by the Antigravity platform is the use of "Agent Skills," adhering to the open agentskills.io standard.

Agent Skills operate on a sophisticated principle of "progressive disclosure," which functions in three distinct stages to optimize context window utilization. During the Discovery stage, at startup, the agent loads only the name and a brief description of each available skill, utilizing just enough tokens to know when a skill might be relevant. During the Activation stage, when a user's task matches a specific skill's description, the agent dynamically reads the full instructional document into its active context. Finally, during Execution, the agent follows the procedural instructions step-by-step, optionally executing bundled scripts or loading reference materials.

To structure this capability within the prototype, the developer must create a filesystem-native hierarchy. By default, the Antigravity agent automatically detects and mounts skills placed within the .agents/skills/ directory of the workspace.

Engineering the SKILL.md Configuration
The core of any skill is the SKILL.md file, which requires specific YAML frontmatter to define metadata, followed by Markdown body content containing the operational instructions. The frontmatter mandates two fields: a unique name formatted in lowercase with hyphens, and a comprehensive description that explicitly dictates when the agent should trigger the skill.

For the financial forensics prototype, the developer should create a directory path such as .agents/skills/ipo-forensics/SKILL.md. The content of this file essentially codifies the analytical methodology of a professional researcher into an executable algorithm for the AI.

name: ipo-forensics-analyst description: Activates comprehensive financial research protocols using Tavily web crawling and PyMuPDF extraction to analyze DRHPs, postal ballots, and corporate risk factors.
IPO & Financial Forensics Protocol
When tasked with analyzing a company's financial filings or evaluating an IPO, you must assume the persona of an independent, highly skeptical forensic analyst. You must bypass marketing narratives and execute the following systematic workflow:

Phase 1: Corporate Intelligence Gathering
Deconstruct the user's target company into specific investigative queries.
Use the deep_web_search tool to gather broad context on the company's recent M&A activities, founder history, and grey market premium (GMP) trends.
If investigating an IPO, actively search for recent founder resignations, which often serve as massive warning signs immediately prior to listing.
Phase 2: Document Extraction and Red Flag Identification
Locate the target company's Draft Red Herring Prospectus (DRHP) or postal ballot PDF URL.
Utilize the extract_text_from_remote_pdf tool to read the document into memory. Do not attempt to use standard web scraping tools for PDFs.
Scan the extracted text specifically for deceptive corporate maneuvers. Look for highly disparate reward ratios hidden in annexures (e.g., a default 1:6000 ratio versus a hidden 1109:6000 ratio wrapped in bureaucratic obstacle courses).
Analyze the "Related Party Transactions" section meticulously.
Phase 3: Synthesis and Artifact Generation
Cross-reference all extracted financial data with the web intelligence gathered via Tavily. For instance, if a company claims massive online growth in its DRHP, cross-reference this with news reports detailing costly shifts to hybrid offline models.
Synthesize findings into a comprehensive Markdown artifact outlining the methodology, identified red flags, structural risks, and strategic warnings for retail investors.
By packaging this specific domain expertise into an Agent Skill, the prototype transforms a general-purpose coding assistant into a highly specialized financial research entity without bloating the global configuration or requiring the user to type lengthy prompts.

Phase 5: Synthesizing the Execution Loop and Session State
With the environment initialized, the custom Python tools built, and the domain knowledge encapsulated in an Agent Skill, the actual execution logic must be synthesized using the Python application. The developer will leverage the Antigravity Agent class, which represents Layer 1 of the SDK architecture. This class provides an asynchronous context manager that handles tool wiring, binary discovery, hook registration, and safety policy enforcement entirely behind the scenes.

To properly configure the agent, the developer instantiates a LocalAgentConfig object. By default, the Antigravity agent runs in a strict read-only mode for safety. Because the research agent requires the ability to crawl the web, execute custom tools, and potentially generate markdown files summarizing its findings, the developer must supply capabilities=CapabilitiesConfig() to the configuration, which explicitly enables all write tools and operational capabilities.

The configuration also requires the skills_paths parameter to be explicitly set, pointing the agent to the directory where the ipo-forensics-analyst skill resides. Once the configuration is passed to the Agent class, the developer initiates the autonomous reasoning loop using the chat() method.

To visually highlight the system's technical complexity during a prototype demonstration, the developer should not simply wait for the final output. Instead, the SDK allows for advanced streaming of the model's internal cognitive processes. By asynchronously iterating over the response.thoughts property, the developer can print the agent's internal reasoning deltas to the console in real-time. Similarly, iterating over the response.tool_calls property allows the UI to display exactly when the agent triggers the PyMuPDF extractor or the Tavily crawler.

Managing Advanced Session States via Layer 2
For scenarios requiring granular manipulation of the operational state, developers can bypass the high-level Agent class and interact directly with Layer 2 of the SDK: the Conversation object. While high-level users typically stick to agent.chat(), developers access agent.conversation when they need to inspect the underlying session state.

The Conversation layer tracks the progression of dialogue turns, manages history limits to prevent memory bloat, and actively monitors the specific index points where the model's context has undergone compaction. Because the forensic research agent will ingest highly dense text from massive DRHP PDFs, tracking the agent.conversation.total_usage property allows the system to dynamically monitor token consumption as it approaches the 135,000 token limit. If the usage spikes during a PyMuPDF extraction, the developer can program the system to pause, summarize the current findings into an intermediate artifact, and clear the history buffer before proceeding, ensuring the agent never hallucinates due to context overflow.

Furthermore, the SDK supports multimodal ingestion natively. If a local architectural diagram of a company's corporate shell structure is available, the developer can pass it directly to the agent using the Image class or the from_file() helper method. The agent can seamlessly cross-reference this visual data with the web-crawled research data natively, combining text and imagery into a unified forensic analysis.

Phase 6: Enforcing Security via Declarative Policies and MCP Integration
AI agents equipped with code execution and unrestrained shell access present severe inherent security risks. A single hallucinated terminal command can corrupt the local environment or expose secure credentials to remote servers. The Antigravity SDK mitigates this attack vector through a rigorous Hook Taxonomy and Declarative Tool Call Policies managed by the internal HookRunner.

The SDK classifies operational hooks into three strict, functional types to prevent Time-of-Check to Time-of-Use (TOCTOU) vulnerabilities.

Decide Hooks are read-only and blocking; they execute before any tool is run to evaluate permissions. If a decide hook returns an abort signal, the operation fails instantly.
Transform Hooks are modifying and blocking; they execute to sanitize data or handle interactive user responses before execution.
Inspect Hooks are read-only and non-blocking; they execute asynchronously after a tool successfully runs, used solely for observability and logging.
Instead of forcing developers to write complex raw hook logic, the policy module provides a declarative API that chains builder functions together. Policies are evaluated based on a strict hierarchy of specificity and safety, following a fail-closed strategy where the first matched rule dictates the outcome.

Policy Priority Level

Example Syntax

Operational Behavior

Level 1: Specific DENY

policy.deny("run_command")

Explicitly blocks the named tool from executing under any circumstance.

Level 2: Specific ASK_USER

policy.ask_user("run_command", handler=func)

Pauses execution, requiring the developer to approve the command interactively.

Level 3: Specific APPROVE

policy.allow("view_file")

Grants uninhibited access to a specific tool.

Level 4: Wildcard DENY

policy.deny("*")

Default fail-closed state; blocks all tools not explicitly approved.

To build a robust prototype, the developer must implement an ask_user policy for the native run_command tool. While the agent must be allowed to crawl the web and extract PDFs autonomously, it should never be permitted to execute arbitrary shell scripts downloaded during its research phase without explicit human authorization via a CLI prompt.

Model Context Protocol (MCP) Integration for Dependency Intelligence
If the prototype's objective eventually extends beyond generating markdown reports into writing actual Python code based on its research, it must handle open-source dependencies securely. AI agents do not inherently know which dependencies are secure, well-maintained, or safe to use, risking the introduction of vulnerable or malicious components.

The developer can solve this by integrating the Model Context Protocol (MCP). The Antigravity SDK includes an McpBridge class that seamlessly connects to external MCP servers via standard input/output (stdio), Server-Sent Events (SSE), or Streamable HTTP. By passing mcp_servers=)] into the agent's configuration, the agent gains direct access to Sonatype Guide's dependency intelligence. This empowers the agent to automatically assess dependency risk, check for known malware in specific releases, and verify ecosystem health before ever writing an import statement, establishing a new standard for trusted, AI-assisted development.

Phase 7: Scaling Throughput via Asynchronous Subagents
A true demonstration of advanced agentic capability involves parallelization. Single-threaded LLM processing is a massive bottleneck for deep research, as pulling, parsing, and reasoning over a 500-page financial prospectus completely stalls the main execution loop. The Antigravity platform introduces a paradigm-shifting architecture: programmatic subagent spawning.

Subagents exist to offload complex, highly focused subtasks without polluting the main agent's context window. The parent agent calls an internal invoke_subagent tool, creating a concurrent session with a dedicated role and a clean-slate context window. The subagent runs using the same underlying model as its parent but operates in complete isolation.

In the SDK architecture, subagents exist in distinct lifecycle states. When Running, the subagent is actively executing its specific task, calling its own tools, and generating intermediate responses. Because these subagents run as asynchronous background tasks, the main agent yields control immediately, establishing a polling loop or intercepting an event stream to catch the subagent's progress logs in real-time. Once the task is complete, the subagent transitions to the Idle state, sending a finalized message containing the condensed results back to the parent agent, and safely terminating its execution.

Applying Subagents to the Financial Forensics Prototype
To highlight maximum technical strength in the prototype, the developer should instruct the main agent (via the SKILL.md instructions) to aggressively utilize subagents for the research workflow.

When the user queries the system to analyze a complex entity, the main agent will deconstruct the prompt into parallel investigative tracks. It will spawn Subagent A with instructions to utilize the PyMuPDF tool to extract and analyze the company's DRHP for predatory equity structures. Simultaneously, it will spawn Subagent B to utilize the Tavily smart_site_crawl tool to scan Reddit forums and market news sites for real-time sentiment regarding the company's grey market premium. Furthermore, it could spawn Subagent C to query public GSTIN records to cross-reference corporate structures.

The parent agent simply waits asynchronously. When Subagents A, B, and C transition to the idle state and return their findings, the parent agent synthesizes the disparate data streams into a cohesive, highly nuanced forensic report. This architectural pattern transforms a slow, linear AI into a highly efficient, multi-threaded research team.

Phase 8: Architectural Best Practices for Token Optimization (Free Tier Maximization)
When operating within the constraints of the free Antigravity tier, strict token budgeting is essential. The prototype must implement the following rule set to minimize AI token consumption and maximize efficiency:

Utilize TOON over JSON for Structured Data: Traditional JSON is highly inefficient for LLM context windows due to repeated keys, quotes, and brackets, often acting as "chatty" structural overhead. Instead, the prototype should serialize data outputs using TOON (Token-Oriented Object Notation). TOON uses YAML-like indentation and CSV-style tabular layouts for uniform arrays, reducing token usage by 30% to 60% compared to JSON. The architecture should maintain JSON for backend APIs but convert data to TOON strictly for the LLM prompt ingestion.
Hard-Disable Unused Tools: Use the CapabilitiesConfig.disabled_tools parameter to completely remove irrelevant tools from the model's context. Unlike hook-based policies (such as policy.deny()), which still allow the model to see the tool and waste tokens attempting to use it before being rejected, disabling tools at the configuration level costs zero tokens.
Progressive Disclosure via Agent Skills: Do not load all procedural instructions into the main system prompt. By relying on the SKILL.md progressive disclosure mechanism, the agent only loads the skill's name and description during the initial Discovery phase, saving significant token overhead until the specific research skill is actually invoked.
Coordinate-Based Extraction: When parsing PDFs with PyMuPDF, avoid dumping entire documents into the context window. Use fitz.Rect coordinate clipping to extract only the specific bounding boxes that contain tabular financial data, radically reducing the text footprint.
Parallelize Context via Subagents: Offload heavy document reading to asynchronous subagents. Because subagents do not inherit the parent's conversation history, they can process massive text payloads in their own isolated context windows, returning only token-light summaries to the main agent.
Phase 9: Automating Workflows with Scheduled Triggers
While hooks react inline to the agent's internal lifecycle events, the Antigravity SDK also provides an architecture for "Triggers," which are long-lived asynchronous functions that run alongside an agent session in the background and react to external events, such as timers or cron schedules.

Triggers communicate back to the active session by pushing messages directly into the agent using a TriggerContext. There are two primary methods for scheduling triggers. The developer can manually schedule a trigger using the @triggers.trigger decorator on an async def function containing an infinite loop controlled by asyncio.sleep(). Alternatively, the developer can use the every() helper factory to schedule recurring callbacks on a fixed interval.

For the financial forensics prototype, triggers enable continuous monitoring. The developer can register a trigger that executes the Tavily search tool every 3600 seconds (one hour) to check for breaking news regarding a specific IPO. If the trigger detects a newly published article detailing a sudden founder resignation or an auditor flagging internal control failures, it pushes a critical alert into the agent's active context window, prompting the agent to instantly update its forensic report with the new intelligence. This transitions the prototype from a static analysis tool into a dynamic, real-time monitoring system.

Strategic Deployment Timeline (June 2 to June 7)
Delivering a highly functional, complex prototype by the June 7th deadline requires a disciplined, phase-based software engineering strategy. Given the current date of June 2, the developer has exactly five days to execute the architecture.

Date

Phase

Execution Objectives

June 2

Infrastructure & Dependencies

Complete the pip installations for google-antigravity, tavily-python, and pymupdf. Authenticate all API keys (GEMINI_API_KEY, TAVILY_API_KEY). Verify the presence of the compiled runtime binary by running a basic "Hello World" agent script.

June 3

Tool Engineering

Construct the foundational Python tool wrappers for the web and document extraction functionalities. Ensure type hints and docstrings are rigorously defined so the ToolRunner correctly generates the JSON schemas. Test the io.BytesIO PyMuPDF extraction on a sample PDF to verify memory efficiency.

June 4

Progressive Disclosure & Skills

Design the .agents/skills/ipo-forensics directory structure. Write the SKILL.md file, embedding strict methodological rules for the financial research workflow. Enforce the separation of information gathering, extraction, and synthesis within the instructions.

June 5

Advanced Orchestration & Policies

Construct the main async application loop using the Layer 1 Agent class. Implement the declarative safety policies (policy.ask_user) to guarantee secure sandboxing for shell commands. Integrate the CapabilitiesConfig and define the skills_paths.

June 6

Subagent Parallelization & Testing

Refine the system prompts to trigger subagent invocation. Test the system with a highly complex query—such as analyzing the PhysicsWallah DRHP—to observe the asynchronous delegation of tasks and the behavior of the context compaction mechanism when processing large document payloads.

June 7

Final Polish & Demonstration

Implement the CLI streaming logic to visualize response.thoughts and response.tool_calls. This proves to observers an understanding of the underlying asynchronous event loop and highlights the technical strength of the prototype by exposing the AI's dynamic reasoning pathways in real-time.

By systematically layering custom API tools over the Google Antigravity SDK, enforcing declarative safety policies, leveraging progressive disclosure via Agent Skills, orchestrating asynchronous subagents for parallel processing, and rigidly optimizing token consumption through TOON formatting, the developer will produce a formidable prototype. This implementation thoroughly masks a lack of traditional data analytics experience by replacing manual statistical modeling with advanced, autonomous systems engineering, resulting in a highly capable financial forensics tool delivered exactly on schedule.

Works cited
1. PyMuPDF is a high performance Python library for data extraction, analysis, conversion & manipulation of PDF (and other) documents. - GitHub, https://github.com/pymupdf/pymupdf 2. GitHub - google-antigravity/antigravity-sdk-python: A Python library ..., https://github.com/google-antigravity/antigravity-sdk-python 3. Antigravity: Build Your First AI Agent Skill - YouTube, https://www.youtube.com/watch?v=gRAndTHbHWo&vl=en 4. Asynchronous Subagents - Google Antigravity Documentation, https://antigravity.google/docs/subagents