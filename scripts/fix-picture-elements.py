#!/usr/bin/env python3
"""Fix nested picture elements and ensure proper WebP fallback"""
import re
import os
import glob

def fix_picture_elements(html_content):
    """Fix nested picture elements and ensure proper structure"""
    
    # Remove all nested picture elements and rebuild properly
    # First, find all picture blocks and extract their content
    
    def extract_picture_content(match):
        """Extract the inner content of a picture element"""
        content = match.group(1)
        return content
    
    # Pattern to match picture elements (including nested ones)
    # We'll do multiple passes to flatten nested elements
    
    max_passes = 10
    for _ in range(max_passes):
        # Match nested picture elements
        pattern = r'<picture>\s*<picture>(.*?)</picture>\s*</picture>'
        new_content = re.sub(pattern, r'<picture>\1</picture>', html_content, flags=re.DOTALL)
        if new_content == html_content:
            break
        html_content = new_content
    
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
        
        # Check if file has picture elements
        if '<picture>' not in content:
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
    print("Fixing nested picture elements...")
    fixed = process_html_files()
    print(f"\nFixed {fixed} files")
