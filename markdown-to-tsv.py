#!/usr/bin/env python3
"""
Convert markdown inventory files to TSV format for asset database import.
Processes markdown tables and extracts inventory data.
"""

import re
import csv
import sys
import os
from pathlib import Path
import argparse
from datetime import datetime

def parse_markdown_table(content, section_name):
    """Parse a markdown table and return rows as dictionaries."""
    items = []
    
    # Find the section
    section_pattern = rf'## {section_name}\s*\n'
    section_match = re.search(section_pattern, content, re.IGNORECASE)
    
    if not section_match:
        return items
    
    # Extract content from this section until next section or end
    start_pos = section_match.end()
    next_section = re.search(r'\n## ', content[start_pos:])
    
    if next_section:
        section_content = content[start_pos:start_pos + next_section.start()]
    else:
        section_content = content[start_pos:]
    
    # Find table
    table_pattern = r'\|([^|]+\|)+\s*\n\|[-\s|:]+\|\s*\n((?:\|[^|]*\|.*\n?)*)'
    table_match = re.search(table_pattern, section_content)
    
    if not table_match:
        return items
    
    # Parse header
    header_line = table_match.group(0).split('\n')[0]
    headers = [h.strip() for h in header_line.split('|')[1:-1]]
    
    # Parse data rows
    data_section = table_match.group(2)
    for line in data_section.strip().split('\n'):
        if line.strip() and '|' in line:
            values = [v.strip() for v in line.split('|')[1:-1]]
            if values and values[0]:  # Skip empty rows
                item = dict(zip(headers, values))
                item['Category'] = section_name
                items.append(item)
    
    return items

def extract_shop_name(content):
    """Extract shop name from markdown title."""
    title_match = re.search(r'^#\s*(.+)', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return "Unknown Shop"

def process_markdown_file(file_path):
    """Process a single markdown file and extract all inventory items."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        shop_name = extract_shop_name(content)
        all_items = []
        
        # Process each section
        sections = ['Equipment', 'Tools', 'Supplies', 'Consumables']
        for section in sections:
            items = parse_markdown_table(content, section)
            for item in items:
                item['Shop'] = shop_name
                item['Source_File'] = os.path.basename(file_path)
                all_items.append(item)
        
        return all_items
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return []

def write_tsv(items, output_file):
    """Write items to TSV file."""
    if not items:
        print("No items to write.")
        return
    
    # Get all unique fields
    all_fields = set()
    for item in items:
        all_fields.update(item.keys())
    
    # Standard field order
    standard_fields = ['Shop', 'Category', 'Item', 'Model/Part Number', 'Serial Number', 
                      'Purchase Date', 'Purchase Price', 'Current Value', 'Location', 
                      'Condition', 'Quantity', 'Unit Cost', 'Total Value', 'Expiration Date', 
                      'Notes', 'Source_File']
    
    # Arrange fields with standard ones first
    fieldnames = [f for f in standard_fields if f in all_fields]
    fieldnames.extend([f for f in all_fields if f not in standard_fields])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(items)

def main():
    parser = argparse.ArgumentParser(description='Convert markdown inventory to TSV')
    parser.add_argument('input', nargs='*', help='Input markdown files or directories')
    parser.add_argument('-o', '--output', default='inventory.tsv', help='Output TSV file')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process directories recursively')
    
    args = parser.parse_args()
    
    if not args.input:
        # Default to current directory src folder
        args.input = ['src/']
    
    all_items = []
    
    for input_path in args.input:
        path = Path(input_path)
        
        if path.is_file() and path.suffix == '.md':
            all_items.extend(process_markdown_file(path))
        elif path.is_dir():
            pattern = '**/*.md' if args.recursive else '*.md'
            for md_file in path.glob(pattern):
                if 'inventory' in md_file.name.lower() or 'equipment' in md_file.name.lower() or 'tools' in md_file.name.lower():
                    all_items.extend(process_markdown_file(md_file))
    
    if all_items:
        write_tsv(all_items, args.output)
        print(f"Processed {len(all_items)} items and wrote to {args.output}")
    else:
        print("No inventory items found in the specified files.")

if __name__ == '__main__':
    main()