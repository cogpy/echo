#!/usr/bin/env python3
"""
Convert deep_tree_echo_dan_conversation.jsonl to Scheme (.scm) format.

This script transforms the ChatGPT conversation export JSON into Scheme s-expressions
while preserving the hierarchical message structure and all metadata.
"""

import json
import sys
import re
from datetime import datetime
from typing import Dict, Any, List, Optional


def escape_scheme_string(text: str) -> str:
    """Escape special characters for Scheme string literals."""
    if not isinstance(text, str):
        return str(text)
    
    # Escape backslashes and quotes
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    
    # Handle newlines and special characters
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    
    return text


def format_scheme_value(value: Any, indent_level: int = 0) -> str:
    """Convert Python values to Scheme representation."""
    indent = "  " * indent_level
    
    if value is None:
        return "#f"
    elif isinstance(value, bool):
        return "#t" if value else "#f"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return f'"{escape_scheme_string(value)}"'
    elif isinstance(value, list):
        if not value:
            return "'()"
        items = []
        for item in value:
            items.append(format_scheme_value(item, indent_level + 1))
        if len(items) == 1:
            return f"(list {items[0]})"
        return f"(list\n{indent}  " + f"\n{indent}  ".join(items) + f"\n{indent})"
    elif isinstance(value, dict):
        if not value:
            return "'()"
        pairs = []
        for key, val in value.items():
            key_str = f'"{escape_scheme_string(str(key))}"'
            val_str = format_scheme_value(val, indent_level + 1)
            pairs.append(f"({key_str} . {val_str})")
        
        if len(pairs) == 1:
            return f"(alist {pairs[0]})"
        return f"(alist\n{indent}  " + f"\n{indent}  ".join(pairs) + f"\n{indent})"
    else:
        return f'"{escape_scheme_string(str(value))}"'


def convert_message_to_scheme(msg_id: str, msg_data: Dict[str, Any], indent_level: int = 1) -> str:
    """Convert a single message to Scheme format."""
    indent = "  " * indent_level
    
    # Extract message content
    message_obj = msg_data.get('message')
    if not message_obj:
        content = "#f"
        role = "#f"
        timestamp = "#f"
    else:
        role = message_obj.get('author', {}).get('role', 'unknown')
        role = f'"{escape_scheme_string(role)}"'
        
        content_obj = message_obj.get('content', {})
        if isinstance(content_obj, dict) and 'parts' in content_obj:
            parts = content_obj.get('parts', [])
            if parts and parts[0]:
                content = f'"{escape_scheme_string(parts[0])}"'
            else:
                content = '""'
        else:
            content = f'"{escape_scheme_string(str(content_obj))}"'
        
        # Convert timestamp
        create_time = message_obj.get('create_time')
        timestamp = str(create_time) if create_time else "#f"
    
    # Handle parent and children
    parent = msg_data.get('parent')
    parent_str = f'"{escape_scheme_string(parent)}"' if parent else "#f"
    
    children = msg_data.get('children', [])
    if children:
        children_list = " ".join(f'"{escape_scheme_string(child)}"' for child in children)
        children_str = f"(list {children_list})"
    else:
        children_str = "'()"
    
    return f"""("{escape_scheme_string(msg_id)}"
{indent}  (role . {role})
{indent}  (content . {content})
{indent}  (timestamp . {timestamp})
{indent}  (parent . {parent_str})
{indent}  (children . {children_str}))"""


def convert_conversation_to_scheme(conversation: Dict[str, Any]) -> str:
    """Convert the entire conversation to Scheme format."""
    
    # Header and metadata
    title = conversation.get('title', 'Untitled Conversation')
    create_time = conversation.get('create_time', 0)
    update_time = conversation.get('update_time', 0)
    conversation_id = conversation.get('conversation_id', '')
    current_node = conversation.get('current_node', '')
    
    # Convert create/update times to readable format
    try:
        create_date = datetime.fromtimestamp(create_time).isoformat() if create_time else ''
        update_date = datetime.fromtimestamp(update_time).isoformat() if update_time else ''
    except (ValueError, TypeError):
        create_date = str(create_time)
        update_date = str(update_time)
    
    # Start building the Scheme representation
    scheme_output = [
        ';; Deep Tree Echo Conversation - Converted from JSON',
        f';; Title: {title}',
        f';; Created: {create_date}',
        f';; Updated: {update_date}',
        f';; Total Messages: {len(conversation.get("mapping", {}))}',
        '',
        '(define deep-tree-echo-conversation',
        '  (list'
    ]
    
    # Add metadata
    scheme_output.extend([
        f'    (cons "title" "{escape_scheme_string(title)}")',
        f'    (cons "create-time" {create_time})',
        f'    (cons "update-time" {update_time})',
        f'    (cons "conversation-id" "{escape_scheme_string(conversation_id)}")',
        f'    (cons "current-node" "{escape_scheme_string(current_node)}")',
    ])
    
    # Add messages
    mapping = conversation.get('mapping', {})
    if mapping:
        scheme_output.append('    (cons "messages" (list')
        
        for msg_id, msg_data in mapping.items():
            msg_scheme = convert_message_to_scheme(msg_id, msg_data, indent_level=3)
            scheme_output.append(f'      {msg_scheme}')
        
        scheme_output.append('    ))')
    else:
        scheme_output.append('    (cons "messages" \'())')
    
    # Close the main structure
    scheme_output.extend([
        '  ))',
        '',
        ';; Helper functions for accessing conversation data',
        '(define (get-conversation-title) (cdr (assoc "title" deep-tree-echo-conversation)))',
        '(define (get-messages) (cdr (assoc "messages" deep-tree-echo-conversation)))',
        '(define (get-message id) (assoc id (get-messages)))',
        '(define (get-message-content id)',
        '  (let ((msg (get-message id)))',
        '    (if msg (cdr (assoc "content" (cdr msg))) #f)))',
        '(define (get-message-role id)',
        '  (let ((msg (get-message id)))',
        '    (if msg (cdr (assoc "role" (cdr msg))) #f)))',
        '',
        ';; Export the conversation',
        'deep-tree-echo-conversation'
    ])
    
    return '\n'.join(scheme_output)


def main():
    """Main conversion function."""
    input_file = '/home/runner/work/echo/echo/data/conversations/deep_tree_echo_dan_conversation.jsonl'
    output_file = '/home/runner/work/echo/echo/data/conversations/deep_tree_echo_dan_conversation.scm'
    
    try:
        # Load the JSON conversation
        print(f"Loading conversation from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
        
        print(f"Converting conversation: {conversation.get('title', 'Untitled')}")
        print(f"Total messages: {len(conversation.get('mapping', {}))}")
        
        # Convert to Scheme
        scheme_content = convert_conversation_to_scheme(conversation)
        
        # Write the output
        print(f"Writing Scheme output to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(scheme_content)
        
        print("Conversion completed successfully!")
        print(f"Output size: {len(scheme_content)} characters")
        
        # Validate parentheses balance
        open_count = scheme_content.count('(')
        close_count = scheme_content.count(')')
        print(f"Parentheses balance: {open_count} open, {close_count} close, balanced: {open_count == close_count}")
        
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()