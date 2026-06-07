import os
import sys
import json
import asyncio

# Reconfigure standard output/error to UTF-8 on Windows to prevent UnicodeEncodeError crashes (e.g. Rupee symbol '₹')
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
from custom_tools import deep_web_search, smart_site_crawl, scrape_webpage_content, extract_text_from_remote_pdf

# Flag to check if we are in the remote Antigravity environment
HAS_SDK = False
try:
    from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
    from google.antigravity.policies import policy
    from google.antigravity.triggers import triggers
    HAS_SDK = True
except ImportError:
    pass


def get_usd_to_inr_rate():
    try:
        import urllib.request, json
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/USD", timeout=3) as response:
            data = json.loads(response.read().decode())
            return float(data["rates"]["INR"])
    except Exception as e:
        print(f"[-] Could not fetch live USD/INR exchange rate: {e}. Falling back to 84.0")
        return 84.0


class APIUsageTracker:
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost_usd = 0.0
        
    def add_usage(self, model_name, response):
        if not response or not hasattr(response, 'usage_metadata') or not response.usage_metadata:
            return
        meta = response.usage_metadata
        inputs = getattr(meta, 'prompt_token_count', 0) or 0
        outputs = getattr(meta, 'candidates_token_count', 0) or 0
        
        self.input_tokens += inputs
        self.output_tokens += outputs
        
        # Calculate Cost (standard pay-as-you-go rates)
        # Gemini 1.5/2.5 Flash: $0.075 / 1M input, $0.30 / 1M output
        # Gemini 1.5/2.5 Pro: $1.25 / 1M input, $5.00 / 1M output
        if "pro" in model_name.lower():
            cost = (inputs * 1.25 / 1_000_000) + (outputs * 5.00 / 1_000_000)
        else:
            cost = (inputs * 0.075 / 1_000_000) + (outputs * 0.30 / 1_000_000)
        self.total_cost_usd += cost

    def get_stats(self):
        rate = get_usd_to_inr_rate()
        cost_inr = self.total_cost_usd * rate
        return {
            "total_input_tokens": self.input_tokens,
            "total_output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            "total_cost_usd": self.total_cost_usd,
            "total_cost_inr": cost_inr,
            "usd_to_inr_rate": rate
        }


usage_tracker = APIUsageTracker()


# =====================================================================
# SQUAD QUANTITATIVE & FORENSIC ACCOUNTING MATHEMATICAL MODELS
# =====================================================================

def calculate_kelly_criterion(win_prob: float, win_loss_ratio: float) -> dict:
    """Calculates the Kelly Criterion fraction and recommended fractional sizing."""
    try:
        p = float(win_prob)
        r = float(win_loss_ratio)
        if r <= 0:
            return {"win_probability": p, "win_loss_ratio": r, "kelly_fraction_percentage": 0.0, "fractional_kelly_percentage": 0.0}
        q = 1.0 - p
        f_star = p - (q / r)
        f_star_pct = max(0.0, f_star * 100.0)
        return {
            "win_probability": p,
            "win_loss_ratio": r,
            "kelly_fraction_percentage": f_star_pct,
            "fractional_kelly_percentage": f_star_pct / 4.0
        }
    except Exception:
        return {"win_probability": 0.0, "win_loss_ratio": 0.0, "kelly_fraction_percentage": 0.0, "fractional_kelly_percentage": 0.0}


def calculate_dupont_5_factor(tax_burden: float, interest_burden: float, operating_margin: float, asset_turnover: float, leverage: float) -> dict:
    """Calculates DuPont 5-Factor ROE decomposition."""
    try:
        tb = float(tax_burden)
        ib = float(interest_burden)
        om = float(operating_margin)
        at = float(asset_turnover)
        lev = float(leverage)
        roe = tb * ib * om * at * lev * 100.0
        return {
            "roe_percentage": roe,
            "factors": {
                "tax_burden": tb,
                "interest_burden": ib,
                "operating_margin": om,
                "asset_turnover": at,
                "equity_multiplier": lev
            }
        }
    except Exception:
        return {
            "roe_percentage": 0.0,
            "factors": {
                "tax_burden": 1.0,
                "interest_burden": 1.0,
                "operating_margin": 0.0,
                "asset_turnover": 0.0,
                "equity_multiplier": 1.0
            }
        }


def calculate_sloan_ratio(net_income: float, operating_cash_flow: float, investing_cash_flow: float, total_assets: float) -> dict:
    """Calculates the Sloan Ratio to detect earnings quality."""
    try:
        ni = float(net_income)
        ocf = float(operating_cash_flow)
        icf = float(investing_cash_flow)
        ta = float(total_assets)
        if ta <= 0:
            return {"ratio_percentage": 0.0, "verdict": "LOW", "variables": {"net_income": ni, "operating_cf": ocf, "investing_cf": icf, "total_assets": ta}}
        ratio = (ni - ocf - icf) / ta
        ratio_pct = ratio * 100.0
        abs_ratio_pct = abs(ratio_pct)
        if abs_ratio_pct > 10.0:
            verdict = "HIGH"
        elif abs_ratio_pct > 5.0:
            verdict = "MODERATE"
        else:
            verdict = "LOW"
        return {
            "ratio_percentage": ratio_pct,
            "verdict": verdict,
            "variables": {
                "net_income": ni,
                "operating_cf": ocf,
                "investing_cf": icf,
                "total_assets": ta
            }
        }
    except Exception:
        return {"ratio_percentage": 0.0, "verdict": "LOW", "variables": {"net_income": 0.0, "operating_cf": 0.0, "investing_cf": 0.0, "total_assets": 1.0}}


def calculate_beneish_m_score(dsri: float, gmi: float, aqi: float, sgi: float, depi: float, sgai: float, lvgi: float, tata: float) -> dict:
    """Calculates the Beneish M-Score for earnings manipulation detection."""
    try:
        m_score = -4.84 + (0.920 * float(dsri)) + (0.528 * float(gmi)) + (0.404 * float(aqi)) + (0.892 * float(sgi)) + (0.115 * float(depi)) - (0.172 * float(sgai)) + (4.037 * float(tata)) + (0.0327 * float(lvgi))
        verdict = "MANIPULATION RISK" if m_score > -1.78 else "SAFE"
        return {
            "score": m_score,
            "verdict": verdict,
            "variables": {
                "dsri": dsri, "gmi": gmi, "aqi": aqi, "sgi": sgi,
                "depi": depi, "sgai": sgai, "lvgi": lvgi, "tata": tata
            }
        }
    except Exception:
        return {
            "score": -4.84,
            "verdict": "SAFE",
            "variables": {
                "dsri": 1.0, "gmi": 1.0, "aqi": 1.0, "sgi": 1.0,
                "depi": 1.0, "sgai": 1.0, "lvgi": 1.0, "tata": 0.0
            }
        }


def fermi_tam_check(reported_tam: float, physical_limit: float) -> dict:
    """Checks if reported TAM exceeds physical/logical bounds by more than 3x."""
    try:
        rep = float(reported_tam)
        limit = float(physical_limit)
        if limit <= 0:
            return {"reported_tam_usd": rep, "physical_limit_usd": limit, "discrepancy_ratio": 1.0, "warning_triggered": False}
        ratio = rep / limit
        warning = ratio > 3.0
        return {
            "reported_tam_usd": rep,
            "physical_limit_usd": limit,
            "discrepancy_ratio": ratio,
            "warning_triggered": warning
        }
    except Exception:
        return {"reported_tam_usd": 0.0, "physical_limit_usd": 1.0, "discrepancy_ratio": 1.0, "warning_triggered": False}


def calculate_bass_diffusion(p: float, q: float) -> dict:
    """Estimates years to market maturity using innovation (p) and imitation (q) coefficients."""
    try:
        p_val = float(p)
        q_val = float(q)
        if p_val <= 0 or q_val <= 0:
            return {"p_innovation": p_val, "q_imitation": q_val, "years_to_maturity": 0.0}
        import math
        t_star = (1.0 / (p_val + q_val)) * math.log(q_val / p_val)
        return {
            "p_innovation": p_val,
            "q_imitation": q_val,
            "years_to_maturity": max(0.0, t_star)
        }
    except Exception:
        return {"p_innovation": 0.001, "q_imitation": 0.38, "years_to_maturity": 15.0}


def calculate_power_law_alpha(market_shares: list) -> dict:
    """Computes power law alpha exponent for industry consolidation level."""
    try:
        shares = [float(s) for s in market_shares if float(s) > 0]
        if not shares or len(shares) < 2:
            return {"exponent_alpha": 1.5, "concentration_verdict": "FRAGMENTED"}
        shares.sort(reverse=True)
        import math
        ratio = shares[0] / shares[1]
        alpha = 1.0 / math.log(ratio) if ratio > 1.0 else 2.0
        verdict = "WINNER-TAKE-ALL" if alpha < 1.2 else "FRAGMENTED"
        return {
            "exponent_alpha": alpha,
            "concentration_verdict": verdict
        }
    except Exception:
        return {"exponent_alpha": 1.5, "concentration_verdict": "FRAGMENTED"}


def process_quantitative_models(report_data: dict) -> dict:
    """Deterministic math calculation for SQUAD models."""
    q_models = report_data.get("quantitative_models", {})
    
    # 1. Beneish M-Score
    b_data = q_models.get("beneish_m_score", {})
    dsri = b_data.get("dsri", 1.0)
    gmi = b_data.get("gmi", 1.0)
    aqi = b_data.get("aqi", 1.0)
    sgi = b_data.get("sgi", 1.0)
    depi = b_data.get("depi", 1.0)
    sgai = b_data.get("sgai", 1.0)
    lvgi = b_data.get("lvgi", 1.0)
    tata = b_data.get("tata", 0.0)
    report_data.setdefault("quantitative_models", {})["beneish_m_score"] = calculate_beneish_m_score(dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata)
    
    # 2. Sloan Ratio
    s_data = q_models.get("sloan_ratio", {})
    ni = s_data.get("net_income", 0.0)
    ocf = s_data.get("operating_cash_flow", 0.0)
    icf = s_data.get("investing_cash_flow", 0.0)
    ta = s_data.get("total_assets", 1.0)
    report_data["quantitative_models"]["sloan_ratio"] = calculate_sloan_ratio(ni, ocf, icf, ta)
    
    # 3. DuPont 5-Factor
    d_data = q_models.get("dupont_5_factor", {})
    tb = d_data.get("tax_burden", 1.0)
    ib = d_data.get("interest_burden", 1.0)
    om = d_data.get("operating_margin", 0.0)
    at = d_data.get("asset_turnover", 0.0)
    lev = d_data.get("leverage", 1.0)
    report_data["quantitative_models"]["dupont_5_factor"] = calculate_dupont_5_factor(tb, ib, om, at, lev)
    
    # 4. Kelly Criterion
    k_data = q_models.get("kelly_criterion", {})
    wp = k_data.get("win_probability", 0.0)
    wlr = k_data.get("win_loss_ratio", 0.0)
    report_data["quantitative_models"]["kelly_criterion"] = calculate_kelly_criterion(wp, wlr)
    
    # 5. Fermi TAM Check
    f_data = q_models.get("fermi_tam_check", {})
    rep_tam = f_data.get("reported_tam_usd", 0.0)
    phys_lim = f_data.get("physical_limit_usd", 1.0)
    report_data["quantitative_models"]["fermi_tam_check"] = fermi_tam_check(rep_tam, phys_lim)
    
    # 6. Bass Diffusion
    bass_data = q_models.get("bass_diffusion", {})
    p = bass_data.get("p_innovation", 0.001)
    q = bass_data.get("q_imitation", 0.38)
    report_data["quantitative_models"]["bass_diffusion"] = calculate_bass_diffusion(p, q)
    
    # 7. Power Law Alpha
    pl_data = q_models.get("power_law_alpha", {})
    shares = pl_data.get("market_shares", [0.0, 0.0])
    report_data["quantitative_models"]["power_law_alpha"] = calculate_power_law_alpha(shares)
    
    # 8. EVT Tail Risk
    evt_data = q_models.get("evt_tail_risk", {})
    report_data["quantitative_models"]["evt_tail_risk"] = {
        "cvar_95_percent": float(evt_data.get("cvar_95_percent", 0.0)),
        "evt_99_percent_cvar": float(evt_data.get("evt_99_percent_cvar", 0.0))
    }
    
    return report_data


