# AI JSON to Markdown Converter - Usage Examples

## Basic Usage

```python
from ai_json_converter import AIJSONConverter

# Create converter instance
converter = AIJSONConverter()

# Convert JSON file to markdown
converter.convert_to_markdown('conversations.json', 'output_folder')
```

## Command Line Usage

```bash
# Basic usage (uses default output directory)
python ai_json_converter.py conversations.json

# Specify output directory
python ai_json_converter.py conversations.json markdown_output

# Use default filename (conversations.json)
python ai_json_converter.py
```

## Supported Formats

1. **Claude.ai Format**
   - Structure: `uuid`, `chat_messages`
   - Example: Claude AI export files

2. **ChatGPT Format**
   - Structure: `title`, `mapping`
   - Example: OpenAI ChatGPT export files

3. **Generic Nested Format**
   - Structure: `chat.history.messages`
   - Example: Your provided format

4. **Simple Messages Format**
   - Structure: Direct `messages` array
   - Example: Basic chat exports

5. **Gemini Format** (hypothetical)
   - Structure: `conversation_id`, `turns`
   - Example: Google Gemini exports

## Features

- ✅ Automatic format detection
- ✅ Safe filename generation (removes emojis, special characters)
- ✅ Proper timestamp sorting
- ✅ Error handling and reporting
- ✅ Multiple content format support
- ✅ Command line interface