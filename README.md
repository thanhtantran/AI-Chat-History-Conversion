# Claude.ai Chat Log Converter

This script converts Claude.ai JSON chat logs into various formats: Markdown, plain text, JSON Lines (JSONL), and PDF.  
Output files are named using the sanitized chat title (non-ASCII characters, including emojis, are removed), and chats without a valid title are skipped.

## Requirements

Install the required package:
```bash
pip install fpdf
```

## Usage

Run the script with:
```bash
python extract.py [JSON_FILE] [OPTIONS]
```

- **JSON_FILE**: Path to the input JSON file (defaults to `conversations.json` in the current directory).
- **OPTIONS**:
  - `-md`, `--markdown`: Convert to Markdown (default).
  - `-txt`, `--text`: Convert to plain text.
  - `-jsonl`, `--jsonlines`: Convert to JSON Lines (JSONL).
  - `-pdf`, `--pdf`: Convert to PDF.

**Examples:**

- Convert `conversations.json` to Markdown:
    ```bash
    python extract.py -md
    ```
    or
    ```bash
    python extract.py conversations.json -md
    ```

- Convert `my_chats.json` to plain text:
    ```bash
    python extract.py my_chats.json -txt
    ```

- Convert `conversations.json` to JSONL:
    ```bash
    python extract.py -jsonl
    ```

- Convert `conversations.json` to PDF:
    ```bash
    python extract.py -pdf
    ```

## Output

The script creates output files in the current directory with filenames based solely on the sanitized chat title:

- `CHAT_TITLE.md` (Markdown)
- `CHAT_TITLE.txt` (plain text)
- `CHAT_TITLE.jsonl` (JSONL)
- `CHAT_TITLE.pdf` (PDF)

## Notes

- Chats with empty or invalid titles are skipped.
- Chat titles are sanitized by removing non-ASCII characters (including emojis) and replacing forbidden characters.
- If no output format is specified, the script defaults to Markdown.
- JSON files are not tracked in this repository and are excluded via the `.gitignore` file.
- The script requires the `fpdf` library for PDF generation.

## License

This script is licensed under the MIT License.