def convert_to_toon(data: dict) -> str:
    """
    Serializes data into TOON (Token-Oriented Object Notation) format.
    Uses YAML-like indentation and CSV-style tabular layouts to save 30-60% token overhead.
    """
    import yaml
    clean_data = {}
    for k, v in data.items():
        if isinstance(v, list):
            if v and isinstance(v[0], dict):
                headers = list(v[0].keys())
                csv_lines = [",".join(headers)]
                for item in v:
                    csv_lines.append(",".join([str(item.get(h, "")) for h in headers]))
                clean_data[k] = "\n".join(csv_lines)
            else:
                clean_data[k] = v
        else:
            clean_data[k] = v
    return yaml.dump(clean_data, default_flow_style=False)


def semantic_compress_text(text: str, query: str) -> str:
    """
    Compresses long natural language text (scraped pages/PDFs) before embedding it
    into LLM prompts. Extracts only keyword-adjacent paragraphs, saving 60-90% tokens.
    """
    if not text or len(text) < 2000:
        return text
        
    import re
    # Extract keywords of length >= 3 from the query
    query_words = re.findall(r'[a-zA-Z0-9]{3,}', query.lower())
    stopwords = {
        "the", "and", "for", "with", "from", "that", "this", "these", "those",
        "they", "their", "them", "have", "has", "had", "been", "will", "would",
        "should", "could", "about", "into", "onto", "under", "over", "above",
        "between", "among", "through", "during", "before", "after", "while",
        "because", "since", "until", "unless", "although", "though", "even",
        "also", "than", "then", "their", "your", "mine", "some", "many", "more",
        "most", "very", "much", "such", "both", "each", "every", "other", "another"
    }
    keywords = [w for w in query_words if w not in stopwords]
    
    paragraphs = text.split('\n')
    compressed_paragraphs = []
    matched_indices = []
    
    for idx, p in enumerate(paragraphs):
        p_lower = p.lower()
        matches = sum(1 for kw in keywords if kw in p_lower)
        if matches > 0:
            matched_indices.append(idx)
            
    if not matched_indices:
        # Fallback to a truncated summary of the first 4000 characters
        return text[:4000] + "\n... [CAPPED FALLBACK FOR CONTEXT BUDGET] ..."
        
    # Group matched paragraphs with a context window of +/- 1 paragraph
    selected_indices = set()
    for idx in matched_indices:
        if idx > 0:
            selected_indices.add(idx - 1)
        selected_indices.add(idx)
        if idx < len(paragraphs) - 1:
            selected_indices.add(idx + 1)
            
    last_idx = -2
    for idx in sorted(selected_indices):
        p_text = paragraphs[idx].strip()
        if not p_text:
            continue
        if idx != last_idx + 1 and last_idx != -2:
            compressed_paragraphs.append("[...]")
        compressed_paragraphs.append(p_text)
        last_idx = idx
        
    compressed_text = "\n".join(compressed_paragraphs)
    
    # Enforce a strict cap of 6000 characters per single document
    if len(compressed_text) > 6000:
        compressed_text = compressed_text[:6000] + "\n... [TRUNCATED] ..."
        
    return compressed_text


def reconstruct_markdown_report(data: dict) -> str:
    """
    Programmatically reconstructs a detailed, professional briefing markdown report
    from the structured JSON fields. Saves thousands of output tokens by avoiding
    redundant text generation in the LLM.
    """
    subject = data.get("subject", "Investigative Forensics Report")
    case_study = data.get("forensic_case_study", {})
    headline = case_study.get("headline", "Forensic Investigation Findings")
    verdict = case_study.get("editorial_verdict", "No editorial verdict compiled.")
    comparison = case_study.get("side_by_side_comparison", {})
    conclusion = case_study.get("conclusion_question", "")
    
    trust_gap = data.get("forensic_trust_gap", {})
    executive_brief = data.get("executive_brief", "No executive briefing available.")
    
    md = []
    md.append(f"# {subject.upper()}\n")
    md.append(f"## {headline.upper()}\n")
    md.append(f"### Editorial Verdict & Outlook\n{verdict}\n")
    
    if comparison and "rows" in comparison:
        headers = comparison.get("column_headers", {"standard_label": "Standard", "target_label": "Target"})
        std_h = headers.get("standard_label", "Standard")
        tgt_h = headers.get("target_label", "Target")
        
        md.append("### Key Data Mismatches & Variance Matrix")
        md.append(f"| Metric / Line Item | {std_h} | {tgt_h} | Mismatch Variance |")
        md.append("| :--- | :--- | :--- | :--- |")
        for row in comparison.get("rows", []):
            metric = row.get("metric", "")
            std_v = row.get("standard_value", "")
            tgt_v = row.get("target_value", "")
            var_p = row.get("mismatch_percentage", "")
            md.append(f"| {metric} | {std_v} | {tgt_v} | {var_p} |")
        md.append("\n")
        
    if conclusion:
        md.append(f"**Outlook Reflection:** *{conclusion}*\n")
        
    md.append(f"## Executive Briefing & Context\n{executive_brief}\n")
    
    trust_std = trust_gap.get("standard_sources_coverage", "")
    trust_exp = trust_gap.get("our_forensic_exposure", "")
    trust_rat = trust_gap.get("unique_trust_rationale", "")
    if trust_std or trust_exp or trust_rat:
        md.append("### The Forensic Trust Gap")
        if trust_std:
            md.append(f"- **Standard Media/Broker Coverage:** {trust_std}")
        if trust_exp:
            md.append(f"- **Our Forensic Exposure:** {trust_exp}")
        if trust_rat:
            md.append(f"- **Why This Teardown Matters:** {trust_rat}")
        md.append("\n")
        
    anomalies = data.get("anomalies", [])
    if anomalies:
        md.append("## Deconstructed Anomalies & Verdicts")
        for idx, a in enumerate(anomalies, 1):
            claim = a.get("source_claim", "")
            counter = a.get("counter_claim", "")
            verd = a.get("verdict", "")
            sev = a.get("severity", "Medium")
            typ = a.get("type", "Narrative")
            
            md.append(f"### Anomaly {idx}: {claim[:80]}...")
            md.append(f"- **Source Claim:** {claim}")
            md.append(f"- **Counter-Claim/Defense:** {counter}")
            md.append(f"- **Forensic Verdict:** **{verd}**")
            md.append(f"- **Audit Metrics:** Severity: *{sev}* | Type: *{typ}*")
            
            citations = a.get("citations", [])
            if citations:
                links = [f"[{c.get('name', 'Source')}]({c.get('url', '#')})" for c in citations]
                md.append(f"- **Backing Sources:** {', '.join(links)}")
            md.append("\n")
            
    tracks = data.get("tracks", {})
    if tracks:
        md.append("## Multi-Track Forensic Findings")
        for track_name in ["corporate", "policy", "sovereign"]:
            t_data = tracks.get(track_name, {})
            text = t_data.get("text", "")
            if text:
                md.append(f"### Track: {track_name.title()}")
                md.append(f"{text}\n")
                
    socio = data.get("socioeconomic", [])
    if socio:
        md.append("## Socioeconomic & Industry Impact Vectors")
        for s in socio:
            area = s.get("area", "")
            impact = s.get("impact", "")
            outcome = s.get("outcome", "")
            md.append(f"### Vector: {area}")
            md.append(f"- **Structural Impact:** {impact}")
            md.append(f"- **Outcome/Vector Direction:** **{outcome}**")
            md.append("\n")
            
    igs = data.get("india_growth_story", {})
    if igs:
        md.append("## India Growth Story Outlook")
        md.append(f"### {igs.get('title', 'Outlook Teardown')}")
        md.append(f"{igs.get('narrative', '')}\n")
        md.append(f"- **India Ecosystem Outlook/Vector:** **{igs.get('outlook', '')}**")
        md.append("\n")
            
    benchmarks = data.get("strategic_benchmarks", [])
    if benchmarks:
        md.append("## Strategic Case Benchmarks")
        for b in benchmarks:
            model = b.get("model_project", "")
            well = b.get("what_they_did_well", "")
            short = b.get("our_target_shortfall", "")
            learn = b.get("strategic_learning", "")
            
            md.append(f"### Model Project: {model}")
            md.append(f"- **Best Practice:** {well}")
            md.append(f"- **Target Shortfall:** {short}")
            md.append(f"- **Key Takeaway:** {learn}\n")
            
    deep_dive = data.get("deep_dive")
    if deep_dive:
        md.append("## Deep-Dive Anomaly Investigation")
        md.append(f"### {deep_dive.get('title', 'Deep-Dive Findings').upper()}")
        md.append(f"{deep_dive.get('narrative', '')}\n")
        metrics = deep_dive.get("metrics", [])
        if metrics:
            md.append("#### Key Deep-Dive Metrics")
            for m in metrics:
                md.append(f"- **{m.get('label', '')}:** {m.get('value', '')}")
            md.append("\n")
        citations = deep_dive.get("citations", [])
        if citations:
            links = [f"[{c.get('name', 'Source')}]({c.get('url', '#')})" for c in citations]
            md.append(f"- **Backing Sources:** {', '.join(links)}")
            md.append("\n")

    citations = data.get("citations", [])
    if citations:
        md.append("## Global References & Citations")
        for c in citations:
            name = c.get("name", "")
            url = c.get("url", "")
            md.append(f"- [{name}]({url})")
            
    return "\n".join(md)



# =====================================================================
# SDK RUNTIME MODE (Linux Sandbox)
# =====================================================================
async def run_sdk_mode(query: str):
    print("[*] Launching in Antigravity SDK Mode...")
    
    def interactive_cli_prompt(tool_name, args):
        print(f"\n[SECURITY ALERT] Agent requested execution of: {tool_name} with {args}")
        print("[-] Blocked for safety by declarative policy.")
        return False

    policy.ask_user("run_command", handler=interactive_cli_prompt)
    policy.deny("delete_file")
    policy.allow("view_file")
    
    config = LocalAgentConfig(
        skills_paths=["./.agents/skills"],
        capabilities=CapabilitiesConfig(
            allow_write=True,
            disabled_tools=["delete_file"]
        ),
        tools=[deep_web_search, smart_site_crawl, extract_text_from_remote_pdf]
    )
    
    async with Agent(config) as agent:
        print("[*] Antigravity Agent initialized. Spawning multi-track forensics subagents...")
        response = await agent.chat(
            f"You are the macro-corporate-forensics-analyst. Run a full 5-track analysis on: {query}"
        )
        
        async def stream_thoughts():
            async for thought in response.thoughts:
                sys.stdout.write(f"\r[Cognitive Stream]: {thought}")
                sys.stdout.flush()
                
        async def stream_tools():
            async for call in response.tool_calls:
                print(f"\n[Tool Execution]: Dispatching {call.name} with arguments {call.args}")
                
        await asyncio.gather(stream_thoughts(), stream_tools())
        
        print("\n" + "="*60)
        print("   FINAL RESEARCH REPORT   ")
        print("="*60)
        print(await response.text())
        print("="*60)


