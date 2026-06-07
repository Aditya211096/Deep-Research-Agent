// State Variables for Slide Deck Navigation
let currentSlideIndex = 0;
let totalSlides = 10;
let reportData = null;

// UI Element References
const slideWindow = document.getElementById("slideWindow");
const btnPrev = document.getElementById("btnPrev");
const btnNext = document.getElementById("btnNext");
const currentSlideNum = document.getElementById("currentSlideNum");
const totalSlidesNum = document.getElementById("totalSlidesNum");
const progressBar = document.getElementById("progressBar");
const anomalyList = document.getElementById("anomalyList");

// =====================================================================
// DATA LOADING LAYER
// =====================================================================
async function loadForensicData() {
    try {
        // 1. First check if forensic data was loaded globally via script tag (bypasses CORS restrictions on file://)
        if (window.forensicReportData) {
            reportData = window.forensicReportData;
        } else {
            // Fallback to fetch API if running on a local or remote web server
            const response = await fetch("forensic_report.json");
            if (!response.ok) {
                throw new Error("Report database file not found.");
            }
            reportData = await response.json();
        }
        
        if (reportData.deep_dive) {
            totalSlides = 11;
        } else {
            totalSlides = 10;
        }
        totalSlidesNum.textContent = totalSlides;
        
        // 2. Render the active slide index
        renderSlide(currentSlideIndex);
        
        // 3. Populate the Automated Anomaly Scanner Sidebar
        populateAnomalySidebar();
        
        // 3b. Update Live Pricing HUD in footer
        updateFooterHud();
        
        // 4. Update linear glow progress bar and controls
        updateDeckControls();
        
    } catch (err) {
        renderSetupInstructions();
    }
}

function updateFooterHud() {
    if (!reportData) return;
    const stats = reportData.usage_stats;
    const footerHud = document.getElementById("footerHud");
    if (footerHud) {
        if (stats && stats.total_cost_inr > 0) {
            footerHud.innerHTML = `&bull; TOTAL COST: ₹${stats.total_cost_inr.toFixed(3)} INR (${(stats.total_tokens / 1000).toFixed(1)}k tokens)`;
        } else {
            footerHud.innerHTML = `&bull; TOTAL COST: ₹0.000 INR (N/A / cached)`;
        }
    }
}

