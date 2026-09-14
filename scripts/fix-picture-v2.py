#!/usr/bin/env python3
"""Fix nested picture elements - version 2"""
import re
import os
import glob

def fix_picture_elements(html_content):
    """Fix nested picture elements"""
    
    # Multiple passes to flatten nested elements
    for _ in range(20):
        # Pattern to match nested picture elements
        pattern = r'<picture>\s*<picture>'
        if re.search(pattern, html_content):
            # Replace nested picture with single picture
            html_content = re.sub(
                r'<picture>\s*<picture>(.*?)</picture>\s*</picture>',
                r'<picture>\1</picture>',
                html_content,
                flags=re.DOTALL
            )
        else:
            break
    
    return html_content

def process_html_files():
    """Process all HTML files in the project"""
    project_dir = '/home/amram/WEBSITE'
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(project_dir, '*.html'))
    html_files += glob.glob(os.path.join(project_dir, '**/*.html'), recursive=True)
    
    fixed = 0
    for html_file in html_files:
        if 'node_modules' in html_file or '.git' in html_file:
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has nested picture elements
        if '<picture>\s*<picture>' not in content and not re.search(r'<picture>\s*<picture>', content):
            continue
            
        # Fix
        new_content = fix_picture_elements(content)
        
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f"✓ Fixed: {os.path.basename(html_file)}")
    
    return fixed

if __name__ == '__main__':
    print("Fixing nested picture elements (v2)...")
    fixed = process_html_files()
    print(f"\nFixed {fixed} files")