def generate_folder_slug(client, query: str) -> str:
    """
    Calls gemini-2.5-flash to generate a safe, 1-3 word lowercase slug
    for the query to act as the folder name.
    """
    from google.genai import types
    prompt = f"""
    Analyze the user query under investigation and convert it into a safe, maximum 3-word directory slug.
    The slug must be all lowercase, with words separated by underscores. Do not include any special characters or file extensions.
    Example query: "Identify all the bottlenecks in the Ola Electric DRHP" -> "ola_electric_drhp"
    Example query: "台湾の半導体エコシステム" -> "taiwan_semiconductor"
    
    Query to slugify: "{query}"
    
    Output ONLY the raw slug string.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0)
        )
        usage_tracker.add_usage("gemini-2.5-flash", response)
        slug = response.text.strip().lower()
        # Clean slug of any whitespace or characters just in case
        slug = "".join([c if c.isalnum() or c == "_" else "_" for c in slug])
        # Replace multiple underscores
        import re
        slug = re.sub(r'_+', '_', slug).strip('_')
        # Limit to max 3 words
        words = slug.split('_')
        if len(words) > 3:
            slug = "_".join(words[:3])
        return slug
    except Exception as e:
        # Fallback to local heuristic slugify
        import re
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', query).lower()
        words = clean.split()[:3]
        return "_".join(words) if words else "forensics_report"


def expand_search_queries(client, query: str) -> dict:
    """
    Uses gemini-2.5-flash to parse the raw user query, extract the target entity name,
    and generate a dictionary of laser-focused search queries for document and context retrieval.
    """
    from google.genai import types
    prompt = f"""
    You are a Search Query Architect. Analyze the raw user query and extract:
    1. The core target entity name (e.g., "InCred Holdings Limited", "Ola Electric").
    2. The primary filing or document type being asked for (e.g., "DRHP", "Postal Ballot", "Annual Report").
    
    Then, generate three specific search queries:
    - "pdf_query": A query targeting direct PDF files of the filing (e.g., "InCred Holdings Limited DRHP filetype:pdf")
    - "regulatory_query": A query targeting official regulatory repositories like SEBI or stock exchanges (e.g., "InCred Holdings Limited DRHP site:sebi.gov.in")
    - "context_query": A query targeting news, analyses, bottlenecks, and controversies (e.g., "InCred Holdings Limited IPO bottlenecks risks controversies")
    
    User Query: "{query}"
    
    Return your output strictly as a valid JSON object matching this schema:
    {{
      "entity_name": "extracted entity name",
      "document_type": "extracted document type",
      "pdf_query": "query string",
      "regulatory_query": "query string",
      "context_query": "query string"
    }}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        usage_tracker.add_usage("gemini-2.5-flash", response)
        data = json.loads(response.text.strip())
        return data
    except Exception as e:
        # Robust fallback if API fails
        import re
        entity = "InCred Holdings Limited"
        if "ola" in query.lower():
            entity = "Ola Electric"
        return {
            "entity_name": entity,
            "document_type": "DRHP",
            "pdf_query": f"{entity} DRHP filetype:pdf",
            "regulatory_query": f"{entity} DRHP site:sebi.gov.in",
            "context_query": f"{entity} IPO bottlenecks risks"
        }


def self_correct_json(client, invalid_json: str, error_message: str) -> str:
    """
    Spawns a fast, low-temperature gemini-2.5-flash correction call to repair
    syntactically invalid JSON outputted by the main synthesis model.
    """
    from google.genai import types
    prompt = f"""
    You are a high-speed JSON syntax correction specialist.
    The provided JSON block failed to parse with the following error:
    "{error_message}"
    
    Please analyze the JSON, repair any syntax errors (such as missing commas, unescaped quotes inside strings, unescaped control characters like newlines, trailing commas, or missing brackets), and output ONLY the clean, valid JSON block.
    Ensure that the exact structure, keys, values, and research content are completely preserved—only repair the syntax!
    
    === INVALID JSON ===
    {invalid_json}
    
    Output ONLY the raw repaired JSON string starting with '{{' and ending with '}}'. Do not include any explanation or markdown code blocks.
    """
    try:
        print("[*] Launching Auto-Self-Correction JSON Repair Loop...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        usage_tracker.add_usage("gemini-2.5-flash", response)
        return response.text.strip()
    except Exception as e:
        print(f"[-] Self-correction call failed: {str(e)}")
        return invalid_json


def load_local_knowledge_base() -> str:
    """
    Scans the dashboard folder for all past investigation subfolders,
    extracts their query subjects and anomalies, and compiles a shared
    knowledge base string to give cross-referencing capabilities to the model.
    """
    dashboard_dir = os.path.join(".", "dashboard")
    if not os.path.exists(dashboard_dir):
        return "No past investigations available."
        
    knowledge_records = []
    try:
        subdirs = [d for d in os.listdir(dashboard_dir) if os.path.isdir(os.path.join(dashboard_dir, d))]
        for s in subdirs:
            report_path = os.path.join(dashboard_dir, s, "forensic_report.json")
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                subject = data.get("subject", "Unknown Target")
                anomalies = data.get("anomalies", [])
                anom_summaries = []
                for a in anomalies[:3]:  # Top 3 anomalies to keep prompt concise
                    claim = a.get("source_claim", "")[:100]
                    reality = a.get("reality", "")[:120]
                    anom_summaries.append(f"  * Claim: '{claim}' -> Reality: '{reality}'")
                
                record = f"- Past Investigation on '{subject}':\n" + "\n".join(anom_summaries)
                knowledge_records.append(record)
    except Exception as e:
        return f"Error loading shared knowledge base: {str(e)}"
        
    if not knowledge_records:
        return "No past investigations available."
        
    return "\n\n".join(knowledge_records)


async def run_divergent_agent(client, model_name, persona_name, focus_instructions, corpus, query, usage_tracker):
    prompt = f"""
You are the specialized virtual agent '{persona_name}'. Your focus area is:
{focus_instructions}

Analyze the provided research corpus and deconstruct it to answer the user query through your specific investigative lens.
Identify key data points, variances, risks, opportunities, policy bottlenecks, or social outcomes.

=== CONSOLIDATED DEEP RESEARCH CORPUS ===
{corpus}

=== USER QUERY ===
{query}

=== INSTRUCTIONS ===
1. Draft a highly detailed, professional briefing memo summarizing your findings from your perspective.
2. Provide concrete metrics, numbers, and facts backed by references from the corpus.
3. Be highly objective, analytical, and critical.
4. Keep your response under 800 words.
"""
    try:
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        usage_tracker.add_usage(model_name, response)
        print(f"[+] Divergent Agent '{persona_name}' completed execution.")
        return f"=== PERSPECTIVE: {persona_name} ===\n{response.text.strip()}\n"
    except Exception as e:
        print(f"[-] Divergent Agent '{persona_name}' failed: {e}")
        return f"=== PERSPECTIVE: {persona_name} ===\nFailed to compile perspective: {e}\n"


async def heal_forensic_report_json(client, report_data: dict, query: str, divergent_briefs: str) -> dict:
    """
    Checks for missing or null essential keys in the compiled report data and
    sends a targeted, low-temperature prompt to Gemini 2.5 Flash to generate only
    the missing parts, merging them back to ensure the dashboard remains complete.
    """
    # Initialize tracks if missing
    tracks = report_data.setdefault("tracks", {})
    if not isinstance(tracks, dict):
        tracks = {}
        report_data["tracks"] = tracks
        
    missing_tracks = []
    for t in ["corporate", "policy", "sovereign"]:
        if t not in tracks or not tracks[t] or (isinstance(tracks[t], dict) and not tracks[t].get("text")):
            missing_tracks.append(t)
            
    missing_benchmarks = not report_data.get("strategic_benchmarks")
    missing_socio = not report_data.get("socioeconomic")
    missing_citations = not report_data.get("citations")
    
    if not (missing_tracks or missing_benchmarks or missing_socio or missing_citations):
        print("[+] Healer: No missing keys detected. Report is fully populated.")
        return report_data
        
    print(f"[*] Healer: Detected missing/null fields: tracks={missing_tracks}, benchmarks={missing_benchmarks}, socioeconomic={missing_socio}, citations={missing_citations}")
    
    # We will build a prompt requesting ONLY these missing fields
    schema_desc = []
    if missing_tracks:
        schema_desc.append(f"""
  "tracks": {{
    {", ".join([f'"{t}": {{ "text": "2-3 short bullet points (separated by newlines) detailing {t}-specific findings", "citations": [] }}' for t in missing_tracks])}
  }}""")
    if missing_benchmarks:
        schema_desc.append("""
  "strategic_benchmarks": [
    {
      "model_project": "Real-world competitor/peer project name",
      "what_they_did_well": "What they executed successfully with real numbers",
      "our_target_shortfall": "Where the target under investigation falls short",
      "strategic_learning": "Key warning or takeaway for investors/policymakers"
    }
  ]""")
    if missing_socio:
        schema_desc.append("""
  "socioeconomic": [
    {
      "area": "Specific impact vector (e.g. 'Labor & Gig Wages', 'Kirana Disruption', 'UPI Infrastructure')",
      "impact": "Detailed assessment of the structural changes with real numbers",
      "outcome": "Positive / Negative / Neutral / Mixed / Disruptive",
      "citations": []
    }
  ]""")
    if missing_citations:
        schema_desc.append("""
  "citations": [
    {
      "name": "Reference source name",
      "url": "Direct source link"
    }
  ]""")

    prompt_schema = ",\n".join(schema_desc)
    
    heal_prompt = f"""
You are the Forensic Data Healer. The main report synthesis missed some crucial fields due to parsing constraints.
You must analyze the query and the specialized briefs, and compile ONLY the missing fields requested below.

User Query: "{query}"

=== DIVERGENT AGENT PERSPECTIVES (CONTEXT) ===
{divergent_briefs[:25000]}

=== TARGET JSON SCHEMA FOR MISSING FIELDS ===
{{
{prompt_schema}
}}

Ensure all fields are fully populated with highly precise, realistic research details. Do not use generic placeholders.
Output ONLY the valid, minified or formatted JSON string starting with '{{' and ending with '}}'.
"""
    
    try:
        from google.genai import types
        print("[*] Dispatching Healer Agent to generate missing report sections...")
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=heal_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
                max_output_tokens=4000
            )
        )
        usage_tracker.add_usage("gemini-2.5-flash", response)
        healed_data = json.loads(response.text.strip())
        
        # Merge missing tracks back
        if "tracks" in healed_data:
            for t in missing_tracks:
                if t in healed_data["tracks"]:
                    report_data["tracks"][t] = healed_data["tracks"][t]
                    
        # Merge benchmarks
        if missing_benchmarks and "strategic_benchmarks" in healed_data:
            report_data["strategic_benchmarks"] = healed_data["strategic_benchmarks"]
            
        # Merge socioeconomic
        if missing_socio and "socioeconomic" in healed_data:
            report_data["socioeconomic"] = healed_data["socioeconomic"]
            
        # Merge citations
        if missing_citations and "citations" in healed_data:
            report_data["citations"] = healed_data["citations"]
            
        print("[+] Healer Agent successfully generated and merged missing fields!")
    except Exception as e:
        print(f"[-] Healer Agent failed: {str(e)}. Populating default fallbacks to prevent frontend crashes.")
        # Fallback to prevent crash
        for t in missing_tracks:
            report_data["tracks"][t] = {
                "text": f"No {t} data compiled for this research target.",
                "citations": []
            }
        if missing_benchmarks:
            report_data["strategic_benchmarks"] = []
        if missing_socio:
            report_data["socioeconomic"] = []
        if missing_citations:
            report_data["citations"] = []
            
    return report_data


