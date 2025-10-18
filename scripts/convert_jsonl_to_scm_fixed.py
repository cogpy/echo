#!/usr/bin/env python3
"""
Convert deep_tree_echo_dan_conversation.jsonl to Scheme (.scm) format - Fixed version.
"""

import json
import sys
from datetime import datetime


def escape_scheme_string(text: str) -> str:
    """Escape special characters for Scheme string literals."""
    if not isinstance(text, str):
        return str(text)
    
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    
    return text


def convert_message_to_scheme(msg_id: str, msg_data: dict) -> str:
    """Convert a single message to Scheme format."""
    
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
        
        timestamp = str(message_obj.get('create_time', '#f'))
    
    # Handle parent and children
    parent = msg_data.get('parent')
    parent_str = f'"{escape_scheme_string(parent)}"' if parent else "#f"
    
    children = msg_data.get('children', [])
    if children:
        children_items = " ".join(f'"{escape_scheme_string(child)}"' for child in children)
        children_str = f"(list {children_items})"
    else:
        children_str = "'()"
    
    return f"""      ("{escape_scheme_string(msg_id)}" (role . {role}) (content . {content}) (timestamp . {timestamp}) (parent . {parent_str}) (children . {children_str}))"""


def convert_conversation_to_scheme(conversation: dict) -> str:
    """Convert the entire conversation to Scheme format."""
    
    title = conversation.get('title', 'Untitled Conversation')
    create_time = conversation.get('create_time', 0)
    update_time = conversation.get('update_time', 0)
    conversation_id = conversation.get('conversation_id', '')
    current_node = conversation.get('current_node', '')
    
    # Convert timestamps
    try:
        create_date = datetime.fromtimestamp(create_time).isoformat() if create_time else ''
        update_date = datetime.fromtimestamp(update_time).isoformat() if update_time else ''
    except (ValueError, TypeError):
        create_date = str(create_time)
        update_date = str(update_time)
    
    # Build Scheme representation
    lines = [
        ';; Deep Tree Echo Conversation - Converted from JSON',
        f';; Title: {title}',
        f';; Created: {create_date}',
        f';; Updated: {update_date}',
        f';; Total Messages: {len(conversation.get("mapping", {}))}',
        '',
        '(define deep-tree-echo-conversation',
        '  (list',
        f'    (cons "title" "{escape_scheme_string(title)}")',
        f'    (cons "create-time" {create_time})',
        f'    (cons "update-time" {update_time})',
        f'    (cons "conversation-id" "{escape_scheme_string(conversation_id)}")',
        f'    (cons "current-node" "{escape_scheme_string(current_node)}")',
        '    (cons "messages" (list'
    ]
    
    # Add messages
    mapping = conversation.get('mapping', {})
    for msg_id, msg_data in mapping.items():
        msg_scheme = convert_message_to_scheme(msg_id, msg_data)
        lines.append(msg_scheme)
    
    # Close structure
    lines.extend([
        '    ))',  # Close messages list
        '  ))',    # Close main list  
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
    
    return '\n'.join(lines)


def main():
    """Main conversion function."""
    input_file = '/home/runner/work/echo/echo/data/conversations/deep_tree_echo_dan_conversation.jsonl'
    output_file = '/home/runner/work/echo/echo/data/conversations/deep_tree_echo_dan_conversation.scm'
    
    try:
        print(f"Loading conversation from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
        
        print(f"Converting conversation: {conversation.get('title', 'Untitled')}")
        print(f"Total messages: {len(conversation.get('mapping', {}))}")
        
        scheme_content = convert_conversation_to_scheme(conversation)
        
        print(f"Writing Scheme output to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(scheme_content)
        
        # Validate balance
        open_count = scheme_content.count('(')
        close_count = scheme_content.count(')')
        
        print("Conversion completed successfully!")
        print(f"Output size: {len(scheme_content)} characters")
        print(f"Parentheses balance: {open_count} open, {close_count} close, balanced: {open_count == close_count}")
        
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()