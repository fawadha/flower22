import os
import re

# Match tags containing href or src="/wp-content/..."
PATTERN = re.compile(
    r'(?P<before><[^>]+\s(?:href|src)\s*=\s*")/wp-content/(?P<rest>[^"]+)(")',
    re.IGNORECASE
)

def replace_wp_content_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = PATTERN.sub(r'\g<before>wp-content/\g<rest>\g<3>', content)

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
                if replace_wp_content_paths(file_path):
                    updated_files += 1
                print(f"Scanned: {total_files} files, Updated: {updated_files}", end='\r')
    print()  # Newline after progress

if __name__ == "__main__":
    target_folder = "./"  # Replace with your folder path
    process_all_index_html(target_folder)
    print("Processing complete.")