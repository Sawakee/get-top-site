# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
CUSTOM_SEARCH_ENGINE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

# Google Custom Search API serviceをグローバルで1回だけ生成
service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

def getSearchResponse(keyword):
    try:
        response = service.cse().list(
            q=keyword,
            cx=CUSTOM_SEARCH_ENGINE_ID,
            lr='lang_ja',
            num=1,
            start=1
        ).execute()
        if 'items' in response:
            return response['items'][0]['link']
        else:
            return None
    except HttpError as e:
        if e.resp.status == 429:
            print("[ERROR] Quota exceeded. Stopping.")
            sys.exit(1)
        print(e)
        return None
    except Exception as e:
        print(e)
        return None



def print_usage_and_exit():
    print("Usage: python get_top_site.py <list_file> [-o output_file]")
    sys.exit(1)

def process_company(item, out_fp=None):
    url = getSearchResponse(item)
    line = f"{item}|{url if url else 'None'}"
    print(line)
    if out_fp:
        print(line, file=out_fp)

def main():
    if len(sys.argv) < 2:
        print_usage_and_exit()

    list_file = sys.argv[1]
    output_file = None
    if '-o' in sys.argv:
        o_idx = sys.argv.index('-o')
        if o_idx + 1 < len(sys.argv):
            output_file = sys.argv[o_idx + 1]
        else:
            print("'-o' specified but no output file given.")
            sys.exit(1)

    out_fp = open(output_file, 'w', encoding='utf-8') if output_file else None
    try:
        with open(list_file, "r", encoding="utf-8") as f:
            for item in f:
                process_company(item.strip(), out_fp)
    finally:
        if out_fp:
            out_fp.close()

if __name__ == '__main__':
    main()