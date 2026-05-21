#!/usr/bin/env python3

"""
IFP Workshop v2.1 Screenshot Integration Script

Wires extracted v2.1 screenshots into HTML pages at predefined locations.
Usage: python3 wire-screenshots.py

This script:
1. Reads extracted screenshots from img/v2.1-screenshots/
2. Finds placeholder sections in HTML pages (or specific <figure> tags)
3. Wires screenshots with updated captions
4. Creates backup of original files

Configuration is defined below.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Extraction configuration
# Format: {
#   'filename': 'screenshot-name.jpg',
#   'pages': ['docs/page1.html'],  # Pages to insert into
#   'alt_text': 'Description for accessibility',
#   'caption': 'Caption text',
#   'section_marker': '<h2>Specific Section Title</h2>',  # Where to insert (optional)
# }

SCREENSHOTS = [
    {
        'filename': 'app-framework-overview.jpg',
        'pages': ['docs/03-ifp-overview.html'],
        'alt_text': 'IFP Application Framework overview showing 44 configurations, 4 models, 17 assets',
        'caption': 'IFP Application Framework overview (v2.1) — 44 configurations, 4 models, 17 assets',
        'section_marker': '<h2>App Framework Overview</h2>',
    },
    {
        'filename': 'hierarchy-list.jpg',
        'pages': ['docs/03-ifp-overview.html'],
        'alt_text': 'IFP hierarchy lists showing Entity, Account, Location, Customer, Job with levels',
        'caption': 'IFP hierarchy lists (v2.1) — Entity, Account, Location, Customer, Job with default levels',
        'section_marker': '<h2>IFP Hierarchy Lists</h2>',
    },
    {
        'filename': 'system-modules.jpg',
        'pages': ['docs/03-ifp-overview.html'],
        'alt_text': 'IFP system modules (SYS prefix) list after v2.1 generation',
        'caption': 'IFP system modules (SYS prefix) list after v2.1 generation',
        'section_marker': '<h2>SYS Modules After Generation</h2>',
    },
    {
        'filename': 'configurator-walkthrough.jpg',
        'pages': ['docs/05-configurator-walkthrough.html'],
        'alt_text': 'App Framework Configurator showing Location dimension (formerly Geography)',
        'caption': 'App Framework Configurator (v2.1) — showing Location dimension, Customer, Job options',
        'section_marker': '<h2>Configurator Section</h2>',
    },
]

def create_figure_html(filename, alt_text, caption):
    """Generate HTML for a screenshot figure."""
    rel_path = f"../img/v2.1-screenshots/{filename}"
    return f'''<figure class="screenshot"><img src="{rel_path}" alt="{alt_text}" style="width:100%;border-radius:6px;border:1px solid #e2e8f0;"><figcaption style="font-size:0.8rem;color:#6b7280;margin-top:0.4rem;text-align:center;">{caption}</figcaption></figure>'''

def wire_screenshot(page_path, screenshot_config):
    """Wire a screenshot into a specific page."""
    if not os.path.exists(page_path):
        print(f"  ⚠️  Page not found: {page_path}")
        return False
    
    with open(page_path, 'r') as f:
        content = f.read()
    
    # Check if screenshot filename exists
    img_path = f"img/v2.1-screenshots/{screenshot_config['filename']}"
    if not os.path.exists(img_path):
        print(f"  ⚠️  Screenshot not found: {img_path}")
        return False
    
    # Create backup
    backup_path = f"{page_path}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    with open(backup_path, 'w') as f:
        f.write(content)
    
    # Generate figure HTML
    figure_html = create_figure_html(
        screenshot_config['filename'],
        screenshot_config['alt_text'],
        screenshot_config['caption']
    )
    
    # Find insertion point (after section marker if provided)
    if 'section_marker' in screenshot_config:
        marker = screenshot_config['section_marker']
        if marker in content:
            # Insert after marker
            insertion_point = content.find(marker) + len(marker)
            content = content[:insertion_point] + '\n' + figure_html + '\n' + content[insertion_point:]
            print(f"  ✅ Wired into section: {screenshot_config['section_marker']}")
        else:
            print(f"  ⚠️  Section marker not found: {marker}")
            return False
    else:
        print(f"  ⚠️  No section marker provided")
        return False
    
    # Write back
    with open(page_path, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main entry point."""
    print("🎬 IFP Workshop v2.1 Screenshot Integration")
    print("=" * 60)
    print()
    
    # Verify screenshots exist
    missing = []
    for screenshot in SCREENSHOTS:
        img_path = f"img/v2.1-screenshots/{screenshot['filename']}"
        if not os.path.exists(img_path):
            missing.append(img_path)
    
    if missing:
        print("❌ Missing screenshots:")
        for path in missing:
            print(f"   {path}")
        print()
        print("Run extract-screenshots.sh first to generate screenshots.")
        return False
    
    print("✅ All screenshots found")
    print()
    
    # Wire each screenshot
    success_count = 0
    total = sum(len(s['pages']) for s in SCREENSHOTS)
    
    for screenshot in SCREENSHOTS:
        print(f"📷 {screenshot['filename']}")
        for page in screenshot['pages']:
            if wire_screenshot(page, screenshot):
                success_count += 1
            else:
                print(f"   ❌ Failed to wire into {page}")
        print()
    
    print("=" * 60)
    print(f"✅ Integration complete: {success_count}/{total} wired successfully")
    print()
    print("Next steps:")
    print("1. Review updated pages in docs/")
    print("2. Test screenshot display (check alignment, visibility)")
    print("3. Verify captions are accurate")
    print("4. Commit changes: git add docs/ && git commit -m 'Wire v2.1 screenshots'")
    print()

if __name__ == '__main__':
    main()
