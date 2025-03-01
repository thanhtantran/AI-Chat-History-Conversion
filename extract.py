import os
import json
import re

def safe_filename(title):
    """
    Return a sanitized version of 'title' for filenames.
    Removes non-ASCII characters (including emojis),
    then replaces typical forbidden characters with '_'.
    """
    # Remove all non-ASCII (including emojis)
    title = re.sub(r'[^\x00-\x7F]+', '', title)
    # Replace typical forbidden characters on Windows/*nix
    return re.sub(r'[\\/*?:"<>|]', '_', title)

def json_to_markdown(json_file, output_dir):
    """
    Converts a Claude.ai JSON chat log file into readable markdown files.
    Skips empty or nameless chats. Sanitizes filenames to remove emojis.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"Error: JSON file '{json_file}' does not contain a list of chats.")
            return

        total_chats = len(data)
        processed = 0
        skipped = 0

        for chat in data:
            # Basic validation
            if not isinstance(chat, dict) or 'uuid' not in chat or 'chat_messages' not in chat:
                skipped += 1
                continue

            chat_id = chat['uuid']
            title = chat.get('name', '') or ''
            messages = chat['chat_messages']

            # Skip if there is no title or no messages
            if not title or not messages:
                skipped += 1
                continue

            # Sanitize the title (removes emojis, etc.)
            title_sanitized = safe_filename(title).strip()

            # If title becomes empty after sanitizing, skip
            if not title_sanitized:
                skipped += 1
                continue

            # Construct final filename without date/hyphen
            markdown_filename = os.path.join(output_dir, f"{title_sanitized}.md")

            with open(markdown_filename, 'w', encoding='utf-8') as md_file:
                md_file.write(f"# Chat ID: {chat_id}\n\n")

                for message in messages:
                    if not isinstance(message, dict) or 'sender' not in message or 'content' not in message:
                        continue

                    sender = message['sender']
                    contents = message['content']

                    for content in contents:
                        if not isinstance(content, dict) or 'text' not in content:
                            continue
                        text = content['text']
                        md_file.write(f"**{sender}:**\n\n{text}\n\n")

            processed += 1

        print(f"\n--- Markdown Conversion Report ---")
        print(f"Total chats in '{json_file}': {total_chats}")
        print(f"Processed: {processed}")
        print(f"Skipped: {skipped}")
        print(f"Markdown files saved to: {output_dir}\n")

    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # The main logic: just call our function on your known file
    json_file = "conversations.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, json_file)

    json_to_markdown(json_file_path, script_dir)
