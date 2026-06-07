import os
import io
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

# Initialize Tavily client from environment variable
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = None

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def get_tavily_client() -> TavilyClient:
    """Ensures Tavily Client is initialized at runtime."""
    global tavily_client
    if not tavily_client:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set.")
        tavily_client = TavilyClient(api_key=api_key)
    return tavily_client


def deep_web_search(query: str, search_depth: str = "advanced", max_results: int = 20) -> dict:
    """
    Executes a comprehensive web search to gather up-to-date market, macro, and policy intelligence.
    Provides sources, answers, and context required for in-depth forensics.
    
    Args:
        query: The search term or research question.
        search_depth: The search depth ('basic' or 'advanced'). Defaults to 'advanced'.
        max_results: The maximum number of search results to return. Defaults to 20.
    """
    client = get_tavily_client()
    return client.search(query=query, search_depth=search_depth, max_results=max_results)


def smart_site_crawl(url: str, instructions: str) -> dict:
    """
    Performs a smart crawl starting at a given root URL.
    It navigates subpages to extract content matching the specific instructions provided.
    Ideal for targeted policy crawls (e.g., NITI Aayog, PIB) or company-specific controversies.
    
    Args:
        url: The root URL to crawl.
        instructions: Natural language instructions detailing what content to extract.
    """
    client = get_tavily_client()
    return client.crawl(url, instructions=instructions)


def scrape_webpage_content(url: str) -> str:
    """
    Downloads the HTML content of a given URL, parses it using BeautifulSoup4,
    strips ads, navigation menus, footers, scripts, and styles, and returns cleaned body text.
    Provides high-fidelity, complete context instead of short snippets.
    
    Args:
        url: The webpage URL to scrape.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return f"Error: Unable to fetch page. HTTP Status {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strip out non-content boilerplate elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            element.decompose()
            
        # Extract and clean textual content
        text = soup.get_text(separator=' ')
        
        # Compress whitespaces and newlines to optimize token consumption
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if len(clean_text) > 25000:
            # Prevent extreme context blow-up per single page
            clean_text = clean_text[:25000] + "\n... [CONTENT TRUNCATED FOR CONTEXT BUDGET] ..."
            
        return clean_text
        
    except Exception as e:
        return f"Error: Web scraper failed to retrieve content. Detail: {str(e)}"


def extract_text_from_remote_pdf(pdf_url: str, clip_coords: list = None) -> str:
    """
    Downloads a PDF document from a provided URL entirely in-memory and extracts textual content.
    Avoids I/O latency and permission issues in ephemeral sandboxes.
    Enforces a strict 60,000 character extraction cap to prevent API payload timeouts.
    Includes robust fallback from PyMuPDF (fitz) to pypdf if DLL bindings are missing on Windows.
    
    Args:
        pdf_url: The URL of the PDF document.
        clip_coords: Optional list of 4 floats [x0, y0, x1, y1] specifying a Rect coordinate bounding box to extract.
                     Saves tokens by skipping surrounding legal boilerplate. Only supported under PyMuPDF.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Robust retry loop to handle unstable CDN connections or incomplete reads (ProtocolError/IncompleteRead)
    response = None
    last_err = ""
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            res = requests.get(pdf_url, headers=headers, timeout=25)
            if res.status_code == 200:
                # Accessing .content triggers the download stream and lets us catch incomplete read errors here
                _ = res.content
                response = res
                break
            else:
                last_err = f"HTTP Status {res.status_code}"
        except Exception as e:
            last_err = str(e)
            
        if attempt < max_retries:
            import time
            time.sleep(1.5)
            
    if not response:
        return f"Error: Unable to fetch document after {max_retries} attempts. Details: {last_err}"
        
    filestream = io.BytesIO(response.content)
    extracted_text = ""
    
    # 1. Attempt high-performance PyMuPDF extraction
    try:
        import fitz  # Attempt to import PyMuPDF
        
        # Bounding box clipping
        clip_rect = None
        if clip_coords and len(clip_coords) == 4:
            clip_rect = fitz.Rect(clip_coords[0], clip_coords[1], clip_coords[2], clip_coords[3])
            
        with fitz.open(stream=filestream, filetype="pdf") as doc:
            for page_num, page in enumerate(doc, 1):
                # Enforce context budget limit per PDF
                if len(extracted_text) > 60000:
                    extracted_text += "\n... [PDF TEXT TRUNCATED TO CAPPED CONTEXT BUDGET] ...\n"
                    break
                    
                if clip_rect:
                    page_text = page.get_text(clip=clip_rect)
                else:
                    page_text = page.get_text()
                    
                if page_text.strip():
                    extracted_text += f"--- PAGE {page_num} ---\n{page_text}\n"
                    
        if extracted_text.strip():
            return extracted_text
            
    except (ImportError, Exception) as e:
        # Fallback to pure-Python pypdf if PyMuPDF fails or experiences C-DLL issues
        pass
        
    # 2. Pure-Python Fallback (100% Reliable on Windows)
    try:
        import pypdf
        
        filestream.seek(0)
        reader = pypdf.PdfReader(filestream)
        
        for page_num, page in enumerate(reader.pages, 1):
            # Enforce context budget limit per PDF
            if len(extracted_text) > 60000:
                extracted_text += "\n... [PDF TEXT TRUNCATED TO CAPPED CONTEXT BUDGET] ...\n"
                break
                
            page_text = page.extract_text()
            if page_text and page_text.strip():
                extracted_text += f"--- PAGE {page_num} ---\n{page_text}\n"
                
        if clip_coords:
            extracted_text = f"[WARNING: Coordinate clipping skipped due to C-extensions load failure. Displaying full pages.]\n{extracted_text}"
            
    except Exception as e:
        return f"Error: Extraction failed under both PyMuPDF and pypdf fallbacks. Detail: {str(e)}"
        
    if not extracted_text.strip():
        return "Warning: No text extracted. The document may be scanned or empty."
        
    return extracted_text
