#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cli import Transkribus_CLI

def main():
    cli = Transkribus_CLI()
    cli.login()
    colId = cli.choose_collection()
    docId = cli.choose_document(colId)
    pageNr = cli.choose_page(colId, docId)
    page = cli.get_page(colId, docId, pageNr)
    cli.print_page(page, raw_text=False)
    cli.logout()

if __name__ == "__main__":
    main()