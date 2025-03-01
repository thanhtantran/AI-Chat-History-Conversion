# Claude.ai Chat Log Converter

This script converts Claude.ai JSON chat logs into various formats, including Markdown, plain text, JSON Lines (JSONL), and PDF.

## Usage

1.  **Install Requirements:**

    ```bash
    pip install fpdf
    ```

2.  **Run the script:**

    ```bash
    python extract.py [JSON_FILE] [OPTIONS]
    ```

    * `JSON_FILE`: Path to the input JSON file (defaults to `conversations.json` in the current directory).
    * `OPTIONS`:
        * `-md`, `--markdown`: Convert to Markdown (default).
        * `-txt`, `--text`: Convert to plain text.
        * `-jsonl`, `--jsonlines`: Convert to JSON Lines (JSONL).
        * `-pdf`, `--pdf`: Convert to PDF.

**Examples:**

* Convert `conversations.json` to Markdown:

    ```bash
    python extract.py -md
    ```

    or

    ```bash
    python extract.py conversations.json -md
    ```

* Convert `my_chats.json` to plain text:

    ```bash
    python extract.py my_chats.json -txt
    ```

* Convert `conversations.json` to JSONL:

    ```bash
    python extract.py -jsonl
    ```

* Convert `conversations.json` to PDF:

    ```bash
    python extract.py -pdf
    ```

## Output

The script will create output files in the current directory with the following naming convention:

* `DDMMYY-CHAT_TITLE.md` (for Markdown)
* `DDMMYY-CHAT_TITLE.txt` (for plain text)
* `DDMMYY-CHAT_TITLE.jsonl` (for JSONL)
* `DDMMYY-CHAT_TITLE.pdf` (for PDF)

## Notes

* The script handles empty chat titles and skips chats with missing or invalid data.
* If no output format is specified, the script defaults to Markdown.
* The script requires the `fpdf` library for PDF generation.

## License

This script is licensed under the MIT License.