// =====================================================================
// DYNAMIC SLIDE RENDERING
// =====================================================================
function renderSlide(index) {
    if (!reportData) return;
    
    let html = "";
    
    switch(index) {
        case 0: // Slide 0: Forensic Case Study (Teardown Editorial Verdict & Outlook)
            {
                const caseStudy = reportData.forensic_case_study || {
                    headline: "Filing Forensic Case Study Under Review",
                    editorial_verdict: "No editorial verdict compiled.",
                    side_by_side_comparison: { rows: [] },
                    conclusion_question: "No conclusion question parsed."
                };
                
                // Support both array and object formats for side_by_side_comparison
                const isObjectFormat = caseStudy.side_by_side_comparison && !Array.isArray(caseStudy.side_by_side_comparison);
                const compareRows = isObjectFormat ? (caseStudy.side_by_side_comparison.rows || []) : (caseStudy.side_by_side_comparison || []);
                const headers = isObjectFormat ? (caseStudy.side_by_side_comparison.column_headers || {}) : {};
                
                html = `
                    <div class="slide-content-block">
                        <div class="newsletter-masthead">
                            <span class="masthead-tag">DECODING ECONOMIES</span>
                            <h1 class="newsletter-title">${highlightFinancialFigures(caseStudy.headline)}</h1>
                            <div class="newsletter-meta">
                                <span class="meta-author">By Aditya Agarwal</span> &bull; 
                                <span class="meta-date">${new Date().toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'})}</span> &bull; 
                                <span class="meta-network">Zero1 Writers Network</span>
                            </div>
                        </div>
                        <div class="case-study-grid">
                            <div class="case-study-left-pane">
                                <div class="editorial-verdict-card">
                                    ${formatEditorialVerdict(highlightFinancialFigures(caseStudy.editorial_verdict))}
                                    <div class="newsletter-signature">
                                        <p>Best,</p>
                                        <strong>Aditya Agarwal</strong>
                                        <div class="social-links-sig">
                                            <a href="https://linkedin.com" target="_blank">LinkedIn</a> | 
                                            <a href="https://twitter.com" target="_blank">Twitter</a> | 
                                            <a href="https://decodingeconomies.substack.com" target="_blank">Substack</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="case-study-right-pane">
                                ${compareRows && compareRows.length ? `
                                <div class="case-study-sec card-glass-bg" style="margin-bottom: 16px;">
                                    <h4>NUMERICAL VARIANCE MATRIX</h4>
                                    <div class="comparison-table-wrapper">
                                        <table class="comparison-table">
                                            <thead>
                                                <tr>
                                                    <th>Line Item / Metric</th>
                                                    <th>${headers.standard_label || 'Baseline / Peer'}</th>
                                                    <th>${headers.target_label || 'Forensic Actual'}</th>
                                                    <th>Variance %</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                ${compareRows.map(item => `
                                                    <tr>
                                                        <td>${item.metric}</td>
                                                        <td>${highlightFinancialFigures(item.standard_value)}</td>
                                                        <td class="highlight-target">${highlightFinancialFigures(item.target_value)}</td>
                                                        <td><span class="variance-badge-red">${highlightFinancialFigures(item.mismatch_percentage)}</span></td>
                                                    </tr>
                                                `).join("")}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                ` : ''}
                                <div class="case-study-sec card-glass-bg case-study-question">
                                    <strong>${highlightFinancialFigures(caseStudy.conclusion_question)}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
            break;
            
        case 1: // Slide 1: Home / Executive Brief & Forensic Trust Gap
            {
                const trustGap = reportData.forensic_trust_gap || {
                    standard_sources_coverage: "No standard coverage data parsed.",
                    our_forensic_exposure: "No unique exposure data parsed.",
                    unique_trust_rationale: "No trust rationale data parsed."
                };
                const stats = reportData.usage_stats;
                const statsHtml = stats ? `
                    <div class="usage-stats-hud-card">
                        <div class="usage-stat-box">
                            <span class="stat-num">${(stats.total_tokens / 1000).toFixed(1)}k</span>
                            <span class="stat-label">TOKENS SPENT</span>
                        </div>
                        <div class="usage-stat-box">
                            <span class="stat-num">₹${stats.total_cost_inr.toFixed(3)}</span>
                            <span class="stat-label">API COST (INR)</span>
                        </div>
                        <div class="usage-stat-box">
                            <span class="stat-num">${reportData.anomalies ? reportData.anomalies.length : 0}</span>
                            <span class="stat-label">ANOMALIES</span>
                        </div>
                    </div>
                ` : "";
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Briefing & Differentiation</h3>
                            <h2>EXECUTIVE CONTEXT & FORENSIC TRUST GAP</h2>
                        </div>
                        <div class="split-brief-grid">
                            <div class="case-study-left-pane">
                                <div class="explorer-text-card" style="height: 100%; margin-bottom: 0;">
                                    ${formatMarkdownParagraphs(highlightFinancialFigures(reportData.executive_brief || "No brief available."))}
                                </div>
                            </div>
                            <div class="case-study-right-pane">
                                ${statsHtml}
                                <div class="trust-gap-card">
                                    <div class="trust-gap-header">
                                        <h4>FORENSIC EXPOSURE DIFFERENTIAL</h4>
                                    </div>
                                    <div class="trust-gap-row">
                                        <div class="trust-gap-row-title">Standard Broker & Media Focus</div>
                                        <div class="trust-gap-row-text">${highlightFinancialFigures(trustGap.standard_sources_coverage)}</div>
                                    </div>
                                    <div class="trust-gap-row">
                                        <div class="trust-gap-row-title" style="color: var(--accent-cyan)">What We Expose (Anomalies)</div>
                                        <div class="trust-gap-row-text" style="font-weight: 500;">${highlightFinancialFigures(trustGap.our_forensic_exposure)}</div>
                                    </div>
                                    <div class="trust-gap-row trust-gap-highlight">
                                        <div class="trust-gap-row-title" style="color: var(--accent-green)">Why This Teardown Incurs Unique Trust</div>
                                        <div class="trust-gap-row-text">${highlightFinancialFigures(trustGap.unique_trust_rationale)}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="brief-query-block" style="margin-top: 20px;">
                            <strong>Investigative Target:</strong> "${highlightFinancialFigures(reportData.subject)}"
                        </div>
                        ${renderSlideCitations(reportData.executive_brief_citations)}
                    </div>
                `;
            }
            break;
            
        case 2: // Slide 2: Deep Anomaly Scanner Slide (Claim vs. Defense vs. Verdict)
            {
                const anomalies = reportData.anomalies || [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Scrutiny Scanner</h3>
                            <h2>DETECTED DATA MISMATCHES & VERDICTS</h2>
                        </div>
                        <div class="slide-anomaly-matrix">
                            ${anomalies.map((anom, idx) => `
                                <div class="comparator-card-glass">
                                    <div class="anomaly-card-meta">
                                        <span class="meta-type-tag">${anom.type || "Forensic Scan"}</span>
                                        <span class="badge-risk ${getRiskClass(anom.severity)}">${anom.severity || "Warning"}</span>
                                    </div>
                                    <div class="comparator-grid-card">
                                        <div class="card-half">
                                            <span class="label-claim">CLAIM</span>
                                            <p>"${highlightFinancialFigures(anom.source_claim)}"</p>
                                        </div>
                                        <div class="card-half half-defense">
                                            <span class="label-defense">COUNTER-CLAIM / DEFENSE</span>
                                            <p>"${highlightFinancialFigures(anom.counter_claim || "No standard defense offered.")}"</p>
                                        </div>
                                        <div class="card-half half-reality">
                                            <span class="label-reality">FORENSIC VERDICT</span>
                                            <p>${highlightFinancialFigures(anom.verdict || anom.reality)}</p>
                                        </div>
                                    </div>
                                    ${renderCardCitations(anom.citations)}
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `;
            }
            break;
            
        case 3: // Slide 3: Corporate Fine-Print Explorer (Track 1)
            {
                const corpData = reportData.tracks ? reportData.tracks.corporate : null;
                const textVal = corpData ? (typeof corpData === "object" ? (corpData.text || "") : corpData) : "";
                const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                const citations = corpData && typeof corpData === "object" ? corpData.citations : [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Track 4 / 6</h3>
                            <h2>CORPORATE & FILING FINE PRINT</h2>
                        </div>
                        <div class="explorer-text-card">
                            ${formatEditorialContent(highlightFinancialFigures(text))}
                        </div>
                        ${renderSlideCitations(citations)}
                    </div>
                `;
            }
            break;
            
        case 4: // Slide 4: Government Policy & Schemes (Track 2 & 4)
            {
                const policyData = reportData.tracks ? reportData.tracks.policy : null;
                const textVal = policyData ? (typeof policyData === "object" ? (policyData.text || "") : policyData) : "";
                const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                const citations = policyData && typeof policyData === "object" ? policyData.citations : [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Track 5 / 6</h3>
                            <h2>POLICY FORECASTS & INITIATIVES</h2>
                        </div>
                        <div class="explorer-text-card">
                            ${formatEditorialContent(highlightFinancialFigures(text))}
                        </div>
                        ${renderSlideCitations(citations)}
                    </div>
                `;
            }
            break;
            
        case 5: // Slide 5: Sovereign Strategy (Track 3)
            {
                const sovData = reportData.tracks ? reportData.tracks.sovereign : null;
                const textVal = sovData ? (typeof sovData === "object" ? (sovData.text || "") : sovData) : "";
                const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                const citations = sovData && typeof sovData === "object" ? sovData.citations : [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Track 6 / 6</h3>
                            <h2>SOVEREIGN STRATEGIES & MACRO DEPLOYMENT</h2>
                        </div>
                        <div class="explorer-text-card">
                            ${formatEditorialContent(highlightFinancialFigures(text))}
                        </div>
                        ${renderSlideCitations(citations)}
                    </div>
                `;
            }
            break;
            
        case 6: // Slide 6: Comparative Benchmarks & Strategic Learnings
            {
                const benchmarks = reportData.strategic_benchmarks || [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Benchmarking</h3>
                            <h2>COMPARATIVE BENCHMARKS & STRATEGIC LEARNINGS</h2>
                        </div>
                        <div class="benchmarks-grid">
                            ${benchmarks.length ? benchmarks.map(item => `
                                <div class="benchmark-card">
                                    <div class="benchmark-card-header">
                                        <h4>${item.model_project}</h4>
                                    </div>
                                    <div class="benchmark-card-body">
                                        <div>
                                            <div class="benchmark-item-title">SUCCESSFUL MODEL EXECUTION</div>
                                            <p>${highlightFinancialFigures(item.what_they_did_well)}</p>
                                        </div>
                                        <div>
                                            <div class="benchmark-item-title">INVESTIGATIVE TARGET SHORTFALL</div>
                                            <p>${highlightFinancialFigures(item.our_target_shortfall)}</p>
                                        </div>
                                        <div class="benchmark-learning-block">
                                            <div class="benchmark-item-title" style="color: var(--accent-green)">STRATEGIC LEARNING</div>
                                            <p style="color: var(--text-primary); font-weight: 500;">${highlightFinancialFigures(item.strategic_learning)}</p>
                                        </div>
                                    </div>
                                </div>
                            `).join("") : `
                                <div class="explorer-text-card">
                                    <p>No model benchmarks or comparative learnings have been compiled for this subject yet.</p>
                                </div>
                            `}
                        </div>
                    </div>
                `;
            }
            break;

        case 7: // Slide 7: Socioeconomic Impact Matrix
            {
                let igsHtml = "";
                if (reportData.india_growth_story) {
                    const igs = reportData.india_growth_story;
                    igsHtml = `
                        <div class="india-growth-story-panel glass-panel" id="indiaGrowthStoryContainer">
                            <div class="igs-header">
                                <div class="igs-title-group">
                                    <span class="igs-subtitle-badge">INDIA GROWTH STORY OUTLOOK</span>
                                    <h2 class="igs-panel-title">${highlightFinancialFigures(igs.title)}</h2>
                                </div>
                                <span class="badge-outcome igs-outlook-badge outlook-${igs.outlook ? igs.outlook.toLowerCase() : 'neutral'}">${igs.outlook}</span>
                            </div>
                            <div class="igs-body">
                                ${formatMarkdownParagraphs(highlightFinancialFigures(igs.narrative))}
                            </div>
                        </div>
                    `;
                }
                const socioeconomic = reportData.socioeconomic || [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Synthesis</h3>
                            <h2>SOCIOECONOMIC OUTCOMES (INDIA FOCUS)</h2>
                        </div>
                        <div class="socio-card-grid">
                            ${socioeconomic.map(item => `
                                <div class="socio-impact-card">
                                    <div class="socio-card-header">
                                        <h4>${item.area}</h4>
                                        <span class="badge-outcome ${getOutcomeClass(item.outcome)}">${item.outcome}</span>
                                    </div>
                                    <p>${highlightFinancialFigures(item.impact)}</p>
                                    ${renderCardCitations(item.citations)}
                                </div>
                            `).join("")}
                        </div>
                        ${igsHtml}
                    </div>
                `;
            }
            break;
            
        case 8: // Slide 8: Advanced Forensic & Quantitative Models
            {
                const qModels = reportData.quantitative_models || {};
                const beneish = qModels.beneish_m_score || { score: 0, verdict: 'SAFE' };
                const sloan = qModels.sloan_ratio || { ratio_percentage: 0, verdict: 'LOW' };
                const dupont = qModels.dupont_5_factor || { roe_percentage: 0, factors: {} };
                const kelly = qModels.kelly_criterion || { win_probability: 0, win_loss_ratio: 0, kelly_fraction_percentage: 0, fractional_kelly_percentage: 0 };
                const evt = qModels.evt_tail_risk || { cvar_95_percent: 0, evt_99_percent_cvar: 0 };
                const bass = qModels.bass_diffusion || { p_innovation: 0, q_imitation: 0, years_to_maturity: 0 };
                const power = qModels.power_law_alpha || { exponent_alpha: 0, concentration_verdict: 'FRAGMENTED' };
                const fermi = qModels.fermi_tam_check || { reported_tam_usd: 0, physical_limit_usd: 0, discrepancy_ratio: 1, warning_triggered: false };

                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Model Auditing</h3>
                            <h2>Advanced Risk, Moat & Valuation Models</h2>
                        </div>
                        <div class="quant-grid">
                            <div class="quant-card glass-panel">
                                <h4>Earnings Quality & Accounting Integrity</h4>
                                <div class="quant-explanation-header" style="font-size: 11px; color: var(--text-secondary); opacity: 0.8; margin-bottom: 12px; line-height: 1.4;">
                                    Statistical screens checking for reporting inconsistencies or potential balance-sheet engineering.
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Beneish M-Score:</span>
                                    <span class="q-value highlight-figure">${beneish.score.toFixed(4)}</span>
                                    <span class="badge-risk ${getRiskClass(beneish.verdict)}">${beneish.verdict}</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Earnings Manipulation Detector (Score &gt; -1.78 indicates high anomaly risk).
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Sloan Ratio:</span>
                                    <span class="q-value highlight-figure">${sloan.ratio_percentage.toFixed(2)}%</span>
                                    <span class="badge-risk ${getRiskClass(sloan.verdict)}">${sloan.verdict} Accruals</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Cash Flow vs. Accrual Integrity (Values within &plusmn;10% indicate solid cash-backed earnings).
                                </div>
                                <div class="quant-sub-card" style="margin-top: 16px;">
                                    <h5>DuPont ROE Profitability Drivers</h5>
                                    <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 6px;">
                                        Deconstructs Return on Equity into five operating efficiency factors:
                                    </div>
                                    <ul>
                                        <li>Tax Burden (Net Income/EBT): <span>${(dupont.factors.tax_burden || 0).toFixed(2)}</span></li>
                                        <li>Interest Burden (EBT/EBIT): <span>${(dupont.factors.interest_burden || 0).toFixed(2)}</span></li>
                                        <li>Operating Margin (EBIT/Sales): <span>${((dupont.factors.operating_margin || 0) * 100).toFixed(2)}%</span></li>
                                        <li>Asset Turnover (Sales/Assets): <span>${(dupont.factors.asset_turnover || 0).toFixed(2)}x</span></li>
                                        <li>Equity Multiplier (Assets/Equity): <span>${(dupont.factors.equity_multiplier || 0).toFixed(2)}x</span></li>
                                        <li class="dupont-final" style="margin-top: 8px; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 6px; font-weight: bold;">
                                            ROE Decomposition: <span>${dupont.roe_percentage.toFixed(2)}%</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="quant-card glass-panel">
                                <h4>Investment Sizing & Tail Risk Models</h4>
                                <div class="quant-explanation-header" style="font-size: 11px; color: var(--text-secondary); opacity: 0.8; margin-bottom: 12px; line-height: 1.4;">
                                    Capital allocation frameworks and loss distributions for extreme statistical scenarios.
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Kelly Sizing Fraction (f*):</span>
                                    <span class="q-value highlight-figure">${kelly.kelly_fraction_percentage.toFixed(2)}%</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Kelly Criterion (Optimal theoretical allocation of investment capital based on edge/odds).
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Recommended (f*/4):</span>
                                    <span class="q-value highlight-figure">${kelly.fractional_kelly_percentage.toFixed(2)}%</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Conservative Allocation (Fractional sizing to shield against variance and drawdowns).
                                </div>
                                <div class="quant-sub-card" style="margin-top: 16px;">
                                    <h5>Extreme Market Risk (Tail Risk Models)</h5>
                                    <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 8px;">
                                        Estimates structural capital exposure under worst-case statistical shocks:
                                    </div>
                                    <ul>
                                        <li>Conditional VaR (95% CVaR): <span class="highlight-figure">${evt.cvar_95_percent.toFixed(2)}%</span></li>
                                        <li>EVT Tail Risk (99% CVaR): <span class="highlight-figure">${evt.evt_99_percent_cvar.toFixed(2)}%</span></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="quant-card glass-panel">
                                <h4>Market Moat & Adoption Life Cycle</h4>
                                <div class="quant-explanation-header" style="font-size: 11px; color: var(--text-secondary); opacity: 0.8; margin-bottom: 12px; line-height: 1.4;">
                                    Evaluates market expansion speed, saturation limits, and competitive market concentration.
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Bass Diffusion Curve:</span>
                                    <span class="q-value" style="font-size: 13px;">p=${bass.p_innovation.toFixed(4)}, q=${bass.q_imitation.toFixed(4)}</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Adoption Velocity (p = Innovation coefficient; q = Imitation/Network effect coefficient).
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Maturation Time:</span>
                                    <span class="q-value highlight-figure">${bass.years_to_maturity.toFixed(1)} years</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Estimated time in years until the target market reaches peak maturity/consolidation.
                                </div>
                                <div class="quant-metric-row">
                                    <span class="q-label">Power Law Alpha:</span>
                                    <span class="q-value highlight-figure">α=${power.exponent_alpha.toFixed(2)}</span>
                                    <span class="badge-outcome ${getOutcomeClass(power.concentration_verdict)}">${power.concentration_verdict}</span>
                                </div>
                                <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 12px;">
                                    Consolidation Index (Alpha &lt; 1.2 indicates a highly consolidated winner-take-all moat structure).
                                </div>
                                <div class="quant-sub-card" style="margin-top: 16px;">
                                    <h5>Fermi TAM Reality Check</h5>
                                    <div class="q-desc" style="font-size: 11px; color: var(--text-secondary); opacity: 0.7; margin-top: 2px; margin-bottom: 6px;">
                                        Sanity check comparing reported market size (TAM) against absolute physical boundaries:
                                    </div>
                                    <ul>
                                        <li>Reported TAM: <span>$${(fermi.reported_tam_usd / 1e9).toFixed(1)}B</span></li>
                                        <li>Fermi Physical Limit: <span>$${(fermi.physical_limit_usd / 1e9).toFixed(1)}B</span></li>
                                        <li class="fermi-warning ${fermi.warning_triggered ? 'warning-active' : ''}" style="margin-top: 4px; font-weight: 500;">
                                            TAM Discrepancy: <span class="highlight-figure">${fermi.discrepancy_ratio.toFixed(1)}x</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
            break;

        case 9: // Slide 9: Citation References (or Deep-Dive slide if totalSlides === 11)
            if (totalSlides === 11) {
                const dd = reportData.deep_dive || { title: "Deep-Dive Slide", narrative: "No deep-dive narrative compiled.", metrics: [], citations: [] };
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>Deep-Dive Investigation</h3>
                            <h2>${dd.title.toUpperCase()}</h2>
                        </div>
                        <div class="split-brief-grid">
                            <div class="case-study-left-pane">
                                <div class="explorer-text-card" style="height: 100%; margin-bottom: 0;">
                                    ${formatMarkdownParagraphs(highlightFinancialFigures(dd.narrative))}
                                </div>
                            </div>
                            <div class="case-study-right-pane">
                                <div class="trust-gap-card">
                                    <div class="trust-gap-header">
                                        <h4>KEY DEEP-DIVE METRICS</h4>
                                    </div>
                                    ${(dd.metrics || []).map(metric => `
                                        <div class="trust-gap-row">
                                            <div class="trust-gap-row-title">${metric.label}</div>
                                            <div class="trust-gap-row-text" style="font-weight: 500;">${highlightFinancialFigures(metric.value)}</div>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>
                        </div>
                        ${renderSlideCitations(dd.citations)}
                    </div>
                `;
            } else {
                const citations = reportData.citations || [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>References</h3>
                            <h2>VERIFIED SOURCE CITATIONS</h2>
                        </div>
                        <div class="citations-list-deck">
                            ${citations.map((cit, idx) => `
                                <div class="citation-card-ref">
                                    <div class="citation-info-block">
                                        <span>[${idx+1}] ${cit.name}</span>
                                        <em>${cit.url}</em>
                                    </div>
                                    <a href="${cit.url}" target="_blank" class="citation-out-btn">OPEN ▶</a>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `;
            }
            break;

        case 10: // Slide 10: Citation References (only if totalSlides === 11)
            {
                const citations = reportData.citations || [];
                html = `
                    <div class="slide-content-block">
                        <div class="slide-title-block">
                            <h3>References</h3>
                            <h2>VERIFIED SOURCE CITATIONS</h2>
                        </div>
                        <div class="citations-list-deck">
                            ${citations.map((cit, idx) => `
                                <div class="citation-card-ref">
                                    <div class="citation-info-block">
                                        <span>[${idx+1}] ${cit.name}</span>
                                        <em>${cit.url}</em>
                                    </div>
                                    <a href="${cit.url}" target="_blank" class="citation-out-btn">OPEN ▶</a>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `;
            }
            break;
    }

    slideWindow.innerHTML = html;
}

// =====================================================================
// POPULATE SIDEBAR SCANNER
// =====================================================================
function populateAnomalySidebar() {
    if (!reportData || !reportData.anomalies) return;
    
    anomalyList.innerHTML = reportData.anomalies.map(anom => `
        <div class="comparator-card-glass">
            <div class="anomaly-card-meta">
                <span class="meta-type-tag">${anom.type || "Forensic Scan"}</span>
                <span class="badge-risk ${getRiskClass(anom.severity)}">${anom.severity || "High"}</span>
            </div>
            <div class="comparator-grid-card">
                <div class="card-half">
                    <span class="label-claim">CLAIM</span>
                    <p>"${highlightFinancialFigures(anom.source_claim)}"</p>
                </div>
                <div class="card-half half-defense">
                    <span class="label-defense">COUNTER-CLAIM / DEFENSE</span>
                    <p>"${highlightFinancialFigures(anom.counter_claim || "No standard defense offered.")}"</p>
                </div>
                <div class="card-half half-reality">
                    <span class="label-reality">FORENSIC VERDICT</span>
                    <p>${highlightFinancialFigures(anom.verdict || anom.reality)}</p>
                </div>
            </div>
            ${renderCardCitations(anom.citations)}
        </div>
    `).join("");
}

// =====================================================================
// AUTOMATED DYNAMIC FINANCIAL HIGHLIGHTER
// =====================================================================
function highlightFinancialFigures(text) {
    if (!text) return "";
    
    let placeholders = [];
    let html = text;
    
    // 1. Temporarily replace Markdown Links [text](url) and [text](slide:X) with placeholders
    // This protects everything inside the brackets and parentheses from the highlighter
    html = html.replace(/\[{1,2}\s*([^\]]+?)\s*\]{1,2}\s*\(\s*(https?:\/\/[^\s)]+|slide:\d+)\s*\)/g, (match, linkText, url) => {
        const placeholder = `__MD_LINK_PLACEHOLDER_${placeholders.length}__`;
        placeholders.push({ match, linkText, url });
        return placeholder;
    });
    
    // 2. Temporarily replace plain URLs with placeholders
    html = html.replace(/(https?:\/\/[^\s)]+)/g, (match) => {
        const placeholder = `__PLAIN_URL_PLACEHOLDER_${placeholders.length}__`;
        placeholders.push({ match, url: match });
        return placeholder;
    });
    
    // 3. Highlight rupee amounts and currency phrases (e.g., ₹1,584 crore, ₹72-76 per share, ₹3.31 Cr)
    html = html.replace(/(₹\s?\d+(?:[.,\d-]*\d+)?(?:\s?(?:crore|lakh|million|billion|shares|per share|cr|lacs|lakhs|lakh))?)/gi, '<span class="highlight-figure">$1</span>');
    
    // 4. Highlight percentages (e.g. 36.86%, 12.58%, 15-20%)
    html = html.replace(/(\b\d+(?:\.\d+)?(?:\s?-\s?\d+(?:\.\d+)?)?%)/g, '<span class="highlight-figure">$1</span>');
    
    // 5. Highlight growth rates and multipliers (e.g. 13.4x, 2X, 6.5x, 2-3x)
    html = html.replace(/(\b\d+(?:\.\d+)?(?:\s?-\s?\d+(?:\.\d+)?)?[xX]\b)/g, '<span class="highlight-figure">$1</span>');
    
    // 6. Highlight comma-separated large numbers (e.g. 95,191,195)
    html = html.replace(/(\b\d{1,3}(?:,\d{3})+\b)/g, '<span class="highlight-figure">$1</span>');
    
    // 7. Restore placeholders and convert them to HTML anchors
    placeholders.forEach((item, idx) => {
        const mdPlaceholder = `__MD_LINK_PLACEHOLDER_${idx}__`;
        const plainPlaceholder = `__PLAIN_URL_PLACEHOLDER_${idx}__`;
        
        if (item.linkText) {
            let anchorHtml = "";
            if (item.url.startsWith("slide:")) {
                const slideNum = item.url.split(":")[1];
                anchorHtml = `<a href="#" class="internal-slide-link" onclick="goToSlide(${slideNum}); return false;">${item.linkText}</a>`;
            } else {
                anchorHtml = `<a href="${item.url}" target="_blank" class="external-source-link">${item.linkText}</a>`;
            }
            html = html.replace(mdPlaceholder, anchorHtml);
        } else {
            const anchorHtml = `<a href="${item.url}" target="_blank" class="external-source-link">${item.url}</a>`;
            html = html.replace(plainPlaceholder, anchorHtml);
        }
    });
    
    // 8. Parse Markdown Bold
    html = html.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
    
    // 9. Parse Markdown Italics
    html = html.replace(/\*([^\s\*][^*]*?[^\s\*]|[^\s\*])\*/g, '<em>$1</em>');
    
    return html;
}

// =====================================================================
// CITATION RENDERING HELPERS
// =====================================================================
function renderSlideCitations(citations) {
    if (!citations || !citations.length) return "";
    return `
        <div class="slide-citations-container">
            <span class="slide-citations-label">SOURCES & VETTING LINKS:</span>
            <div class="slide-citations-list">
                ${citations.map(c => `
                    <a href="${c.url}" target="_blank" class="citation-pill" title="${c.url}">
                        <span class="citation-pill-icon">🔗</span>
                        <span class="citation-pill-text">${c.name}</span>
                    </a>
                `).join("")}
            </div>
        </div>
    `;
}

function renderCardCitations(citations) {
    if (!citations || !citations.length) return "";
    return `
        <div class="card-citations-block">
            ${citations.map(c => `
                <a href="${c.url}" target="_blank" class="card-citation-link" title="${c.url}">
                    [${c.name}]
                </a>
            `).join("")}
        </div>
    `;
}

// =====================================================================
// UI STYLING & HELPER FUNCTIONS
// =====================================================================
function getRiskClass(severity) {
    if (!severity) return "risk-high";
    const s = severity.toLowerCase();
    if (s.includes("high")) return "risk-high";
    if (s.includes("med") || s.includes("yellow")) return "risk-medium";
    return "risk-low";
}

function getOutcomeClass(outcome) {
    if (!outcome) return "outcome-neutral";
    const o = outcome.toLowerCase();
    if (o.includes("pos")) return "outcome-positive";
    if (o.includes("neg")) return "outcome-negative";
    return "outcome-neutral";
}

function formatEditorialContent(text) {
    if (!text) return "";
    
    // Split by newline or multiple newlines
    return text.split(/\n+/).map(line => {
        let l = line.trim();
        if (!l) return "";
        
        // If it starts with a number and dash/dot/colon (e.g. "1 - ", "1. ", "1: ")
        if (/^\d+\s*[-\.:]\s*/.test(l)) {
            return `<div class="editorial-list-item">${l}</div>`;
        }
        // If it starts with list bullet (e.g. "* ", "- ")
        if (/^[\*\-]\s+/.test(l)) {
            return `<div class="editorial-bullet-item">${l.replace(/^[\*\-]\s+/, "")}</div>`;
        }
        // Default to bullet item for clean visual formatting
        return `<div class="editorial-bullet-item">${l}</div>`;
    }).join("");
}

window.goToSlide = function(slideNum) {
    const targetIdx = parseInt(slideNum) - 1;
    if (targetIdx >= 0 && targetIdx < totalSlides) {
        currentSlideIndex = targetIdx;
        renderSlide(currentSlideIndex);
        updateDeckControls();
    }
};

function parseMarkdownLinks(text) {
    if (!text) return "";
    
    let html = text;
    // Replace internal slide links: [Slide X](slide:X) or [[Slide X]](slide:X) with optional spaces
    html = html.replace(/\[{1,2}\s*([^\]]+?)\s*\]{1,2}\s*\(\s*slide:(\d+)\s*\)/g, '<a href="#" class="internal-slide-link" onclick="goToSlide($2); return false;">$1</a>');
    
    // Replace external source links: [Link Text](https://...) or [[Link Text]](https://...) with optional spaces
    html = html.replace(/\[{1,2}\s*([^\]]+?)\s*\]{1,2}\s*\(\s*(https?:\/\/[^\s)]+)\s*\)/g, '<a href="$2" target="_blank" class="external-source-link">$1</a>');
    
    return html;
}

function formatEditorialVerdict(text) {
    if (!text) return "";
    
    // Parse links first so markdown notation is converted to clean HTML anchors
    let processedText = parseMarkdownLinks(text);
    
    // Split by double newlines or two or more newlines to handle paragraph blocks
    // Or if the content contains ".." (used as a separator in user sample), replace and split
    let rawText = processedText.replace(/\n\.\.\n/g, "\n\n");
    rawText = rawText.replace(/\.\./g, "\n\n");
    
    return rawText.split(/\n\n+/).map(para => {
        let p = para.trim();
        if (!p) return "";
        
        // Check if paragraph itself is a bulleted list (lines starting with - or *)
        if (p.startsWith("- ") || p.startsWith("* ") || p.includes("\n- ") || p.includes("\n* ")) {
            const listItems = p.split(/\n[\*\-]\s+/).map(item => {
                let cleanItem = item.trim();
                // strip starting indicator if present
                if (cleanItem.startsWith("- ") || cleanItem.startsWith("* ")) {
                    cleanItem = cleanItem.substring(2);
                }
                if (!cleanItem) return "";
                return `<div class="editorial-bullet-item">${cleanItem}</div>`;
            }).join("");
            return `<div style="margin-bottom: 18px;">${listItems}</div>`;
        }
        
        // If it's a list item itself
        if (/^\d+\s*[-\.:]\s*/.test(p)) {
            return `<div class="editorial-list-item" style="margin-bottom: 18px;">${p}</div>`;
        }
        
        return `<p>${p}</p>`;
    }).join("");
}

function formatMarkdownParagraphs(text) {
    if (!text) return "No data available.";
    
    // Simplistic converter of Markdown to HTML formatting for the viewer
    return text.split("\n\n").map(para => {
        let p = para.trim();
        if (!p) return "";
        
        // Header markdown replacement
        if (p.startsWith("### ")) {
            return `<h4>${p.substring(4)}</h4>`;
        }
        if (p.startsWith("## ")) {
            return `<h3>${p.substring(3)}</h3>`;
        }
        
        // List item markdown replacement
        if (p.startsWith("* ") || p.startsWith("- ")) {
            const listItems = p.split(/\n[\*\-]\s/).map(item => `<li>${item.replace(/^[\*\-]\s/, "")}</li>`).join("");
            return `<ul>${listItems}</ul>`;
        }
        
        return `<p>${p}</p>`;
    }).join("");
}

function updateDeckControls() {
    btnPrev.disabled = currentSlideIndex === 0;
    btnNext.disabled = currentSlideIndex === totalSlides - 1;
    currentSlideNum.textContent = currentSlideIndex + 1;
    
    // Calculate progress percentage
    const progressPercent = ((currentSlideIndex + 1) / totalSlides) * 100;
    progressBar.style.width = `${progressPercent}%`;
}

// Renders visual step-by-step instructions if forensic_report.json is missing
function renderSetupInstructions() {
    slideWindow.innerHTML = `
        <div class="instructions-card-deck">
            <h3>▲ Structured Database Not Found</h3>
            <p>To populate this interactive slide deck dashboard, please run the active Python research orchestrator in your terminal first to fetch and compile the database:</p>
            <div class="code-block-display">
                python forensics_orchestrator.py "YOUR RESEARCH QUERY HERE"
            </div>
            <p>This will execute web harvesters, perform the anomaly scans, write the database payload to your workspace, and automatically activate this dashboard!</p>
        </div>
    `;
    
    anomalyList.innerHTML = `
        <div class="sidebar-loading-placeholder">
            Waiting for search audit execution...
        </div>
    `;
}

// =====================================================================
// DECK NAVIGATION CONTROLLERS
// =====================================================================
function slideNext() {
    if (currentSlideIndex < totalSlides - 1) {
        currentSlideIndex++;
        renderSlide(currentSlideIndex);
        updateDeckControls();
    }
}

function slidePrev() {
    if (currentSlideIndex > 0) {
        currentSlideIndex--;
        renderSlide(currentSlideIndex);
        updateDeckControls();
    }
}

// Navigation event listeners
btnNext.addEventListener("click", slideNext);
btnPrev.addEventListener("click", slidePrev);

// Add Arrow key navigation listener
document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
        slideNext();
    } else if (e.key === "ArrowLeft") {
        slidePrev();
    }
});

