import re
import os

html_path = r"C:\Users\Aditya\.gemini\antigravity\brain\4c0fa76b-dbaf-4919-a30a-dd50e654dca9\.system_generated\steps\1454\content.md"

if not os.path.exists(html_path):
    print(f"Path does not exist: {html_path}")
    exit(1)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all href links containing /p/
links = re.findall(r'https://decodingthedragon\.substack\.com/p/[a-zA-Z0-9\-]+', content)
unique_links = list(set(links))

print(f"Discovered {len(unique_links)} articles:")
for link in sorted(unique_links):
    print(link)
