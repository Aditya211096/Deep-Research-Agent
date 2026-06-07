import os
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_style_or_script = False

    def handle_starttag(self, tag, attrs):
        if tag in ['style', 'script']:
            self.in_style_or_script = True
        elif tag in ['p', 'h1', 'h2', 'h3', 'li', 'blockquote']:
            self.text_parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ['style', 'script']:
            self.in_style_or_script = False
        elif tag in ['p', 'h1', 'h2', 'h3', 'li', 'blockquote']:
            self.text_parts.append('\n')

    def handle_data(self, data):
        if not self.in_style_or_script:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(data)

def clean_file(html_path, output_path):
    if not os.path.exists(html_path):
        print(f"Path does not exist: {html_path}")
        return
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    extractor = TextExtractor()
    extractor.feed(content)
    extracted_text = "".join(extractor.text_parts)

    cleaned_lines = []
    for line in extracted_text.split('\n'):
        stripped = line.strip()
        if stripped:
            cleaned_lines.append(stripped)
        elif cleaned_lines and cleaned_lines[-1] != "":
            cleaned_lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned_lines))

    print(f"Clean text successfully written to {output_path}")

base_dir = r"C:\Users\Aditya\.gemini\antigravity\brain\4c0fa76b-dbaf-4919-a30a-dd50e654dca9\.system_generated\steps"
jobs = [
    (os.path.join(base_dir, "1438", "content.md"), r"D:\New folder\drone_article_clean.txt"),
    (os.path.join(base_dir, "1440", "content.md"), r"D:\New folder\bakong_article_clean.txt"),
    (os.path.join(base_dir, "1442", "content.md"), r"D:\New folder\nuclear_article_clean.txt")
]

for html, out in jobs:
    clean_file(html, out)