// Bootstrapping
if (document.readyState === "loading") {
    window.addEventListener("DOMContentLoaded", loadForensicData);
} else {
    loadForensicData();
}

// =====================================================================
// SOCIAL SHARING DECK SUMMARY ENGINE
// =====================================================================
const shareModal = document.getElementById("shareModal");
const btnShareDeck = document.getElementById("btnShareDeck");
const btnShareModalClose = document.getElementById("btnShareModalClose");
const btnShareModalCloseIcon = document.getElementById("btnShareModalCloseIcon");
const btnCopyPost = document.getElementById("btnCopyPost");
const sharePostContent = document.getElementById("sharePostContent");

function cleanTextForSocial(text) {
    if (!text) return "";
    let plain = text;
    // Remove internal slide links
    plain = plain.replace(/\[{1,2}\s*([^\]]+?)\s*\]{1,2}\s*\(\s*slide:\d+\s*\)/g, "$1");
    // Format external source links as: Text (URL)
    plain = plain.replace(/\[{1,2}\s*([^\]]+?)\s*\]{1,2}\s*\(\s*(https?:\/\/[^\s)]+)\s*\)/g, "$1 ($2)");
    // Remove bold asterisks
    plain = plain.replace(/\*\*([^*]+)\*\*/g, "$1");
    // Remove italic asterisks
    plain = plain.replace(/\*([^\s\*][^*]*?[^\s\*]|[^\s\*])\*/g, "$1");
    // Remove HTML tags
    plain = plain.replace(/<[^>]*>/g, "");
    return plain.trim();
}

