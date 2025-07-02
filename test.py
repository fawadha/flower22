import os
import re

# Regex for href or src attributes in HTML or JS files
ATTR_PATTERN = re.compile(
    r'(?P<before>(?:href|src)\s*=\s*")[/]([^"]+)"',
    re.IGNORECASE
)

# Regex for url(...) in CSS files
CSS_URL_PATTERN = re.compile(
    r'(url\()\s*[/]([^)\s]+)(\))',
    re.IGNORECASE
)

def make_paths_relative_in_html_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = ATTR_PATTERN.sub(r'\1\2"', content)

    if content != new_content:
        print(f"✔ Updated: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def make_paths_relative_in_css(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = CSS_URL_PATTERN.sub(r'\1\2\3', content)

    if content != new_content:
        print(f"✔ Updated: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_files(root_dir):
    total_files = 0
    updated_files = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            ext = file.lower().split('.')[-1]
            if ext in ('html', 'js', 'css'):
                total_files += 1
                file_path = os.path.join(root, file)
                if ext == 'css':
                    updated = make_paths_relative_in_css(file_path)
                else:
                    updated = make_paths_relative_in_html_js(file_path)

                if updated:
                    updated_files += 1
                print(f"Scanned: {total_files} files, Updated: {updated_files}", end='\r')
    print()  # newline after progress

if __name__ == "__main__":
    target_folder = "./"  # Replace with your folder path
    process_files(target_folder)
    print("Processing complete.")
