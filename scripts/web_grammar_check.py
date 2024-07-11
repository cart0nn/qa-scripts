import os
from bs4 import BeautifulSoup
import language_tool_python
import time
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_div_text(file_content):
    soup = BeautifulSoup(file_content, 'html.parser')
    div_texts = [div.get_text() for div in soup.find_all('div')]
    return div_texts

def check_grammar(tool, text):
    matches = tool.check(text)
    return text, matches

def process_tsx_files(directory):
    grammar_issues = {}
    file_count = 0
    start_time = time.time()
    tool = language_tool_python.LanguageTool('en-US')  # Initialize once

    with ThreadPoolExecutor(max_workers=4) as executor:  # Limit number of threads
        future_to_text = {}

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.tsx'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        div_texts = extract_div_text(file_content)
                        for div_text in div_texts:
                            future = executor.submit(check_grammar, tool, div_text)
                            future_to_text[future] = (file_path, div_text)

                    # Logging progress
                    file_count += 1
                    if file_count % 10 == 0:
                        print(f"Processed {file_count} files. Time elapsed: {time.time() - start_time:.2f} seconds")

        for future in as_completed(future_to_text):
            file_path, div_text = future_to_text[future]
            _, issues = future.result()
            if issues:
                if file_path not in grammar_issues:
                    grammar_issues[file_path] = []
                grammar_issues[file_path].append((div_text, issues))

    total_time = time.time() - start_time
    print(f"Total files processed: {file_count}")
    print(f"Total time taken: {total_time:.2f} seconds")

    return grammar_issues

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()
    return directory

def write_issues_to_file(grammar_issues, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path, issues in grammar_issues.items():
            f.write(f"File: {file_path}\n")
            for div_text, issue_list in issues:
                # Filter out the specific issue
                filtered_issues = [issue for issue in issue_list if issue.message != "Possible typo: you repeated a whitespace"]
                if filtered_issues:  # Only write if there are issues other than the filtered one
                    f.write(f"Text: {div_text}\n")
                    for issue in filtered_issues:
                        f.write(f"Issue: {issue.message}\n")
                    f.write("\n")
            f.write("\n")

# Prompt the user to select a directory
directory = select_directory()

if directory:
    # Process .tsx files and get grammar issues
    grammar_issues = process_tsx_files(directory)

    # Write grammar issues to a text file
    output_file = 'grammar_issues.txt'
    write_issues_to_file(grammar_issues, output_file)

    print(f"Grammar issues written to {output_file}")
else:
    print("No directory selected.")