# =====================================================================
# LOCAL REAL-TIME HARVESTER ENGINE (Windows Host)
# =====================================================================
async def run_local_mode(query: str):
    print("[*] Launching in Local REAL-TIME Harvester Mode (Windows Host)...")
    print(f"[*] Query: '{query}'")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("[-] Error: GEMINI_API_KEY environment variable is not set.")
        print("[*] Please set your Gemini key before running (e.g. $env:GEMINI_API_KEY='key').")
        sys.exit(1)
        
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        print("[-] Error: TAVILY_API_KEY environment variable is not set.")
        print("[*] Please set your Tavily key before running (e.g. $env:TAVILY_API_KEY='key').")
        sys.exit(1)
        
    # 1. Initialize modern google-genai Client
    from google import genai
    client = genai.Client(api_key=gemini_key)
    
    # Generate the archive slug early so it is globally available
    print("[*] Generating dynamic 3-word folder slug for research archive...")
    slug = generate_folder_slug(client, query)
    print(f"[+] Archive folder slug selected: '{slug}'")
    
    # Create archive folder early
    dashboard_dir = os.path.join(".", "dashboard")
    archive_dir = os.path.join(dashboard_dir, slug)
    os.makedirs(archive_dir, exist_ok=True)
    
    # 2. Gather Web Search Results
    print("[*] Phase 1: Querying web indices for relevant archives...")
    print("[*] Extracting entity and expanding search queries via Search Architect...")
    try:
        expanded = expand_search_queries(client, query)
        print(f"[+] Search Architect parsed Entity: '{expanded.get('entity_name')}' | Document: '{expanded.get('document_type')}'")
        
        search_queries = [
            ("PDF Direct", expanded.get("pdf_query")),
            ("Regulatory Archive", expanded.get("regulatory_query")),
            ("Context & Controversy", expanded.get("context_query"))
        ]
    except Exception as e:
        print(f"[-] Query expansion failed. Using raw query: {str(e)}")
        search_queries = [("Raw User Query", query)]
        
    all_results = []
    seen_urls = set()
    
    for label, q_str in search_queries:
        print(f"[*] Dispatching {label} search: '{q_str}'")
        try:
            res = deep_web_search(q_str, max_results=20)
            if isinstance(res, dict) and "results" in res:
                for item in res["results"]:
                    url = item.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        item["search_type"] = label
                        all_results.append(item)
        except Exception as e:
            print(f"[-] Search '{q_str}' failed: {str(e)}")
            
    print(f"[+] Completed search rounds. Discovered {len(all_results)} unique source URLs.")
    
    # 3. Intelligent Harvester Sorting & Priority Engine
    def get_url_priority(item):
        url = item.get("url", "").lower()
        search_type = item.get("search_type", "")
        
        score = 0
        if url.endswith(".pdf"):
            score += 100
        if "sebi.gov.in" in url:
            score += 90
        if search_type == "PDF Direct":
            score += 50
        if search_type == "Regulatory Archive":
            score += 40
        return score
        
    all_results.sort(key=get_url_priority, reverse=True)
    
    print("[*] Phase 2: Starting Deep Harvester Web Scraper (Body text extraction)...")
    harvester_corpus = []
    
    # Scrape all unique discovered resources for hyper-comprehensive research coverage
    max_urls = len(all_results)
    for idx in range(max_urls):
        item = all_results[idx]
        url = item.get("url", "")
        title = item.get("title", "Web Resource")
        
        if not url:
            continue
            
        print(f"[*] Scraper: Ingesting [{idx+1}/{max_urls}] -> {url} (Priority Score: {get_url_priority(item)})")
        
        if url.lower().endswith(".pdf"):
            content_text = extract_text_from_remote_pdf(url)
        else:
            content_text = scrape_webpage_content(url)
            
        if content_text and not content_text.startswith("Error"):
            # Apply semantic compression to reduce noise and save context window tokens
            compressed_content = semantic_compress_text(content_text, query)
            harvester_corpus.append(f"SOURCE URL: {url}\nTITLE: {title}\nCLEANED BODY:\n{compressed_content}\n" + "="*80 + "\n")
            print(f"[+] Successfully harvested {len(compressed_content)} compressed chars (original {len(content_text)} chars) from {title}")
        else:
            snippet = item.get("content", "")
            harvester_corpus.append(f"SOURCE URL: {url}\nTITLE: {title}\nCLEANED SNIPPET:\n{snippet}\n" + "="*80 + "\n")
            print(f"[-] Scrape failed. Retained standard snippet context.")
            
    # Compile the final high-fidelity research corpus (cap global budget at a comfortable 250,000 chars)
    consolidated_corpus = "\n".join(harvester_corpus)
    if len(consolidated_corpus) > 250000:
        consolidated_corpus = consolidated_corpus[:250000] + "\n... [GLOBAL CONTEXT TRUNCATED TO CAPPED TOKEN BUDGET] ...\n"
    print(f"[+] Harvester completed. Compiled {len(consolidated_corpus)} bytes of high-fidelity research text.")
    
    # 3.5. Run Divergent Agent Panel Concurrently (8 Agents)
    print("[*] Phase 2.8: Spawning 8 specialized virtual agents in parallel (Divergence Panel)...")
    agents_definitions = [
        ("Growth & Scale Analyst", "Growth & Scale Analyst (Growth Case): Customer acquisition rates, TAM expansion, transaction velocity, capital access, and scalability potential. Highlight positive growth indicators and UPI rails. Estimate Bass Diffusion parameters (innovation p, imitation q) and Power Law Alpha concentration exponent based on the quick commerce sector consolidations."),
        ("Unit Economics Auditor", "Unit Economics Auditor (Bear Case): Margins, cash burn, pricing markups, customer acquisition cost (CAC) inflation, and dark store unit leakages. Search for or estimate DuPont 5-Factor ROE variables, Sloan Ratio cash-accrual variables, and Beneish M-Score manipulation indicators (like gross margin, asset quality, leverage index). Execute Fermi TAM bounds checks compared to physical limits."),
        ("Macro & Sovereign Strategist", "Macro & Sovereign Strategist (Ecosystem Case): Intersection with national interests, UPI/Digital Public Infrastructure, foreign capital flows, and macroeconomic indicators."),
        ("Global Precedents Researcher", "Global Precedents Researcher (Comparative Case): Learnings and failures from global peers (e.g. Getir's European market exit, Gopuff's US valuation markdowns, Meituan's Chinese delivery margins)."),
        ("Labor & Human Capital Advocate", "Labor & Human Capital Advocate (Social Case): Gig worker rights, safety metrics, compensation models, labor exploitation, unions, and human resources pressure."),
        ("Legal, Compliance & Governance Counsel", "Legal, Compliance & Governance Counsel (Regulatory Case): Regulatory loopholes, antitrust/monopoly checks, DPDP data privacy compliance, auditing controls, and governance."),
        ("Tech & Logistics Architect", "Tech & Logistics Architect (Operational Case): Dark store layouts, predictive algorithms, routing efficiency, tech stack dependencies, and automation."),
        ("Environmental & Sustainability Auditor", "Environmental & Sustainability Auditor (Ecological Case): Carbon emissions, micro-fulfillment traffic gridlock, packaging waste, and noise/urban infrastructure strain.")
    ]
    
    tasks = []
    for name, focus in agents_definitions:
        tasks.append(
            run_divergent_agent(
                client=client,
                model_name="gemini-2.5-flash",
                persona_name=name,
                focus_instructions=focus,
                corpus=consolidated_corpus,
                query=query,
                usage_tracker=usage_tracker
            )
        )
    
    agent_briefs_list = await asyncio.gather(*tasks)
    divergent_briefs = "\n\n".join(agent_briefs_list)
    print(f"[+] Divergent panel execution completed. Generated {len(divergent_briefs)} characters of agent perspectives.")
    
    # 4. Load all domain skill instructions dynamically from .agents/skills/
    skill_content_parts = []
    skills_base_dir = os.path.join(".agents", "skills")
    if os.path.exists(skills_base_dir):
        try:
            for folder in os.listdir(skills_base_dir):
                folder_path = os.path.join(skills_base_dir, folder)
                if os.path.isdir(folder_path):
                    skill_md_path = os.path.join(folder_path, "SKILL.md")
                    if os.path.exists(skill_md_path):
                        with open(skill_md_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            skill_content_parts.append(f"=== SKILL: {folder} ===\n{content}\n")
        except Exception as e:
            print(f"[-] Error loading multiple skill files: {str(e)}")
    skill_content = "\n".join(skill_content_parts)
    if not skill_content:
        skill_content = "No dynamic skill content loaded."

    # 4b. Load past investigations knowledge base
    print("[*] Phase 2.5: Loading shared local knowledge base...")
    kb_context = load_local_knowledge_base()
    print(f"[+] Loaded shared knowledge base context ({len(kb_context)} bytes).")
    
    # Cache findings backlog immediately after divergent panel completes and KB is loaded
    print("[*] Phase 2.6: Caching raw research briefs and corpus to findings_backlog.json...")
    backlog_data = {
        "query": query,
        "divergent_briefs": divergent_briefs,
        "consolidated_corpus": consolidated_corpus,
        "skill_content": skill_content,
        "kb_context": kb_context
    }
    backlog_path = os.path.join(archive_dir, "findings_backlog.json")
    try:
        with open(backlog_path, "w", encoding="utf-8") as f:
            json.dump(backlog_data, f, indent=2, ensure_ascii=False)
        print(f"[+] Successfully cached findings backlog to: {backlog_path}")
    except Exception as e:
        print(f"[-] Failed to cache findings backlog: {str(e)}")
            
    # 5. Assemble Structured JSON Schema Prompts
    print("[*] Phase 3: Preparing Structured JSON Schema payloads...")
    
    prompt = f"""
You are the Moderator Agent. You must read the briefs compiled by the 8 specialized virtual agents who analyzed the query from conflicting viewpoints, resolve any contradictions or biases, and compile a cohesive converged draft JSON database matching the schema below.
Follow all instructions and rules specified in the Domain Skill and prompt details below.

=== 8 SPECIALIZED DIVERGENT AGENT PERSPECTIVE BRIEFS ===
{divergent_briefs}

=== LOCAL SHARED KNOWLEDGE BASE (CROSS-REFERENCE SOURCE) ===
{kb_context}

=== DOMAIN SKILL CONFIGURATION (SKILL.md) ===
{skill_content}

=== USER QUERY ===
{query}

=== CONSOLIDATED DEEP RESEARCH CORPUS (HARVESTED FROM THE WEB) ===
{consolidated_corpus}

=== CRITICAL READABILITY, QUANTITATIVE DENSITY & INVESTIGATIVE LENS INSTRUCTIONS ===
1. FIVE CORE INVESTIGATIVE LENSES: You must analyze the research corpus through five core investigative lenses:
   - Regulatory Loopholes & Grey Zones: Identify where technologies or practices outrace current regulatory frameworks, outdated laws, definitions being bypassed, or administrative grey zones.
   - Smuggling Pipelines & Transit Hubs: Map out physical and financial routing channels, transshipment hubs (e.g., Dubai, Hong Kong, Bangkok), misdeclaration methods, and grey supply chains.
   - Biosecurity, Espionage, & Trojan Horse Risks: Uncover software backdoors, data leakage to hostile servers, remote control/hijacking, biological pathogens from unregulated live germplasm, and border security/military vulnerabilities.
   - Livelihood vs. Centralized Power Tension: Detail the economic threat of foreign tech dumping or corporate centralization/monopolies squeezing out small-scale local operators, farmers, and local R&D startups.
   - Historical Warnings & Precedents: Stack historical precedents (contamination bans, past outbreaks, border conflicts) to demonstrate systemic vulnerability and show the trajectory of the threat.
2. CONCISE BULLETS: To make the output extremely punchy, readable, and memorable for the end user, DO NOT write long, dense paragraphs in the slide tracks ("corporate", "policy", "sovereign").
3. HIGH ACCESSIBILITY & CLEAR VOCABULARY:
   - Ensure the entire report is written in extremely clear, simple, and accessible English. Avoid overly complex, convoluted corporate speak or legal jargon.
   - Frame financial, macroeconomic, or operational complexities using easy-to-understand analogies and clear real-world references.
   - Keep sentences short, punchy, and clear, making it highly readable and accessible for casual readers while retaining absolute investigative depth.
4. Slide 1 (Teardown Editorial Verdict & Outlook) - "DECODING ECONOMIES" NEWSLETTER / ADITYA AGARWAL STYLE:
   - "editorial_verdict" MUST adopt the high-impact, analytical, warnings-driven tone of Aditya Agarwal's "Decoding Economies" newsletter.
   - Uncover shocking structural forces, macroeconomic policies, geostrategic alignment, capital flows, or hidden regulatory loopholes.
   - Frame the hook with deep intellectual weight, highlighting the stark contradiction between headline optics and the granular facts buried in the footnotes.
   - Do NOT write long, wordy paragraphs. Instead, use very short, punchy paragraphs (1-2 sentences max), double line breaks, and clear bullet points for core numbers.
   - REFERENCES: You MUST reference each and every data point or major assertion with a proper hyperlink right there on the first page itself!
     - Use internal slide links in the format `[Slide X](slide:X)` to link to the corresponding slide (e.g., `[Slide 3](slide:3)` for Slide 3 Anomalies, `[Slide 4](slide:4)` for Slide 4 Corporate, etc.) where the user can find in-depth details.
     - Use external source links in markdown format `[Source Name](URL)` pointing to the actual direct URL from the web search where the raw data is located.
     - Example text: "NCR ticket sizes surged to [₹3.31 Cr](slide:4) (up 231% per [CREDAI](https://...)) while affordable supply plummeted to [11%](slide:5) (per [ANAROCK](https://...))."
   - Weave in at least 5-6 concrete, real-world numerical metrics directly into this post.
5. Slide 2 (Forensic Trust Gap):
   - "forensic_trust_gap" MUST outline the difference between standard coverage and our deep forensic exposure.
   - Set standard coverage to what typical broker/media reports focus on, forensic exposure to the critical footnotes/discrepancies exposed by our pipeline, and the unique trust rationale to why this teardown cannot be replicated by standard sources (e.g. multi-track filing cross-examination, regulatory database audits).
5. Slide 3 (Anomaly Scanner) - TOP 3 ONLY:
   - Rank all discovered anomalies by impact and severity.
   - Select exactly the TOP 3 highest-severity anomalies to populate the main "anomalies" list.
   - For all remaining lower-ranked anomalies, populate the "backlog_anomalies" list with their titles and brief summaries.
   - Every single anomaly in "anomalies" MUST prove the counter-claim wrong by our main verdict.
   - Rebuild each anomaly item to contain:
     1. "source_claim": The public PR assertion / official narrative statement.
     2. "counter_claim": The standard counter-argument, justification, or defense raised by authority supporters/companies to protect the claim.
     3. "verdict": The final forensic verdict that quashes the counter-argument with hard evidence (Government data, regulatory reports, private studies) and proper numbers.
5. Slide 4, 5, 6 Tracks ("corporate", "policy", "sovereign"):
   - The "text" MUST be a list of exactly 2-3 highly precise, short bullet points separated by newlines, highlighting only the most critical corporate/policy/sovereign revelations and anomalies. Do not output wordy paragraphs!
6. Slide 7 (Strategic Benchmarks) - REAL-WORLD CASES ONLY:
   - Identify the core domain and target entity of the query. Conduct deep research on real-world, physical peer projects, companies, cities, or markets worldwide that share similar characteristics or serve as models/competitors.
   - Under no circumstances should you generate "conceptual", "theoretical", "general", or "ideal" benchmark models (do NOT output titles containing '(Conceptual)' or '(Theoretical)', or names like 'Balanced Urban Development'). Every benchmark project must be a real-world physical entity or city.
   - For example, if the query is about Delhi/NCR real estate, benchmark against the Mumbai Metropolitan Region (MMR) or Navi Mumbai CIDCO or Bengaluru IT corridors. If the query is about Jewar Airport, benchmark against Mopa Airport Goa or Heathrow Terminal 5. If it's about Ola Electric, benchmark against Tesla or BYD.
   - Compiles 2 high-density comparative benchmarks containing real numbers and comparisons to the target.

=== OUTPUT INSTRUCTION ===
You MUST return your entire output as a SINGLE, VALID JSON block. Do not wrap it in markdown code fences unless requested, but ensure the root element is a JSON object matching the exact structure below:


{{
  "subject": "The user query / topic under investigation",
  "social_share_post": {{
    "headlines": [
      "Headline Option 1 (Controversial/Skeptical - e.g. 'Is Zepto's 10-Minute Mirage Displacing Local Retail?')",
      "Headline Option 2 (Editorial/Macro - e.g. 'Decoding the Dark Store Economics of Indian Q-Commerce')",
      "Headline Option 3 (Question/Hook - e.g. 'Who actually pays the price for your 10-minute grocery delivery?')",
      "Headline Option 4 (Short/Direct - e.g. 'The True Cost of Instant Convenience')"
    ],
    "sections": {{
      "verdict": "The core newsletter verdict/editorial hook summary.",
      "metrics": "Key quantitative numbers and variance points.",
      "anomalies": "A bulleted breakdown of the key forensic anomalies uncovered.",
      "benchmarks": "Strategic takeaways and learning points from case studies.",
      "socioeconomic": "Major socioeconomic and India growth story impacts."
    }},
    "citations": [
      "Source Name/Link 1 (https://...)",
      "Source Name/Link 2 (https://...)"
    ]
  }},
  "india_growth_story": {{
    "title": "A short, engaging title deconstructing India's connection (e.g. Navigating the Hyper-Speed Delivery Squeeze)",
    "narrative": "A 2-3 paragraph detailed, accessible analysis of how India's growth ecosystem (e.g., UPI rails, digital infrastructure, DPDP regulations, labor policies, foreign venture capital) handles, absorbs, or suffers from this development. Highlight what India is doing differently/efficiently (policies, local investments) or what vulnerabilities it introduces.",
    "outlook": "Positive / Negative / Mixed / Disruptive"
  }},
  "forensic_case_study": {{
    "headline": "A bold, punchy, editorial headline summarizing the main investigative failure or irony (e.g. 'Authorities have made such a joke of new Jewar airport.')",
    "editorial_verdict": "First-person newsletter style narrative teardown (3-5 paragraphs, separated by double newlines, packed with numbers, outlining the surprise, the economics, and the outlook)",
    "side_by_side_comparison": {{
      "column_headers": {{
        "standard_label": "Label of comparison/baseline column (e.g., 'IGI Baseline' or 'MMR Avg' or 'US Cost')",
        "target_label": "Label of target column under investigation (e.g., 'Jewar Cost' or 'Delhi NCR Actual' or 'China Cost')"
      }},
      "rows": [
        {{
          "metric": "Line Item / Metric name (e.g. 6-hour parking for A321)",
          "standard_value": "Comparison/Standard value (e.g., IGI ₹6,900)",
          "target_value": "Target value (e.g., Jewar ₹14,500)",
          "mismatch_percentage": "Percentage mismatch (e.g., 110% higher)"
        }}
      ]
    }},
    "conclusion_question": "A punchy open-ended question to finish the case study editorial (e.g., 'What do you think?')"
  }},
  "forensic_trust_gap": {{
    "standard_sources_coverage": "What typical broker/media reports focus on",
    "our_forensic_exposure": "What this deep forensic teardown exposes (footprints/anomalies)",
    "unique_trust_rationale": "Evidence-backed rationale for why this analysis is uniquely trustworthy and hard to replicate"
  }},
  "executive_brief": "A 2-3 paragraph deep historical/geopolitical/corporate brief deconstructing the topic.",
  "executive_brief_citations": [
    {{"name": "Source Name (e.g. Forbes India)", "url": "Direct link from Tavily search"}}
  ],
  "anomalies": [
    {{
      "source_claim": "The public PR assertion / official narrative statement",
      "counter_claim": "The standard counter-argument, justification, or defense raised by authority supporters/companies to protect the claim",
      "verdict": "The final forensic verdict that quashes the counter-argument with hard evidence (Government data, regulatory reports, private studies) and proper numbers",
      "type": "Narrative / Mathematical / Financial / Geopolitical",
      "severity": "Low / Medium / High",
      "citations": [
        {{"name": "Source Name 1", "url": "Link 1"}},
        {{"name": "Source Name 2", "url": "Link 2"}}
      ]
    }}
  ],
  "backlog_anomalies": [
    {{
      "title": "Short descriptive title of the lower-ranked anomaly (e.g. Dark Store vehicle emissions)",
      "summary": "Brief 1-2 sentence description explaining the mismatch and evidence"
    }}
  ],
  "backlog_anomalies": [
    {{
      "title": "Short descriptive title of the lower-ranked anomaly (e.g. Dark Store vehicle emissions)",
      "summary": "Brief 1-2 sentence description explaining the mismatch and evidence"
    }}
  ],
  "tracks": {{
    "corporate": {{
      "text": "Detailed findings for Track 1: Corporate & Filing Fine Print (auditors, cap tables, hidden liabilities)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }},
    "policy": {{
      "text": "Detailed findings for Track 2 & 4: Policy Dynamics & Bottlenecks (schemes like Make in India, PLI, Swachh Bharat vs global benchmarks)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }},
    "sovereign": {{
      "text": "Detailed findings for Track 3: Sovereign & Geopolitical Alignment (capital flows, border alignments)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }}
  }},
  "socioeconomic": [
    {{
      "area": "Dynamic name of the macro-economic, societal, or industry impact vector (e.g., 'Employment Shift', 'Enterprise Margins', 'Foreign Capital Flows', 'Consumer Safety & Welfare') - identify 3 to 5 critical areas of impact",
      "impact": "Detailed assessment of the structural changes in this specific area, detailing who wins and who loses, packed with real numbers",
      "outcome": "Positive / Negative / Neutral / Mixed / Disruptive",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }}
  ],
  "strategic_benchmarks": [
    {{
      "model_project": "Name of successful similar project / competitor project (e.g. Mopa Airport, Goa)",
      "what_they_did_well": "Description of what they did successfully (e.g. Captured >40% state traffic share within year 1, optimized spatial planning)",
      "our_target_shortfall": "Where the current query entity falls short (e.g. Hindon's 0.1% traffic share warning, standalone airport layout)",
      "strategic_learning": "Actionable takeaway/strategic warning for investors or policy makers (e.g. Secondary airports must integrate transit early)"
    }}
  ],
  "citations": [
    {{
      "name": "Name of the reference/article",
      "url": "Direct source link"
    }}
  ],
  "quantitative_models": {{
    "beneish_m_score": {{
      "dsri": 1.0,
      "gmi": 1.0,
      "aqi": 1.0,
      "sgi": 1.0,
      "depi": 1.0,
      "sgai": 1.0,
      "lvgi": 1.0,
      "tata": 0.0
    }},
    "sloan_ratio": {{
      "net_income": 0.0,
      "operating_cash_flow": 0.0,
      "investing_cash_flow": 0.0,
      "total_assets": 1.0
    }},
    "dupont_5_factor": {{
      "tax_burden": 1.0,
      "interest_burden": 1.0,
      "operating_margin": 0.0,
      "asset_turnover": 0.0,
      "leverage": 1.0
    }},
    "kelly_criterion": {{
      "win_probability": 0.0,
      "win_loss_ratio": 0.0
    }},
    "fermi_tam_check": {{
      "reported_tam_usd": 0.0,
      "physical_limit_usd": 1.0
    }},
    "bass_diffusion": {{
      "p_innovation": 0.001,
      "q_imitation": 0.38
    }},
    "power_law_alpha": {{
      "market_shares": [0.0, 0.0]
    }},
    "evt_tail_risk": {{
      "cvar_95_percent": 0.0,
      "evt_99_percent_cvar": 0.0
    }}
  }}
}}
"""
    
    # 6. Call Multi-Agent Verification and Screening Loop
    print("[*] Phase 4: Launching Autonomous Multi-Agent Screening Loop...")
    
    # Enable JSON Mode in the config to guarantee valid JSON outputs
    from google.genai import types
    json_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.15,  # Low temperature for high-fidelity compliance
        max_output_tokens=8192
    )
    
    # ----------------------------------------------------
    # STAGE 1: DRAFT DATABASE GENERATION (Flash)
    # ----------------------------------------------------
    print("[*] Stage 1: Initiating Ingestion Agent (Drafting initial database via gemini-2.5-flash)...")
    draft_json_str = ""
    try:
        response_draft = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=json_config
        )
        usage_tracker.add_usage("gemini-2.5-flash", response_draft)
        draft_json_str = response_draft.text.strip()
        print("[+] Stage 1 completed successfully.")
    except Exception as e:
        print(f"[-] Stage 1 (Drafting) failed. Error: {str(e)}")
        sys.exit(1)
        
    # Convert Draft JSON to TOON format to save tokens in downstream prompts
    draft_toon_str = draft_json_str
    try:
        # import json (already imported globally)
        draft_json_data = json.loads(draft_json_str)
        draft_toon_str = convert_to_toon(draft_json_data)
        print("[+] Converted Stage 1 Draft JSON to TOON format to optimize tokens.")
    except Exception:
        pass
        
    # ----------------------------------------------------
    # STAGE 2: RED-TEAM AUDITING & CRITIQUE (Pro)
    # ----------------------------------------------------
    print("[*] Stage 2: Initiating Red-Team Auditor Agent (Ruthless cross-examination via gemini-2.5-pro)...")
    auditor_critique = ""
    auditor_prompt = f"""
You are the Red-Team Auditor and Validator. Your job is to perform a ruthless, highly skeptical audit of the Draft JSON database against the raw harvested text.

=== DRAFT DATABASE (TOON COMPACT FORMAT) ===
{draft_toon_str}

=== RAW HARVESTED TEXT CORPUS ===
{consolidated_corpus}

=== USER ORIGINAL QUERY ===
{query}

=== MISSION INSTRUCTION ===
Identify and document in detail:
1. Unbacked Claims: Any claim, anomaly, or outcome in the draft that is not strongly supported by the raw text.
2. Single-Source Bias: Claims that rely on a single source when multiple sources/perspectives exist in the raw corpus.
3. Missing Counter-Claims: Any explanations, defenses, or alternative viewpoints discussed in the raw text but omitted in the draft.
4. Factual Inaccuracies: Any misquoted numbers, incorrect percentages, or dates.

Format your output as a highly professional, structured AUDITOR CRITIQUE LOG detailing what needs to be refactored, corrected, or multi-sourced to make the findings 100% solid and unassailable.
"""
    try:
        response_audit = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=auditor_prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        usage_tracker.add_usage("gemini-2.5-pro", response_audit)
        auditor_critique = response_audit.text.strip()
        print("[+] Stage 2 completed successfully. Ruthless audit log generated.")
        print("-" * 50)
        try:
            print(auditor_critique[:1200] + "\n... [TRUNCATED DISPLAY] ...")
        except Exception:
            print(auditor_critique[:1200].encode('ascii', errors='replace').decode('ascii') + "\n... [TRUNCATED DISPLAY] ...")
        print("-" * 50)
    except Exception as e:
        print(f"[-] Stage 2 (Red-Teaming) failed or was skipped. Detail: {str(e)}")
        # Graceful fallback: if Pro fails due to quota/network, use Flash for red-teaming
        try:
            print("[*] Fallback: Retrying Stage 2 using gemini-2.5-flash...")
            response_audit = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=auditor_prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            usage_tracker.add_usage("gemini-2.5-flash", response_audit)
            auditor_critique = response_audit.text.strip()
            print("[+] Stage 2 fallback completed successfully.")
        except Exception as fallback_e:
            print(f"[-] Stage 2 fallback failed. Proceeding to Stage 3 with raw draft. Error: {fallback_e}")
            auditor_critique = "No auditor critique available."
            
    # ----------------------------------------------------
    # STAGE 3: FACT-HARDEN & BIAS REFINE ENGINE (Pro)
    # ----------------------------------------------------
    print("[*] Stage 3: Initiating Refiner & Debias Engine (Synthesis & Fact-Hardening via gemini-2.5-pro)...")
    refine_prompt = f"""
You are the Refiner and Debias Synthesis Engine. Your job is to take the Ingestion Draft JSON, the Red-Team Auditor's Critique, and the raw harvested corpus, and synthesize the final, unassailable, 100% verified, and balanced research report in the target JSON schema.

=== INGESTION DRAFT (TOON COMPACT FORMAT) ===
{draft_toon_str}

=== RED-TEAM AUDITOR CRITIQUE ===
{auditor_critique}

=== RAW HARVESTED TEXT CORPUS ===
{consolidated_corpus}

=== LOCAL SHARED KNOWLEDGE BASE (CROSS-REFERENCE SOURCE) ===
{kb_context}

=== USER ORIGINAL QUERY ===
{query}

=== TARGET SCHEMAS & REQUIREMENTS ===
1. Address every criticism in the Auditor's Critique.
2. Resolve any single-source bias by ensuring that every deconstructed anomaly has MULTIPLE backing sources/citations (at least 2 different sources/links where possible) directly in the "citations" list for that anomaly.
3. Integrate missing counter-claims and balance the narrative so that the final output is completely objective, factual, and backed by multiple citations.
4. Ensure every slide track ("corporate", "policy", "sovereign", "socioeconomic", "executive_brief") contains its own dedicated list of slide-specific citations.
5. Guarantee the final JSON is fully compliant with the target schema.

=== CRITICAL READABILITY, QUANTITATIVE DENSITY & INVESTIGATIVE LENS REQUIREMENTS ===
1. FIVE CORE INVESTIGATIVE LENSES: You must analyze the research corpus through five core investigative lenses:
   - Regulatory Loopholes & Grey Zones: Identify where technologies or practices outrace current regulatory frameworks, outdated laws, definitions being bypassed, or administrative grey zones.
   - Smuggling Pipelines & Transit Hubs: Map out physical and financial routing channels, transshipment hubs (e.g., Dubai, Hong Kong, Bangkok), misdeclaration methods, and grey supply chains.
   - Biosecurity, Espionage, & Trojan Horse Risks: Uncover software backdoors, data leakage to hostile servers, remote control/hijacking, biological pathogens from unregulated live germplasm, and border security/military vulnerabilities.
   - Livelihood vs. Centralized Power Tension: Detail the economic threat of foreign tech dumping or corporate centralization/monopolies squeezing out small-scale local operators, farmers, and local R&D startups.
   - Historical Warnings & Precedents: Stack historical precedents (contamination bans, past outbreaks, border conflicts) to demonstrate systemic vulnerability and show the trajectory of the threat.
2. HIGH ACCESSIBILITY & CLEAR VOCABULARY:
   - Ensure the entire report is written in extremely clear, simple, and accessible English. Avoid overly complex, convoluted corporate speak or legal jargon.
   - Frame financial, macroeconomic, or operational complexities using easy-to-understand analogies and clear real-world references.
   - Keep sentences short, punchy, and clear, making it highly readable and accessible for casual readers while retaining absolute investigative depth.
3. Slide 1 (Teardown Editorial Verdict & Outlook) - "DECODING ECONOMIES" NEWSLETTER / ADITYA AGARWAL STYLE:
   - "editorial_verdict" MUST adopt the high-impact, analytical, warnings-driven tone of Aditya Agarwal's "Decoding Economies" newsletter.
   - Uncover shocking structural forces, macroeconomic policies, geostrategic alignment, capital flows, or hidden regulatory loopholes.
   - Frame the hook with deep intellectual weight, highlighting the stark contradiction between headline optics and the granular facts buried in the footnotes.
   - Do NOT write long, wordy paragraphs. Instead, use very short, punchy paragraphs (1-2 sentences max), double line breaks, and clear bullet points for core numbers.
   - REFERENCES: You MUST reference each and every data point or major assertion with a proper hyperlink right there on the first page itself!
     - Use internal slide links in the format `[Slide X](slide:X)` to link to the corresponding slide (e.g., `[Slide 3](slide:3)` for Slide 3 Anomalies, `[Slide 4](slide:4)` for Slide 4 Corporate, etc.) where the user can find in-depth details.
     - Use external source links in markdown format `[Source Name](URL)` pointing to the actual direct URL from the web search where the raw data is located.
     - Example text: "NCR ticket sizes surged to [₹3.31 Cr](slide:4) (up 231% per [CREDAI](https://...)) while affordable supply plummeted to [11%](slide:5) (per [ANAROCK](https://...))."
   - Weave in at least 5-6 concrete, real-world numerical metrics directly into this post.
3. Slide 2 (Forensic Trust Gap):
   - "forensic_trust_gap" MUST outline the difference between standard coverage and our deep forensic exposure.
   - Set standard coverage to what typical broker/media reports focus on, forensic exposure to the critical footnotes/discrepancies exposed by our pipeline, and the unique trust rationale to why this teardown cannot be replicated by standard sources (e.g. multi-track filing cross-examination, regulatory database audits).
4. Slide 3 (Anomaly Scanner):
   - Every single anomaly in "anomalies" MUST prove the counter-claim wrong by our main verdict.
   - Rebuild each anomaly item to contain:
     1. "source_claim": The public PR assertion / official narrative statement.
     2. "counter_claim": The standard counter-argument, justification, or defense raised by authority supporters/companies.
     3. "verdict": The final forensic verdict that quashes the counter-argument with hard evidence (Government data, regulatory reports, private studies) and proper numbers.
5. Slide 4, 5, 6 Tracks ("corporate", "policy", "sovereign"):
   - The "text" MUST be a list of exactly 2-3 highly precise, short bullet points separated by newlines, highlighting only the most critical corporate/policy/sovereign revelations and anomalies. Do not output wordy paragraphs!
6. Slide 7 (Strategic Benchmarks) - REAL-WORLD CASES ONLY:
   - Identify the core domain and target entity of the query. Conduct deep research on real-world, physical peer projects, companies, cities, or markets worldwide that share similar characteristics or serve as models/competitors.
   - Under no circumstances should you generate "conceptual", "theoretical", "general", or "ideal" benchmark models (do NOT output titles containing '(Conceptual)' or '(Theoretical)', or names like 'Balanced Urban Development'). Every benchmark project must be a real-world physical entity or city.
   - For example, if the query is about Delhi/NCR real estate, benchmark against the Mumbai Metropolitan Region (MMR) or Navi Mumbai CIDCO or Bengaluru IT corridors. If the query is about Jewar Airport, benchmark against Mopa Airport Goa or Heathrow Terminal 5. If it's about Ola Electric, benchmark against Tesla or BYD.
   - Compiles 2 high-density comparative benchmarks containing real numbers and comparisons to the target.

You MUST return your entire output as a SINGLE, VALID JSON block. Do not wrap it in markdown code fences unless requested, but ensure the root element is a JSON object matching the exact structure below:


{{
  "subject": "The user query / topic under investigation",
  "social_share_post": {{
    "headlines": [
      "Headline Option 1 (Controversial/Skeptical - e.g. 'Is Zepto's 10-Minute Mirage Displacing Local Retail?')",
      "Headline Option 2 (Editorial/Macro - e.g. 'Decoding the Dark Store Economics of Indian Q-Commerce')",
      "Headline Option 3 (Question/Hook - e.g. 'Who actually pays the price for your 10-minute grocery delivery?')",
      "Headline Option 4 (Short/Direct - e.g. 'The True Cost of Instant Convenience')"
    ],
    "sections": {{
      "verdict": "The core newsletter verdict/editorial hook summary.",
      "metrics": "Key quantitative numbers and variance points.",
      "anomalies": "A bulleted breakdown of the key forensic anomalies uncovered.",
      "benchmarks": "Strategic takeaways and learning points from case studies.",
      "socioeconomic": "Major socioeconomic and India growth story impacts."
    }},
    "citations": [
      "Source Name/Link 1 (https://...)",
      "Source Name/Link 2 (https://...)"
    ]
  }},
  "india_growth_story": {{
    "title": "A short, engaging title deconstructing India's connection (e.g. Navigating the Hyper-Speed Delivery Squeeze)",
    "narrative": "A 2-3 paragraph detailed, accessible analysis of how India's growth ecosystem (e.g., UPI rails, digital infrastructure, DPDP regulations, labor policies, foreign venture capital) handles, absorbs, or suffers from this development. Highlight what India is doing differently/efficiently (policies, local investments) or what vulnerabilities it introduces.",
    "outlook": "Positive / Negative / Mixed / Disruptive"
  }},
  "forensic_case_study": {{
    "headline": "A bold, punchy, editorial headline summarizing the main investigative failure or irony (e.g. 'Authorities have made such a joke of new Jewar airport.')",
    "editorial_verdict": "First-person newsletter style narrative teardown (3-5 paragraphs, separated by double newlines, packed with numbers, outlining the surprise, the economics, and the outlook)",
    "side_by_side_comparison": {{
      "column_headers": {{
        "standard_label": "Label of comparison/baseline column (e.g., 'IGI Baseline' or 'MMR Avg' or 'US Cost')",
        "target_label": "Label of target column under investigation (e.g., 'Jewar Cost' or 'Delhi NCR Actual' or 'China Cost')"
      }},
      "rows": [
        {{
          "metric": "Line Item / Metric name (e.g. 6-hour parking for A321)",
          "standard_value": "Comparison/Standard value (e.g., IGI ₹6,900)",
          "target_value": "Target value (e.g., Jewar ₹14,500)",
          "mismatch_percentage": "Percentage mismatch (e.g., 110% higher)"
        }}
      ]
    }},
    "conclusion_question": "A punchy open-ended question to finish the case study editorial (e.g., 'What do you think?')"
  }},
  "forensic_trust_gap": {{
    "standard_sources_coverage": "What typical broker/media reports focus on",
    "our_forensic_exposure": "What this deep forensic teardown exposes (footprints/anomalies)",
    "unique_trust_rationale": "Evidence-backed rationale for why this analysis is uniquely trustworthy and hard to replicate"
  }},
  "executive_brief": "A 2-3 paragraph deep historical/geopolitical/corporate brief deconstructing the topic.",
  "executive_brief_citations": [
    {{"name": "Source Name (e.g. Forbes India)", "url": "Direct link from Tavily search"}}
  ],
  "anomalies": [
    {{
      "source_claim": "The public PR assertion / official narrative statement",
      "counter_claim": "The standard counter-argument, justification, or defense raised by authority supporters/companies to protect the claim",
      "verdict": "The final forensic verdict that quashes the counter-argument with hard evidence (Government data, regulatory reports, private studies) and proper numbers",
      "type": "Narrative / Mathematical / Financial / Geopolitical",
      "severity": "Low / Medium / High",
      "citations": [
        {{"name": "Source Name 1", "url": "Link 1"}},
        {{"name": "Source Name 2", "url": "Link 2"}}
      ]
    }}
  ],
  "backlog_anomalies": [
    {{
      "title": "Short descriptive title of the lower-ranked anomaly (e.g. Dark Store vehicle emissions)",
      "summary": "Brief 1-2 sentence description explaining the mismatch and evidence"
    }}
  ],
  "tracks": {{
    "corporate": {{
      "text": "Detailed findings for Track 1: Corporate & Filing Fine Print (auditors, cap tables, hidden liabilities)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }},
    "policy": {{
      "text": "Detailed findings for Track 2 & 4: Policy Dynamics & Bottlenecks (schemes like Make in India, PLI, Swachh Bharat vs global benchmarks)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }},
    "sovereign": {{
      "text": "Detailed findings for Track 3: Sovereign & Geopolitical Alignment (capital flows, border alignments)",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }}
  }},
  "socioeconomic": [
    {{
      "area": "Dynamic name of the macro-economic, societal, or industry impact vector (e.g., 'Employment Shift', 'Enterprise Margins', 'Foreign Capital Flows', 'Consumer Safety & Welfare') - identify 3 to 5 critical areas of impact",
      "impact": "Detailed assessment of the structural changes in this specific area, detailing who wins and who loses, packed with real numbers",
      "outcome": "Positive / Negative / Neutral / Mixed / Disruptive",
      "citations": [
        {{"name": "Source Name", "url": "Link"}}
      ]
    }}
  ],
  "strategic_benchmarks": [
    {{
      "model_project": "Name of successful similar project / competitor project (e.g. Mopa Airport, Goa)",
      "what_they_did_well": "Description of what they did successfully (e.g. Captured >40% state traffic share within year 1, optimized spatial planning)",
      "our_target_shortfall": "Where the current query entity falls short (e.g. Hindon's 0.1% traffic share warning, standalone airport layout)",
      "strategic_learning": "Actionable takeaway/strategic warning for investors or policy makers (e.g. Secondary airports must integrate transit early)"
    }}
  ],
  "citations": [
    {{
      "name": "Name of the reference/article",
      "url": "Direct source link"
    }}
  ],
  "quantitative_models": {{
    "beneish_m_score": {{
      "dsri": 1.0,
      "gmi": 1.0,
      "aqi": 1.0,
      "sgi": 1.0,
      "depi": 1.0,
      "sgai": 1.0,
      "lvgi": 1.0,
      "tata": 0.0
    }},
    "sloan_ratio": {{
      "net_income": 0.0,
      "operating_cash_flow": 0.0,
      "investing_cash_flow": 0.0,
      "total_assets": 1.0
    }},
    "dupont_5_factor": {{
      "tax_burden": 1.0,
      "interest_burden": 1.0,
      "operating_margin": 0.0,
      "asset_turnover": 0.0,
      "leverage": 1.0
    }},
    "kelly_criterion": {{
      "win_probability": 0.0,
      "win_loss_ratio": 0.0
    }},
    "fermi_tam_check": {{
      "reported_tam_usd": 0.0,
      "physical_limit_usd": 1.0
    }},
    "bass_diffusion": {{
      "p_innovation": 0.001,
      "q_imitation": 0.38
    }},
    "power_law_alpha": {{
      "market_shares": [0.0, 0.0]
    }},
    "evt_tail_risk": {{
      "cvar_95_percent": 0.0,
      "evt_99_percent_cvar": 0.0
    }}
  }}
}}

Ensure all fields are fully populated. Do not return empty fields or placeholders. Output only the raw, minified or formatted JSON string starting with '{' and ending with '}'.
"""
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=refine_prompt,
            config=json_config
        )
        usage_tracker.add_usage("gemini-2.5-pro", response)
        print("[+] Stage 3 completed successfully using: gemini-2.5-pro")
    except Exception as e:
        print(f"[-] Stage 3 (Refining) failed under gemini-2.5-pro. Error: {str(e)}")
        # Fallback to gemini-2.5-flash
        try:
            print("[*] Fallback: Retrying Stage 3 using gemini-2.5-flash...")
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=refine_prompt,
                config=json_config
            )
            usage_tracker.add_usage("gemini-2.5-flash", response)
            print("[+] Stage 3 fallback completed successfully using: gemini-2.5-flash")
        except Exception as fallback_e:
            print(f"[-] Stage 3 fallback failed. Error: {fallback_e}")
            sys.exit(1)
            
    if response:
        try:
            json_text = response.text.strip()
            # If the response text has markdown code blocks, strip them
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            json_text = json_text.strip()
            
            # Verify valid JSON
            report_data = json.loads(json_text)
            report_data = await heal_forensic_report_json(client, report_data, query, divergent_briefs)
            report_data = process_quantitative_models(report_data)
            report_data["usage_stats"] = usage_tracker.get_stats()
            # Programmatically reconstruct the markdown report in Python to save output tokens
            report_data["markdown_report"] = reconstruct_markdown_report(report_data)
            
            # 7. Write Structured JSON to the Dashboard folder
            dashboard_dir = os.path.join(".", "dashboard")
            os.makedirs(dashboard_dir, exist_ok=True)
            
            print(f"[+] Reusing early generated archive folder: '{archive_dir}'")
            
            # Paths to write JSON and JS to both root and archive folder
            json_paths = [
                os.path.join(dashboard_dir, "forensic_report.json"),
                os.path.join(archive_dir, "forensic_report.json")
            ]
            js_paths = [
                os.path.join(dashboard_dir, "forensic_data.js"),
                os.path.join(archive_dir, "forensic_data.js")
            ]
            
            # Write JSON files
            for json_path in json_paths:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            # Update findings_backlog.json with generated backlog_anomalies
            backlog_data["backlog_anomalies"] = report_data.get("backlog_anomalies", [])
            try:
                with open(backlog_path, "w", encoding="utf-8") as f:
                    json.dump(backlog_data, f, indent=2, ensure_ascii=False)
                print(f"[+] Updated findings backlog with backlog_anomalies.")
            except Exception as e:
                print(f"[-] Failed to update findings backlog: {str(e)}")
            print(f"[+] Saved structured slide deck JSON to: {json_paths[0]}")
            print(f"[+] Saved structured slide deck JSON to archive: {json_paths[1]}")
            
            # Write duplicate JS payloads
            for js_path in js_paths:
                with open(js_path, "w", encoding="utf-8") as f:
                    f.write(f"window.forensicReportData = {json.dumps(report_data, indent=2, ensure_ascii=False)};")
            print(f"[+] Saved structured slide deck JS payload to: {js_paths[0]}")
            print(f"[+] Saved structured slide deck JS payload to archive: {js_paths[1]}")
            
            # Copy dynamic UI template files (index.html, style_v2.css, app.js) to the archive folder
            import shutil
            for filename in ["index.html", "style_v2.css", "app.js"]:
                src_file = os.path.join(dashboard_dir, filename)
                dest_file = os.path.join(archive_dir, filename)
                if os.path.exists(src_file):
                    shutil.copy2(src_file, dest_file)
            print(f"[+] Copied UI template files to archive folder.")
            
            # Get absolute URL for easy vetting clicking in local host console
            abs_index_path = os.path.abspath(os.path.join(archive_dir, "index.html"))
            vetting_url = f"file:///{abs_index_path.replace(os.sep, '/')}"
            
            # 8. Write Markdown report to standard app data folder
            output_dir = r"C:\Users\Aditya\.gemini\antigravity\brain\4c0fa76b-dbaf-4919-a30a-dd50e654dca9"
            os.makedirs(output_dir, exist_ok=True)
            report_path = os.path.join(output_dir, "forensic_briefing_report.md")
            
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_data.get("markdown_report", "# Forensic Intelligence Report\nError generating markdown content."))
            print(f"[+] Saved standard briefing markdown to: {report_path}")
            
            print("\n" + "="*60)
            print("   REAL-TIME RESEARCH HARVEST COMPLETE   ")
            print(f"   Dashboard files ready in: {dashboard_dir}")
            print(f"   Archive folder compiled:  {archive_dir}")
            print(f"   VETTING ARCHIVE URL:      {vetting_url}")
            print("="*60)

            # Unified Pipeline: Automatically trigger the Deep-Dive slide generation for the first backlog anomaly
            if report_data.get("backlog_anomalies"):
                print("\n[*] Automatically triggering Deep-Dive slide generation for the first backlog anomaly...")
                await run_deep_dive_mode(0)
            try:
                print(report_data.get("executive_brief", "")[:800] + "\n... [TRUNCATED DISPLAY] ...")
            except Exception:
                # Fallback print if console still rejects unicode character maps
                brief = report_data.get("executive_brief", "")[:800]
                print(brief.encode('ascii', errors='replace').decode('ascii') + "\n... [TRUNCATED DISPLAY] ...")
            print("="*60)
            
        except Exception as json_err:
            print(f"[-] Failed to parse returned JSON: {str(json_err)}")
            # Trigger dynamic self-correction loop
            try:
                repaired_json = self_correct_json(client, json_text, str(json_err))
                if repaired_json.startswith("```json"):
                    repaired_json = repaired_json[7:]
                if repaired_json.endswith("```"):
                    repaired_json = repaired_json[:-3]
                repaired_json = repaired_json.strip()
                
                report_data = json.loads(repaired_json)
                report_data = await heal_forensic_report_json(client, report_data, query, divergent_briefs)
                report_data = process_quantitative_models(report_data)
                report_data["usage_stats"] = usage_tracker.get_stats()
                # Programmatically reconstruct the markdown report in Python to save output tokens
                report_data["markdown_report"] = reconstruct_markdown_report(report_data)
                print("[+] Self-Correction Loop successful! Repaired JSON parsed successfully.")
                
                # Write to files as normal
                dashboard_dir = os.path.join(".", "dashboard")
                os.makedirs(dashboard_dir, exist_ok=True)
                
                print(f"[+] Reusing early generated archive folder: '{archive_dir}'")
                
                json_paths = [
                    os.path.join(dashboard_dir, "forensic_report.json"),
                    os.path.join(archive_dir, "forensic_report.json")
                ]
                js_paths = [
                    os.path.join(dashboard_dir, "forensic_data.js"),
                    os.path.join(archive_dir, "forensic_data.js")
                ]
                
                for json_path in json_paths:
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(report_data, f, indent=2, ensure_ascii=False)
                
                # Update findings_backlog.json with generated backlog_anomalies
                backlog_data["backlog_anomalies"] = report_data.get("backlog_anomalies", [])
                try:
                    with open(backlog_path, "w", encoding="utf-8") as f:
                        json.dump(backlog_data, f, indent=2, ensure_ascii=False)
                    print(f"[+] Updated findings backlog with backlog_anomalies in repair block.")
                except Exception as e:
                    print(f"[-] Failed to update findings backlog in repair block: {str(e)}")
                print(f"[+] Saved structured slide deck JSON to: {json_paths[0]}")
                print(f"[+] Saved structured slide deck JSON to archive: {json_paths[1]}")
                
                for js_path in js_paths:
                    with open(js_path, "w", encoding="utf-8") as f:
                        f.write(f"window.forensicReportData = {json.dumps(report_data, indent=2, ensure_ascii=False)};")
                print(f"[+] Saved structured slide deck JS payload to: {js_paths[0]}")
                print(f"[+] Saved structured slide deck JS payload to archive: {js_paths[1]}")
                
                import shutil
                for filename in ["index.html", "style_v2.css", "app.js"]:
                    src_file = os.path.join(dashboard_dir, filename)
                    dest_file = os.path.join(archive_dir, filename)
                    if os.path.exists(src_file):
                        shutil.copy2(src_file, dest_file)
                print(f"[+] Copied UI template files to archive folder.")
                
                abs_index_path = os.path.abspath(os.path.join(archive_dir, "index.html"))
                vetting_url = f"file:///{abs_index_path.replace(os.sep, '/')}"
                
                output_dir = r"C:\Users\Aditya\.gemini\antigravity\brain\4c0fa76b-dbaf-4919-a30a-dd50e654dca9"
                os.makedirs(output_dir, exist_ok=True)
                report_path = os.path.join(output_dir, "forensic_briefing_report.md")
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report_data.get("markdown_report", "# Forensic Intelligence Report\nError generating markdown content."))
                print(f"[+] Saved standard briefing markdown to: {report_path}")
                
                print("\n" + "="*60)
                print("   REAL-TIME RESEARCH HARVEST COMPLETE   ")
                print(f"   Dashboard files ready in: {dashboard_dir}")
                print(f"   Archive folder compiled:  {archive_dir}")
                print(f"   VETTING ARCHIVE URL:      {vetting_url}")
                print("="*60)

                # Unified Pipeline: Automatically trigger the Deep-Dive slide generation for the first backlog anomaly
                if report_data.get("backlog_anomalies"):
                    print("\n[*] Automatically triggering Deep-Dive slide generation for the first backlog anomaly in repair block...")
                    await run_deep_dive_mode(0)
                try:
                    print(report_data.get("executive_brief", "")[:800] + "\n... [TRUNCATED DISPLAY] ...")
                except Exception:
                    brief = report_data.get("executive_brief", "")[:800]
                    print(brief.encode('ascii', errors='replace').decode('ascii') + "\n... [TRUNCATED DISPLAY] ...")
                print("="*60)
                
            except Exception as repair_err:
                print(f"[-] JSON self-correction failed: {str(repair_err)}")
                print("Raw text returned:")
                try:
                    print(response.text[:2000])
                except Exception:
                    print(response.text[:2000].encode('ascii', errors='replace').decode('ascii'))
    else:
        print("\n" + "!"*60)
        print("[-] FATAL: All model attempts in fallback chain failed.")
        print("Details:")
        for err in errors:
            print(f"  * {err}")
        print("!"*60)


