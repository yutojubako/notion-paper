import os
import subprocess
import requests
from notion_client import Client
import bibtexparser
from datetime import datetime
import argparse
import tempfile

# 環境変数からデフォルト値を取得
DEFAULT_NOTION_TOKEN = os.environ.get("DEDAULT_NOTION_TOKEN")
DEFAULT_DATABASE_ID = os.environ.get("DEDAULT_DATABASE_ID")

def download_pdf_from_url(url):
    print(f"Downloading PDF from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return None

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
    
    title = entry.get("title", "")
    title = title.replace("{", "").replace("}", "").strip()
    
    return {
        "title": title,
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

def user_confirmation(message):
    while True:
        response = input(f"{message} (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please answer with 'yes' or 'no'.")

def add_to_notion(info, notion_client, database_id, force=False, is_url=False):
    print("Checking for duplicates...")
    is_duplicate = check_duplicate(notion_client, database_id, info["title"], info["doi"])
    
    if is_duplicate and not force:
        print(f"Duplicate entry found for '{info['title']}'. Skipping...")
        return False
    elif is_duplicate and force:
        print(f"Duplicate entry found for '{info['title']}'. Force adding...")
    else:
        print(f"Adding new entry: '{info['title']}'")

    if not info["title"] and is_url:
        print("\nWARNING: Null or empty title detected for URL input.")
        print("This may indicate an issue with PDF parsing or Bibtex generation.")
        print("The entry will be added with the title 'Untitled' if you choose to proceed.")
        print("You may want to check the PDF and update the title manually later.\n")
        
        if not user_confirmation("Do you want to proceed with adding this entry?"):
            print("Entry addition cancelled by user.")
            return False

    properties = {
        "タイトル": {"title": [{"text": {"content": info["title"] or "Untitled"}}]},
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

def main(pdf_path, notion_token, database_id, url=None, force=False):
    is_url = bool(url)
    if url:
        pdf_path = download_pdf_from_url(url)
        if not pdf_path:
            print("Failed to download PDF from URL.")
            return

    bibtex_str = pdf_to_bibtex(pdf_path)
    if bibtex_str:
        info = parse_bibtex(bibtex_str)
        notion_client = Client(auth=notion_token)
        if add_to_notion(info, notion_client, database_id, force, is_url):
            print(f"Successfully added {info['title'] or 'Untitled'} to Notion database.")
        else:
            print(f"Skipped adding {info['title'] or 'Untitled'}.")
    else:
        print("Failed to generate BibTeX from PDF.")

    if url:
        os.unlink(pdf_path)  # 一時ファイルを削除

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to BibTeX and add to Notion database")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("pdf_path", nargs='?', help="Path to the PDF file")
    group.add_argument("-u", "--url", help="URL of the PDF file")
    parser.add_argument("--token", default=DEFAULT_NOTION_TOKEN, help="Notion API token")
    parser.add_argument("--db", default=DEFAULT_DATABASE_ID, help="Notion database ID")
    parser.add_argument("-f", "--force", action="store_true", help="Force add entry even if duplicate exists")
    
    args = parser.parse_args()
    
    main(args.pdf_path, args.token, args.db, args.url, args.force)