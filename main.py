import os
import subprocess
from notion_client import Client
import bibtexparser
from datetime import datetime
import argparse

# 環境変数からデフォルト値を取得
DEFAULT_NOTION_TOKEN = os.environ.get("DEDAULT_NOTION_TOKEN")
DEFAULT_DATABASE_ID = os.environ.get("DEDAULT_DATABASE_ID")

def pdf_to_bibtex(pdf_path):
    print("Getting bibtex information...")
    try:
        result = subprocess.run(['pdf2bib', pdf_path], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running pdf2bib: {e}")
        return None

def parse_bibtex(bibtex_str):
    bib_database = bibtexparser.loads(bibtex_str)
    entry = bib_database.entries[0] if bib_database.entries else {}
    
    return {
        "title": entry.get("title", ""),
        "year": entry.get("year", ""),
        "doi": entry.get("doi", ""),
        "bibtex": bibtex_str
    }

def check_duplicate(notion_client, database_id, title, doi):
    query = notion_client.databases.query(
        database_id=database_id,
        filter={
            "or": [
                {"property": "タイトル", "title": {"equals": title}},
                {"property": "doi", "url": {"equals": f"https://doi.org/{doi}"}}
            ]
        }
    )
    return len(query["results"]) > 0

def add_to_notion(info, notion_client, database_id):
    print("checking duplicate...")
    if check_duplicate(notion_client, database_id, info["title"], info["doi"]):
        print(f"Duplicate entry found for '{info['title']}'. Skipping...")
        return False

    properties = {
        "タイトル": {"title": [{"text": {"content": info["title"]}}]},
        "Year": {"number": int(info["year"]) if info["year"].isdigit() else None},
        "doi": {"url": f"https://doi.org/{info['doi']}" if info['doi'] else None},
        "BibTex": {"rich_text": [{"text": {"content": info["bibtex"][:2000]}}]},
        "READ": {"checkbox": False},
        "日付": {"date": {"start": datetime.now().isoformat()}}
    }
    
    print("Properties being sent to Notion:")
    print(properties)
    
    notion_client.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )
    return True

def main(pdf_path, notion_token, database_id):
    bibtex_str = pdf_to_bibtex(pdf_path)
    if bibtex_str:
        info = parse_bibtex(bibtex_str)
        notion_client = Client(auth=notion_token)
        if add_to_notion(info, notion_client, database_id):
            print(f"Successfully added {info['title']} to Notion database.")
        else:
            print(f"Skipped adding {info['title']} as it already exists in the database.")
    else:
        print("Failed to generate BibTeX from PDF.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to BibTeX and add to Notion database")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--token", default=DEFAULT_NOTION_TOKEN, help="Notion API token")
    parser.add_argument("--db", default=DEFAULT_DATABASE_ID, help="Notion database ID")
    
    args = parser.parse_args()
    
    main(args.pdf_path, args.token, args.db)