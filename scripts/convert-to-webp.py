#!/usr/bin/env python3
"""Convert img src to picture element with WebP and JPEG fallback"""
import re
import os
import glob

def convert_img_to_picture(html_content):
    """Convert <img src="*.jpg"> to <picture> with WebP source"""
    
    def replace_img(match):
        full_tag = match.group(0)
        src = match.group(1)
        
        # Skip if already a picture element or if no .jpg extension
        if 'picture' in full_tag.lower() or '.jpg' not in src.lower():
            return full_tag
        
        # Extract other attributes
        attrs = re.findall(r'(\w+)="([^"]*)"', full_tag)
        attrs_dict = {k: v for k, v in attrs if k != 'src'}
        
        # Build picture element
        webp_src = src.replace('.jpg', '.webp')
        
        # Construct picture element
        picture_parts = ['<picture>']
        picture_parts.append(f'  <source srcset="{webp_src}" type="image/webp">')
        
        # Reconstruct img tag with all original attributes
        img_attrs = ' '.join([f'{k}="{v}"' for k, v in attrs_dict.items()])
        picture_parts.append(f'  <img src="{src}" {img_attrs}>')
        picture_parts.append('</picture>')
        
        return '\n'.join(picture_parts)
    
    # Match img tags with .jpg src
    pattern = r'<img\s+[^>]*src="([^"]*\.jpg)"[^>]*>'
    return re.sub(pattern, replace_img, html_content)

def process_html_files():
    """Process all HTML files in the project"""
    project_dir = '/home/amram/WEBSITE'
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(project_dir, '*.html'))
    html_files += glob.glob(os.path.join(project_dir, '**/*.html'), recursive=True)
    
    converted = 0
    for html_file in html_files:
        if 'node_modules' in html_file or '.git' in html_file:
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has .jpg images
        if '.jpg' not in content:
            continue
            
        # Convert
        new_content = convert_img_to_picture(content)
        
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            converted += 1
            print(f"✓ Converted: {os.path.basename(html_file)}")
    
    return converted

if __name__ == '__main__':
    print("Converting images to WebP with fallback...")
    converted = process_html_files()
    print(f"\nConverted {converted} files")
