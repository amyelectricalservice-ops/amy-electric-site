#!/usr/bin/env python3
"""Fix nested picture elements - version 3"""
import re
import os
import glob

def fix_picture_elements(html_content):
    """Fix nested picture elements by rebuilding them properly"""
    
    # Pattern to find picture elements with nested picture elements
    # We'll use a more aggressive approach: find all picture blocks and rebuild them
    
    def rebuild_picture(match):
        """Rebuild a picture element from its content"""
        content = match.group(0)
        
        # Extract all source elements
        sources = re.findall(r'<source[^>]*>', content)
        
        # Extract the img element
        img_match = re.search(r'<img[^>]*>', content)
        if not img_match:
            return content
        img_tag = img_match.group(0)
        
        # Build new picture element
        new_picture = '<picture>\n'
        for source in sources:
            new_picture += f'  {source}\n'
        new_picture += f'  {img_tag}\n'
        new_picture += '</picture>'
        
        return new_picture
    
    # Keep processing until no nested elements remain
    max_iterations = 20
    for i in range(max_iterations):
        # Check for nested picture elements
        if not re.search(r'<picture>.*<picture>.*</picture>.*</picture>', html_content, re.DOTALL):
            break
        
        # Replace nested picture elements
        html_content = re.sub(
            r'<picture>(.*?)<picture>(.*?)</picture>(.*?)</picture>',
            lambda m: f'<picture>{m.group(1)}{m.group(2)}{m.group(3)}</picture>',
            html_content,
            flags=re.DOTALL
        )
    
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
        if not re.search(r'<picture>.*<picture>.*</picture>.*</picture>', content, re.DOTALL):
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
    print("Fixing nested picture elements (v3)...")
    fixed = process_html_files()
    print(f"\nFixed {fixed} files")