# =====================================================================

def find_latest_archive_dir() -> str:
    """
    Scans the dashboard directory for subfolders containing findings_backlog.json.
    Returns the absolute path to the directory with the most recently modified backlog.
    """
    dashboard_dir = os.path.join(".", "dashboard")
    if not os.path.exists(dashboard_dir):
        return None
    subdirs = []
    for d in os.listdir(dashboard_dir):
        p = os.path.join(dashboard_dir, d)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "findings_backlog.json")):
            subdirs.append(p)
    if not subdirs:
        return None
    # Sort by modification time of findings_backlog.json
    subdirs.sort(key=lambda x: os.path.getmtime(os.path.join(x, "findings_backlog.json")), reverse=True)
    return os.path.abspath(subdirs[0])


async def run_deep_dive_mode(index: int):
    """
    Reads the cached backlog and forensic report from the latest run,
    identifies the lower-ranked anomaly at <index>, uses gemini-2.5-pro to generate
    a deep-dive slide payload, merges it, and regenerates outputs.
    """
    print(f"[*] Launching in Deep-Dive Mode for anomaly index {index}...")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("[-] Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    archive_dir = find_latest_archive_dir()
    if not archive_dir:
        print("[-] Error: No active research archives with findings_backlog.json found under dashboard/.")
        sys.exit(1)
        
    print(f"[+] Found latest research archive directory: '{archive_dir}'")
    
    # Load findings_backlog.json
    backlog_path = os.path.join(archive_dir, "findings_backlog.json")
    try:
        with open(backlog_path, "r", encoding="utf-8") as f:
            backlog = json.load(f)
    except Exception as e:
        print(f"[-] Error loading backlog: {str(e)}")
        sys.exit(1)
        
    # Load forensic_report.json
    report_path = os.path.join(archive_dir, "forensic_report.json")
    if not os.path.exists(report_path):
        print(f"[-] Error: forensic_report.json not found in '{archive_dir}'")
        sys.exit(1)
        
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
    except Exception as e:
        print(f"[-] Error loading forensic report: {str(e)}")
        sys.exit(1)
        
    backlog_anomalies = report_data.get("backlog_anomalies", [])
    if not backlog_anomalies:
        print("[-] Error: No backlog_anomalies found in the forensic report.")
        sys.exit(1)
        
    if index < 0 or index >= len(backlog_anomalies):
        print(f"[-] Error: Deep dive index {index} is out of bounds. Available backlog anomalies: {len(backlog_anomalies)}")
        for idx, item in enumerate(backlog_anomalies):
            print(f"  [{idx}]: {item.get('title')}")
        sys.exit(1)
        
    target_anomaly = backlog_anomalies[index]
    print(f"[+] Target Anomaly selected: '{target_anomaly.get('title')}'")
    print(f"    Summary: {target_anomaly.get('summary')}")
    
    # Initialize modern google-genai Client
    from google import genai
    client = genai.Client(api_key=gemini_key)
    
    usage_tracker = APIUsageTracker()
    
    query = backlog.get("query")
    consolidated_corpus = backlog.get("consolidated_corpus")
    kb_context = backlog.get("kb_context")
    divergent_briefs = backlog.get("divergent_briefs")
    skill_content = backlog.get("skill_content")
    
    deep_dive_prompt = f"""
You are the Refiner and Deep-Dive Investigation Engine.
Your job is to read the consolidated research corpus, the local knowledge base, the specialized agent briefs, and the skill configurations, and generate an in-depth deep-dive slide analyzing a specific backlog anomaly that was previously left out of the main report due to context size limitations.

=== TARGET ANOMALY UNDER INVESTIGATION ===
Title: {target_anomaly.get('title')}
Summary: {target_anomaly.get('summary')}

=== ORIGINAL USER QUERY ===
{query}

=== 8 SPECIALIZED DIVERGENT AGENT PERSPECTIVE BRIEFS ===
{divergent_briefs}

=== LOCAL SHARED KNOWLEDGE BASE ===
{kb_context}

=== DOMAIN SKILL CONFIGURATION (SKILL.md) ===
{skill_content}

=== CONSOLIDATED DEEP RESEARCH CORPUS ===
{consolidated_corpus}

=== DEEP-DIVE SLIDE REQUIREMENTS ===
1. Analyze this anomaly in deep detail. The narrative must explain the mismatch between the official claim and reality, back it with hard numbers from the corpus, and detail the implications.
2. Tone: Skeptical, objective, high-impact financial forensics (newsletter style).
3. Frame the analysis in extremely clear, simple, and accessible English. Avoid complex legal jargon.
4. References: You must include at least 1-2 external source citations with direct URLs from the corpus. Also, cross-reference standard slides using [Slide X](slide:X) if relevant.
5. Metrics: Provide 2 to 4 key deep-dive metrics (label and value) to render in the sidebar.

=== OUTPUT INSTRUCTION ===
Return your entire output as a SINGLE, VALID JSON block. Output only the raw, minified or formatted JSON string starting with '{{{{' and ending with '}}}}' matching the schema below:

{{{{
  "deep_dive": {{{{
    "title": "Title of the deep dive anomaly",
    "narrative": "Detailed narrative paragraphs separated by newlines, explaining the anomaly and findings in depth.",
    "metrics": [
      {{{{
        "label": "Metric Name",
        "value": "Metric Value (e.g. 110% higher or ₹15,000 Cr)"
      }}}}
    ],
    "citations": [
      {{{{
        "name": "Source Name / Link",
        "url": "https://..."
      }}}}
    ]
  }}}}
}}}}
"""

    print("[*] Dispatching gemini-2.5-pro to generate deep-dive investigation slide...")
    from google.genai import types
    json_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.15,
        max_output_tokens=8192
    )
    
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=deep_dive_prompt,
            config=json_config
        )
        usage_tracker.add_usage("gemini-2.5-pro", response)
        print("[+] Deep-dive generation completed successfully.")
    except Exception as e:
        print(f"[-] Error calling Gemini Pro for deep dive: {str(e)}")
        sys.exit(1)
        
    json_text = response.text.strip()
    if json_text.startswith("```json"):
        json_text = json_text[7:]
    if json_text.endswith("```"):
        json_text = json_text[:-3]
    json_text = json_text.strip()
    
    try:
        deep_dive_data = json.loads(json_text)
    except Exception as e:
        print(f"[-] Failed to parse returned JSON: {str(e)}")
        print("Raw text returned:")
        print(json_text)
        sys.exit(1)
        
    # Merge into report_data
    report_data["deep_dive"] = deep_dive_data.get("deep_dive")
    
    # Merge existing usage stats
    old_stats = report_data.get("usage_stats", {})
    new_stats = usage_tracker.get_stats()
    
    merged_stats = {}
    merged_stats["total_cost_inr"] = old_stats.get("total_cost_inr", 0.0) + new_stats.get("total_cost_inr", 0.0)
    merged_stats["tokens"] = {}
    for model in set(list(old_stats.get("tokens", {}).keys()) + list(new_stats.get("tokens", {}).keys())):
        merged_stats["tokens"][model] = {
            "prompt_tokens": old_stats.get("tokens", {}).get(model, {}).get("prompt_tokens", 0) + new_stats.get("tokens", {}).get(model, {}).get("prompt_tokens", 0),
            "candidates_tokens": old_stats.get("tokens", {}).get(model, {}).get("candidates_tokens", 0) + new_stats.get("tokens", {}).get(model, {}).get("candidates_tokens", 0)
        }
    report_data["usage_stats"] = merged_stats
    
    # Regenerate markdown report
    report_data["markdown_report"] = reconstruct_markdown_report(report_data)
    
    # Paths to write JSON and JS to both root and archive folder
    dashboard_dir = os.path.join(".", "dashboard")
    json_paths = [
        os.path.join(dashboard_dir, "forensic_report.json"),
        os.path.join(archive_dir, "forensic_report.json")
    ]
    js_paths = [
        os.path.join(dashboard_dir, "forensic_data.js"),
        os.path.join(archive_dir, "forensic_data.js")
    ]
    
    # Write JSON files
    for json_path in json_paths:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved updated slide deck JSON to: {json_paths[0]}")
    
    # Write duplicate JS payloads
    for js_path in js_paths:
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(f"window.forensicReportData = {json.dumps(report_data, indent=2, ensure_ascii=False)};")
    print(f"[+] Saved updated slide deck JS payload to: {js_paths[0]}")
    
    # Write markdown report
    output_dir = "C:/Users/Aditya/.gemini/antigravity/brain/4c0fa76b-dbaf-4919-a30a-dd50e654dca9"
    report_markdown_path = os.path.join(output_dir, "forensic_briefing_report.md")
    with open(report_markdown_path, "w", encoding="utf-8") as f:
        f.write(report_data["markdown_report"])
    print(f"[+] Saved updated briefing markdown to: {report_markdown_path}")
    
    abs_index_path = os.path.abspath(os.path.join(archive_dir, "index.html"))
    vetting_url = f"file:///{abs_index_path.replace(os.sep, '/')}"
    
    print("\n" + "="*60)
    print("   DEEP INVESTIGATION SLIDE PAGING COMPLETE   ")
    print(f"   Dashboard updated in: {dashboard_dir}")
    print(f"   Archive updated in:   {archive_dir}")
    print(f"   VETTING ARCHIVE URL:      {vetting_url}")
    print("="*60)


# =====================================================================
# =====================================================================
if __name__ == "__main__":
    default_query = (
        "Audit the bottlenecks in the Make in India initiative for the semiconductor sector "
        "compared to Taiwan's ecosystem, and outline how it impacts domestic manufacturing jobs and consumers."
    )
    
    import sys
    import asyncio
    
    if len(sys.argv) > 1 and sys.argv[1] == "--deep-dive":
        try:
            deep_dive_index = int(sys.argv[2])
        except (IndexError, ValueError):
            print("[-] Error: --deep-dive requires an integer index (e.g., --deep-dive 0)")
            sys.exit(1)
        asyncio.run(run_deep_dive_mode(deep_dive_index))
    else:
        query_str = sys.argv[1] if len(sys.argv) > 1 else default_query
        if HAS_SDK:
            asyncio.run(run_sdk_mode(query_str))
        else:
            asyncio.run(run_local_mode(query_str))
