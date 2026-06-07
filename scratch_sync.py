import os
import shutil

dashboard_dir = "dashboard"
files_to_copy = ["index.html", "style_v2.css", "app.js"]

print("Synchronizing UI template files to all query subdirectories...")
if not os.path.exists(dashboard_dir):
    print("Dashboard directory not found.")
    exit(1)

subdirs = [d for d in os.listdir(dashboard_dir) if os.path.isdir(os.path.join(dashboard_dir, d))]
for s in subdirs:
    dest_dir = os.path.join(dashboard_dir, s)
    # Verify it is indeed an archive folder by checking for forensic_report.json
    if os.path.exists(os.path.join(dest_dir, "forensic_report.json")):
        for filename in files_to_copy:
            src_path = os.path.join(dashboard_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                print(f"Copied {filename} to {s}")
print("Synchronization completed successfully!")
