const fs = require('fs');
const path = require('path');

// Simulate the browser environment
const reportData = JSON.parse(fs.readFileSync(path.join(__dirname, 'dashboard', 'zepto_business_model', 'forensic_report.json'), 'utf8'));
const totalSlides = reportData.deep_dive ? 11 : 10;

console.log("Total slides calculated:", totalSlides);

// Mock functions that app.js uses
function highlightFinancialFigures(text) {
    if (!text) return "";
    return text; // mock
}
function formatEditorialVerdict(text) {
    if (!text) return "";
    return text;
}
function formatMarkdownParagraphs(text) {
    if (!text) return "";
    return text;
}
function formatEditorialContent(text) {
    if (!text) return "";
    return text;
}
function getRiskClass(sev) {
    return "risk";
}
function getOutcomeClass(out) {
    return "outcome";
}
function renderSlideCitations(citations) {
    return "citations";
}
function renderCardCitations(citations) {
    return "citations";
}

// Test render for each index
for (let index = 0; index < totalSlides; index++) {
    try {
        console.log(`Testing slide index ${index}...`);
        let html = "";
        switch(index) {
            case 0:
                {
                    const caseStudy = reportData.forensic_case_study || {
                        headline: "",
                        editorial_verdict: "",
                        side_by_side_comparison: { rows: [] },
                        conclusion_question: ""
                    };
                    const isObjectFormat = caseStudy.side_by_side_comparison && !Array.isArray(caseStudy.side_by_side_comparison);
                    const compareRows = isObjectFormat ? (caseStudy.side_by_side_comparison.rows || []) : (caseStudy.side_by_side_comparison || []);
                    const headers = isObjectFormat ? (caseStudy.side_by_side_comparison.column_headers || {}) : {};
                    
                    html = `${compareRows.map(item => item.metric).join("")}`;
                }
                break;
            case 1:
                {
                    const trustGap = reportData.forensic_trust_gap || {};
                    html = `${trustGap.standard_sources_coverage}`;
                }
                break;
            case 2:
                {
                    const anomalies = reportData.anomalies || [];
                    html = `${anomalies.map(anom => anom.source_claim).join("")}`;
                }
                break;
            case 3:
                {
                    const corpData = reportData.tracks ? reportData.tracks.corporate : null;
                    const textVal = corpData ? (typeof corpData === "object" ? (corpData.text || "") : corpData) : "";
                    const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                }
                break;
            case 4:
                {
                    const policyData = reportData.tracks ? reportData.tracks.policy : null;
                    const textVal = policyData ? (typeof policyData === "object" ? (policyData.text || "") : policyData) : "";
                    const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                }
                break;
            case 5:
                {
                    const sovData = reportData.tracks ? reportData.tracks.sovereign : null;
                    const textVal = sovData ? (typeof sovData === "object" ? (sovData.text || "") : sovData) : "";
                    const text = Array.isArray(textVal) ? textVal.join("\n") : textVal;
                }
                break;
            case 6:
                {
                    const benchmarks = reportData.strategic_benchmarks || [];
                    html = `${benchmarks.map(item => item.model_project).join("")}`;
                }
                break;
            case 7:
                {
                    const socioeconomic = reportData.socioeconomic || [];
                    html = `${socioeconomic.map(item => item.area).join("")}`;
                }
                break;
            case 8:
                {
                    const qModels = reportData.quantitative_models || {};
                    const beneish = qModels.beneish_m_score || { score: 0, verdict: 'SAFE' };
                }
                break;
            case 9:
                if (totalSlides === 11) {
                    const dd = reportData.deep_dive || { title: "", narrative: "", metrics: [], citations: [] };
                    html = `${dd.title}`;
                } else {
                    const citations = reportData.citations || [];
                    html = `${citations.map(cit => cit.name).join("")}`;
                }
                break;
            case 10:
                {
                    const citations = reportData.citations || [];
                    html = `${citations.map(cit => cit.name).join("")}`;
                }
                break;
        }
        console.log(`Slide index ${index} render SUCCESS.`);
    } catch (err) {
        console.error(`Slide index ${index} render FAILED:`, err.message);
    }
}
