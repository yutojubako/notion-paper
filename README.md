# PDF to Notion Importer

PDF to Notion Importer is a tool that extracts bibliographic information from PDF papers and adds it to a Notion database. It supports both local PDF files and URL inputs, with features like duplicate checking and BibTeX formatting.

## Features

- Extract bibliographic information from PDF files
- Support for local PDF files and URL inputs
- Add extracted information to a Notion database
- Duplicate entry checking
- BibTeX formatting and cleaning
- Force option to override duplicate entries

## Installation

1. Ensure you have Python 3.8+ installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yutojubako/notion-paper
   cd notion-paper
   ```
3. Install the required dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

1. Set up a Notion integration and get your API token. [Learn how](https://developers.notion.com/docs/getting-started)
2. Create a Notion database for storing paper information.
3. Set the following environment variables:
   ```
   export DEFAULT_NOTION_TOKEN="your_notion_api_token"
   export DEFAULT_DATABASE_ID="your_notion_database_id"
   ```

## Usage

### Local PDF File

To add a local PDF file to your Notion database:

```
poetry run python main.py path/to/your/paper.pdf
```

### URL Input

To add a paper from a URL:

```
poetry run python main.py -u https://example.com/paper.pdf
```

### Force Option

To force add an entry even if a duplicate is found:

```
poetry run python main.py path/to/your/paper.pdf -f
```

or

```
poetry run python main.py -u https://example.com/paper.pdf --force
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
