import os
import json

dashboard_dir = "d:/Deep Research Agent/dashboard"
subdirs = ["incred_holdings_udrhp", "jewar_airport_future", "kshitij_polylines_stock", "zepto_business_model", "zepto_ipo"]

for s in subdirs:
    json_path = os.path.join(dashboard_dir, s, "forensic_report.json")
    print(f"\n==================================================")
    print(f"FOLDER: {s}")
    print(f"==================================================")
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            subject = data.get("subject", "N/A")
            brief = data.get("executive_brief", "")[:300]
            print(f"Subject: {subject}".encode('ascii', errors='replace').decode('ascii'))
            print(f"Executive Brief: {brief}...".encode('ascii', errors='replace').decode('ascii'))
            
            print(f"\nAnomalies Deconstructed ({len(data.get('anomalies', []))}):")
            for idx, anom in enumerate(data.get('anomalies', []), 1):
                claim = anom.get('source_claim', 'N/A')
                reality = anom.get('reality', 'N/A')
                sev = anom.get('severity', 'N/A')
                print(f"  {idx}. Claim: {claim}".encode('ascii', errors='replace').decode('ascii'))
                print(f"     Reality: {reality}".encode('ascii', errors='replace').decode('ascii'))
                print(f"     Severity: {sev}".encode('ascii', errors='replace').decode('ascii'))
            
            print("\nTracks Summary:")
            tracks = data.get('tracks', {})
            for track_name, track_val in tracks.items():
                text = track_val.get('text', '') if isinstance(track_val, dict) else str(track_val)
                print(f"  - {track_name.upper()} (first 200 chars): {text[:200]}...".encode('ascii', errors='replace').decode('ascii'))
            
            print("\nCitations:")
            for cit in data.get('citations', []):
                name = cit.get('name', 'N/A')
                url = cit.get('url', 'N/A')
                print(f"  - {name}: {url}".encode('ascii', errors='replace').decode('ascii'))
        except Exception as e:
            print(f"Error reading JSON: {e}")
    else:
        print("No forensic_report.json found")
