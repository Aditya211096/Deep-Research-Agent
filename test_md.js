function highlightAndParseMarkdown(text) {
    if (!text) return "";
    
    let placeholders = [];
    let html = text;
    
    // 1. Temporarily replace Markdown Links [text](url) and [text](slide:X) with placeholders
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+|slide:\d+)\)/g, (match, linkText, url) => {
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
    
    // 3. Highlight figures
    html = html.replace(/(₹\s?\d+(?:[.,\d-]*\d+)?(?:\s?(?:crore|lakh|million|billion|shares|per share|cr|lacs|lakhs|lakh))?)/gi, '<span class="highlight-figure">$1</span>');
    html = html.replace(/(\b\d+(?:\.\d+)?(?:\s?-\s?\d+(?:\.\d+)?)?%)/g, '<span class="highlight-figure">$1</span>');
    html = html.replace(/(\b\d+(?:\.\d+)?(?:\s?-\s?\d+(?:\.\d+)?)?[xX]\b)/g, '<span class="highlight-figure">$1</span>');
    html = html.replace(/(\b\d{1,3}(?:,\d{3})+\b)/g, '<span class="highlight-figure">$1</span>');
    
    // 4. Restore placeholders and convert them to HTML anchors
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
    
    // 5. Parse Markdown Bold
    html = html.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
    
    // 6. Parse Markdown Italics
    html = html.replace(/\*([^\s\*][^*]*?[^\s\*]|[^\s\*])\*/g, '<em>$1</em>');
    
    return html;
}

let input = '*   **The Consumption Chasm:** While RE *capacity* is 45%, coal and lignite still fueled **59%** of India\'s total energy *consumption* in FY23, according to an [NGEL assessment](https://www.ngel.in/public/investors/02%20Indian%20Power%20RE%20%20marker%20assessment_NGEL.pdf).';
console.log("Result:\n", highlightAndParseMarkdown(input));