function generateSocialPostText() {
    if (!reportData) return "No data loaded yet.";

    // If the refinement model compiled a dedicated social media post, use it as the premium option
    if (reportData.social_share_post) {
        return cleanTextForSocial(reportData.social_share_post);
    }

    const subject = reportData.subject || "Investigative Teardown";
    const caseStudy = reportData.forensic_case_study || {};
    const headline = caseStudy.headline || "Macro-Corporate Forensics Teardown";
    
    let post = `📢 FORENSIC INVESTIGATION TEARDOWN: ${headline.toUpperCase()}\n\n`;
    
    // 1. Editorial Narrative
    if (caseStudy.editorial_verdict) {
        post += `🔍 THE VERDICT:\n${cleanTextForSocial(caseStudy.editorial_verdict)}\n\n`;
    }
    
    // 2. Side by Side Comparison
    if (caseStudy.side_by_side_comparison && caseStudy.side_by_side_comparison.length) {
        post += `📊 CORE METRIC DIVERGENCES & VARIANCES:\n`;
        caseStudy.side_by_side_comparison.forEach(item => {
            post += `• ${item.metric}: Standard/Peer: ${cleanTextForSocial(item.standard_value)} | Forensic Actual: ${cleanTextForSocial(item.target_value)} (Variance: ${cleanTextForSocial(item.mismatch_percentage)})\n`;
        });
        post += `\n`;
    }
    
    // 3. Top Anomalies
    if (reportData.anomalies && reportData.anomalies.length) {
        post += `🚨 DECONSTRUCTED MISMATCHES:\n`;
        reportData.anomalies.forEach((anom, idx) => {
            post += `${idx + 1}. CLAIM: "${cleanTextForSocial(anom.source_claim)}"\n`;
            post += `   COUNTER-CLAIM/DEFENSE: "${cleanTextForSocial(anom.counter_claim)}"\n`;
            post += `   FORENSIC VERDICT: ${cleanTextForSocial(anom.verdict || anom.reality)}\n\n`;
        });
    }
    
    // 4. Strategic Benchmarks (Case Studies)
    if (reportData.strategic_benchmarks && reportData.strategic_benchmarks.length) {
        post += `💡 GLOBAL STRATEGIC BENCHMARKS & LEARNINGS:\n`;
        reportData.strategic_benchmarks.forEach(bench => {
            post += `• Model Project: ${bench.model_project}\n`;
            post += `  - What They Did Well: ${cleanTextForSocial(bench.what_they_did_well)}\n`;
            post += `  - Our Shortfall: ${cleanTextForSocial(bench.our_target_shortfall)}\n`;
            post += `  - Learning/Takeaway: ${cleanTextForSocial(bench.strategic_learning)}\n\n`;
        });
    }
    
    // 5. Socioeconomic Outcomes
    if (reportData.socioeconomic && reportData.socioeconomic.length) {
        post += `🌱 DYNAMIC SOCIOECONOMIC OUTCOMES:\n`;
        reportData.socioeconomic.forEach(item => {
            post += `• Area: ${item.area} [Status: ${item.outcome}]\n`;
            post += `  - Impact: ${cleanTextForSocial(item.impact)}\n`;
        });
        post += `\n`;
    }
    
    // 6. Conclusion Question
    if (caseStudy.conclusion_question) {
        post += `🤔 OUTLOOK QUESTION:\n"${cleanTextForSocial(caseStudy.conclusion_question)}"\n\n`;
    }
    
    // 7. Footer & Citations
    post += `🔍 Generated via Antigravity Nexus Forensics.\n`;
    post += `#MacroEconomics #CorporateForensics #BusinessIntelligence #PolicyAnalysis`;
    
    return post;
}

