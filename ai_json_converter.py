import os
import json
import re
from typing import Dict, List, Any, Optional

def safe_filename(title: str) -> str:
    """
    Return a sanitized version of 'title' for filenames.
    Removes non-ASCII characters (including emojis),
    then replaces typical forbidden characters with '_'.
    """
    # Remove all non-ASCII (including emojis)
    title = re.sub(r'[^\\x00-\\x7F]+', '', title)
    # Replace typical forbidden characters on Windows/*nix
    return re.sub(r'[\\\\/*?:"<>|]', '_', title)

class AIJSONConverter:
    """
    A flexible converter that can handle different AI chat JSON formats
    """
    
    def __init__(self):
        self.supported_formats = {
            'claude': self._parse_claude_format,
            'generic_nested': self._parse_generic_nested_format,
            'simple_messages': self._parse_simple_messages_format,
            'chatgpt': self._parse_chatgpt_format,
            'gemini': self._parse_gemini_format
        }
    
    def detect_format(self, data: List[Dict]) -> str:
        """
        Detect the format of the JSON data
        """
        if not data or not isinstance(data, list):
            return 'unknown'
        
        sample = data[0]
        
        # Check for Claude format
        if 'uuid' in sample and 'chat_messages' in sample:
            return 'claude'
        
        # Check for ChatGPT format
        if 'title' in sample and 'mapping' in sample:
            return 'chatgpt'
        
        # Check for Gemini format (hypothetical)
        if 'conversation_id' in sample and 'turns' in sample:
            return 'gemini'
        
        # Check for generic nested format (like your example)
        if 'chat' in sample and 'history' in sample.get('chat', {}):
            return 'generic_nested'
        
        # Check for simple messages format
        if 'messages' in sample and isinstance(sample['messages'], list):
            return 'simple_messages'
        
        return 'unknown'
    
    def _parse_claude_format(self, chat: Dict) -> Optional[Dict]:
        """Parse Claude.ai format"""
        chat_id = chat.get('uuid', 'unknown')
        title = chat.get('name', '') or ''
        messages = chat.get('chat_messages', [])
        
        if not title or not messages:
            return None
        
        parsed_messages = []
        for message in messages:
            if not isinstance(message, dict) or 'sender' not in message or 'content' not in message:
                continue
            
            sender = message['sender']
            contents = message['content']
            
            for content in contents:
                if not isinstance(content, dict) or 'text' not in content:
                    continue
                text = content['text']
                parsed_messages.append({
                    'role': sender,
                    'content': text
                })
        
        return {
            'id': chat_id,
            'title': title,
            'messages': parsed_messages
        }
    
    def _parse_chatgpt_format(self, chat: Dict) -> Optional[Dict]:
        """Parse ChatGPT format"""
        chat_id = chat.get('id', 'unknown')
        title = chat.get('title', '') or ''
        mapping = chat.get('mapping', {})
        
        if not title or not mapping:
            return None
        
        # Extract messages from mapping
        messages_with_order = []
        for node_id, node_data in mapping.items():
            if not isinstance(node_data, dict):
                continue
                
            message = node_data.get('message')
            if not message or not isinstance(message, dict):
                continue
                
            author = message.get('author', {})
            role = author.get('role', 'unknown')
            
            content = message.get('content', {})
            if isinstance(content, dict) and 'parts' in content:
                text = ' '.join(content['parts'])
            else:
                text = str(content) if content else ''
            
            if text.strip() and role != 'system':
                create_time = message.get('create_time', 0)
                messages_with_order.append((create_time, {
                    'role': role,
                    'content': text.strip()
                }))
        
        # Sort by creation time
        messages_with_order.sort(key=lambda x: x[0])
        parsed_messages = [msg for _, msg in messages_with_order]
        
        return {
            'id': chat_id,
            'title': title,
            'messages': parsed_messages
        }
    
    def _parse_gemini_format(self, chat: Dict) -> Optional[Dict]:
        """Parse Gemini format (hypothetical structure)"""
        chat_id = chat.get('conversation_id', 'unknown')
        title = chat.get('title', '') or ''
        turns = chat.get('turns', [])
        
        if not title or not turns:
            return None
        
        parsed_messages = []
        for turn in turns:
            if not isinstance(turn, dict):
                continue
                
            role = turn.get('role', 'unknown')
            content = turn.get('content', '')
            
            if content.strip():
                parsed_messages.append({
                    'role': role,
                    'content': content.strip()
                })
        
        return {
            'id': chat_id,
            'title': title,
            'messages': parsed_messages
        }
    
    def _parse_generic_nested_format(self, chat: Dict) -> Optional[Dict]:
        """Parse generic nested format (like your example)"""
        chat_id = chat.get('id', 'unknown')
        title = chat.get('title', '') or ''
        
        # Navigate to messages
        messages_dict = chat.get('chat', {}).get('history', {}).get('messages', {})
        
        if not title or not messages_dict:
            return None
        
        # Convert messages dict to list and sort by timestamp
        messages_list = []
        for msg_id, msg_data in messages_dict.items():
            if isinstance(msg_data, dict):
                timestamp = msg_data.get('timestamp', 0)
                messages_list.append((timestamp, msg_data))
        
        # Sort by timestamp
        messages_list.sort(key=lambda x: x[0])
        
        parsed_messages = []
        for _, message in messages_list:
            role = message.get('role', 'unknown')
            
            # Handle different content formats
            content = ""
            if 'content' in message:
                if isinstance(message['content'], str):
                    content = message['content']
                elif isinstance(message['content'], list):
                    # Handle content_list format
                    for content_item in message['content']:
                        if isinstance(content_item, dict) and 'content' in content_item:
                            content += content_item['content']
            
            # Check content_list if content is empty
            if not content and 'content_list' in message:
                for content_item in message['content_list']:
                    if isinstance(content_item, dict) and 'content' in content_item:
                        content += content_item['content']
            
            if content.strip():
                parsed_messages.append({
                    'role': role,
                    'content': content.strip()
                })
        
        return {
            'id': chat_id,
            'title': title,
            'messages': parsed_messages
        }
    
    def _parse_simple_messages_format(self, chat: Dict) -> Optional[Dict]:
        """Parse simple messages format"""
        chat_id = chat.get('id', 'unknown')
        title = chat.get('title', '') or chat.get('name', '')
        messages = chat.get('messages', [])
        
        if not title or not messages:
            return None
        
        parsed_messages = []
        for message in messages:
            if isinstance(message, dict):
                role = message.get('role', 'unknown')
                content = message.get('content', '')
                
                if content.strip():
                    parsed_messages.append({
                        'role': role,
                        'content': content.strip()
                    })
        
        return {
            'id': chat_id,
            'title': title,
            'messages': parsed_messages
        }
    
    def convert_to_markdown(self, json_file: str, output_dir: str = None) -> None:
        """
        Convert AI chat JSON to markdown files
        """
        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(json_file))
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"Error: JSON file '{json_file}' does not contain a list of chats.")
                return

            # Detect format
            format_type = self.detect_format(data)
            print(f"Detected format: {format_type}")
            
            if format_type == 'unknown':
                print("Warning: Unknown format detected. Attempting generic parsing...")
                format_type = 'generic_nested'  # Fallback to generic parsing

            if format_type not in self.supported_formats:
                print(f"Error: Format '{format_type}' is not supported.")
                return

            parser = self.supported_formats[format_type]
            
            total_chats = len(data)
            processed = 0
            skipped = 0

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            for chat in data:
                parsed_chat = parser(chat)
                
                if not parsed_chat:
                    skipped += 1
                    continue

                # Sanitize the title
                title_sanitized = safe_filename(parsed_chat['title']).strip()
                
                if not title_sanitized:
                    skipped += 1
                    continue

                # Create markdown file
                markdown_filename = os.path.join(output_dir, f"{title_sanitized}.md")
                
                with open(markdown_filename, 'w', encoding='utf-8') as md_file:
                    md_file.write(f"# {parsed_chat['title']}\\n\\n")
                    md_file.write(f"**Chat ID:** {parsed_chat['id']}\\n\\n")
                    md_file.write("---\\n\\n")

                    for message in parsed_chat['messages']:
                        role = message['role'].title()
                        content = message['content']
                        md_file.write(f"**{role}:**\\n\\n{content}\\n\\n")

                processed += 1

            print(f"\\n--- Markdown Conversion Report ---")
            print(f"Total chats in '{json_file}': {total_chats}")
            print(f"Processed: {processed}")
            print(f"Skipped: {skipped}")
            print(f"Markdown files saved to: {output_dir}\\n")

        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{json_file}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to run the converter
    Usage: python ai_json_converter.py [json_file] [output_directory]
    """
    import sys
    
    # Default values
    json_file = "conversations.json"
    output_dir = None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Create converter and run
    converter = AIJSONConverter()
    converter.convert_to_markdown(json_file, output_dir)

if __name__ == "__main__":
    main()