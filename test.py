import os
import re

# Regex to match href or src attributes that start with a slash (/)
# Example: href="/path/to/file.css"  -->  href="path/to/file.css"
PATTERN = re.compile(
    r'(?P<before><[^>]+\s(?:href|src)\s*=\s*")/(?P<path>[^"]+)(")',
    re.IGNORECASE
)

def make_paths_relative(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = PATTERN.sub(r'\g<before>\g<path>\3', content)

    if content != new_content:
        print(f"✔ Updated: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_all_index_html(root_dir):
    total_files = 0
    updated_files = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'index.html':
                total_files += 1
                file_path = os.path.join(root, file)
                if make_paths_relative(file_path):
                    updated_files += 1
                print(f"Scanned: {total_files} files, Updated: {updated_files}", end='\r')
    print()  # for newline after progress

if __name__ == "__main__":
    target_folder = "./"  # Replace with your folder path
    process_all_index_html(target_folder)
    print("Processing complete.")