function compileInteractivePost() {
    if (!reportData) return;

    const isStructured = reportData.social_share_post && typeof reportData.social_share_post === "object" && !Array.isArray(reportData.social_share_post);
    const controlsSplit = document.querySelector(".share-modal-body-split");
    const controlsPanel = document.querySelector(".share-modal-controls");

    if (!isStructured) {
        // Legacy fallback
        if (controlsPanel) controlsPanel.style.display = "none";
        if (controlsSplit) controlsSplit.classList.add("legacy-only");
        sharePostContent.value = generateSocialPostText();
    } else {
        // Structured mode
        if (controlsPanel) controlsPanel.style.display = "block";
        if (controlsSplit) controlsSplit.classList.remove("legacy-only");

        const radioContainer = document.getElementById("headlineRadios");
        const headlines = reportData.social_share_post.headlines || [];
        
        // Populate radios if empty
        if (radioContainer.innerHTML.trim() === "") {
            let radioHtml = "";
            headlines.forEach((hl, i) => {
                const checked = i === 0 ? "checked" : "";
                radioHtml += `
                    <label class="control-radio-label">
                        <input type="radio" name="postHeadline" value="${i}" ${checked}>
                        <span class="radio-custom-btn"></span>
                        <span class="radio-text">${cleanTextForSocial(hl)}</span>
                    </label>
                `;
            });
            radioContainer.innerHTML = radioHtml;

            // Add change listener to newly created radios
            const radios = radioContainer.querySelectorAll('input[type="radio"]');
            radios.forEach(radio => {
                radio.addEventListener("change", compileInteractivePost);
            });
        }

        // Get selected radio
        const selectedRadio = radioContainer.querySelector('input[name="postHeadline"]:checked');
        const hlIndex = selectedRadio ? parseInt(selectedRadio.value) : 0;
        const headlineText = headlines[hlIndex] || "";

        let postParts = [];
        postParts.push(`📢 ${cleanTextForSocial(headlineText).toUpperCase()}`);

        const sections = reportData.social_share_post.sections || {};
        
        // Editorial Verdict
        if (document.getElementById("chkVerdict").checked && sections.verdict) {
            postParts.push(`🔍 THE VERDICT:\n${cleanTextForSocial(sections.verdict)}`);
        }
        // Key Metrics
        if (document.getElementById("chkMetrics").checked && sections.metrics) {
            postParts.push(`📊 KEY METRICS & VARIANCES:\n${cleanTextForSocial(sections.metrics)}`);
        }
        // Anomalies
        if (document.getElementById("chkAnomalies").checked && sections.anomalies) {
            postParts.push(`🚨 FORENSIC ANOMALIES:\n${cleanTextForSocial(sections.anomalies)}`);
        }
        // Benchmarks
        if (document.getElementById("chkBenchmarks").checked && sections.benchmarks) {
            postParts.push(`💡 STRATEGIC BENCHMARKS:\n${cleanTextForSocial(sections.benchmarks)}`);
        }
        // India Growth Outlook
        if (document.getElementById("chkSocio").checked && sections.socioeconomic) {
            postParts.push(`🌱 SOCIOECONOMIC & INDIA GROWTH STORY:\n${cleanTextForSocial(sections.socioeconomic)}`);
        }
        // Citations
        if (document.getElementById("chkCitations").checked && reportData.social_share_post.citations && reportData.social_share_post.citations.length) {
            let citationsText = `🔗 BACKING SOURCES & VETTING LINKS:\n`;
            reportData.social_share_post.citations.forEach(c => {
                citationsText += `• ${cleanTextForSocial(c)}\n`;
            });
            postParts.push(citationsText.trim());
        }

        postParts.push(`🔍 Generated via Antigravity Nexus Forensics.\n#MacroEconomics #CorporateForensics #BusinessIntelligence #PolicyAnalysis`);

        sharePostContent.value = postParts.join("\n\n");
    }
}

if (btnShareDeck) {
    btnShareDeck.addEventListener("click", () => {
        // Reset headline radios container so it gets rebuilt
        const radioContainer = document.getElementById("headlineRadios");
        if (radioContainer) radioContainer.innerHTML = "";
        
        compileInteractivePost();
        shareModal.classList.add("active");
    });
}

// Add listeners to checkboxes
const shareCheckboxes = ["chkVerdict", "chkMetrics", "chkAnomalies", "chkBenchmarks", "chkSocio", "chkCitations"];
shareCheckboxes.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener("change", compileInteractivePost);
    }
});

function closeShareModal() {
    shareModal.classList.remove("active");
    btnCopyPost.textContent = "📋 COPY POST";
}

if (btnShareModalClose) {
    btnShareModalClose.addEventListener("click", closeShareModal);
}
if (btnShareModalCloseIcon) {
    btnShareModalCloseIcon.addEventListener("click", closeShareModal);
}
if (shareModal) {
    shareModal.addEventListener("click", (e) => {
        if (e.target === shareModal) {
            closeShareModal();
        }
    });
}

if (btnCopyPost) {
    btnCopyPost.addEventListener("click", () => {
        sharePostContent.select();
        sharePostContent.setSelectionRange(0, 99999); // For mobile devices
        
        navigator.clipboard.writeText(sharePostContent.value).then(() => {
            btnCopyPost.textContent = "Copied! ✔";
            setTimeout(() => {
                btnCopyPost.textContent = "📋 COPY POST";
            }, 3000);
        }).catch(err => {
            console.error("Clipboard copy failed:", err);
        });
    });
}
