#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from transkribus_web import Transkribus_Web
from cleaner import Cleaner
import re
import sys

class Transkribus_CLI:
    """ A very simple command line interface (CLI) to operate the Transkribus_Web client 
        and a pipeline which normalizes a diplomatic transcription of Latin text. 
        Caveats: No handling of erroneus user input and no possibility to go one step back. """
    def __init__(self):
        # Initialize the Transkribus_Web object:
        self.client = Transkribus_Web()
        self.cleaner = Cleaner(replacement_table_path = "replacement_table.tsv")
            
    def login(self):
        YOUR_USER_NAME = input("Transkribus user name: ")
        YOUR_PASSWORD = input("Password: ")
        success = self.client.login(YOUR_USER_NAME, YOUR_PASSWORD)
        if success == False:
            print("Wrong username or password. Try again!")
            self.login()

    def choose_collection(self):
        """ Get a list of the user's collections on the Transkribus server
            and let the user choose a collection. """
        my_collections = self.client.get_collections()

        if my_collections:
            for idx, col in enumerate(my_collections):
                print(f"{idx+1} - {col['colName']} ({col['colId']}): {col['nrOfDocuments']} documents")

            this_collection = int(input(f"Choose a collection (1-{len(my_collections)+1}): "))
            colId = my_collections[this_collection - 1]['colId']
            print(f"Opening {colId}...")
            return colId
        else:
            sys.exit("No collections found.")    

    def choose_document(self, colId):
        """ Get a list of documents in a collections on the Transkribus server
            and let the user choose a document. """
        my_documents = self.client.get_documents_in_collection(colId)

        if my_documents:
            for idx, doc in enumerate(my_documents):
                print(f"{idx+1} - {doc['title']} ({doc['docId']}): {doc['nrOfPages']} pages")

            this_document = int(input(f"Choose a document (1-{len(my_documents)+1}): "))
            docId = my_documents[this_document - 1]['docId']
            print(f"Opening {colId}/{docId}...")
            return docId
        else:
            sys.exit("No documents found.")            

    def choose_page(self, colId, docId):
        """ Get a list of pages in a document on the Transkribus server
            and let the user choose a page. Note that only pages with
            status FINAL or GT (Ground Truth) are listed (FINAL in 
            parenthesis). """
        my_pages = self.client.get_pages_in_document(colId, docId)

        if my_pages:
            page_list = []
            for page in my_pages:
                # Select only those pages with status FINAL or GT (Ground Truth):
                status = page['tsList']['transcripts'][0]['status']
                if status == "FINAL":
                    page_list.append(f"({page['pageNr']})")
                elif status == "GT":
                    page_list.append(f"{page['pageNr']}")

            print(" ".join(page_list)) # Print the list of pages in this document.
            print("(Status of page numbers in parenthesis is FINAL, otherwise it's GROUND TRUTH.)")
            pageNr = input(f"Choose a page from the list above: ")
            print(f"Opening {colId}/{docId}/{pageNr}...")
            return pageNr
        else:
            sys.exit("No pages with status FINAL or GT found.")

    def check_for_errors(self, page_xml):
        """ Helper function. Make sure that the page_xml contains
            – TextRegions
            – Baselines
            – TextEquiv, i.e. actual text in the lines. 
            This is useful for further processing of the data to prevent crashes.
            
            page_xml -- a lxml.objectify object of a page in Transkribus 
            
            Returns False if everything is OK, otherwise an error message. """
            
        ns = "{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}"
        
        if page_xml.find(f".//{ns}TextRegion") is None:
            return "PAGE-XML: ERROR: No TextRegions found."
        if page_xml.find(f".//{ns}Baseline") is None:
            return "PAGE-XML: ERROR: No BaseLines found."
        if page_xml.find(f".//{ns}TextEquiv") is None:
            return "PAGE-XML: ERROR: Lines contain no text."

        return False

    def get_custom_attributes(self, string):
        """ Helper function. Returns the custom attributes of a TextRegion as a dict. """
        custom_attributes = re.compile(r'\{(\w*?):(\w*?);\}')
        return dict(custom_attributes.findall(string))

    def get_page(self, colId, docId, pageNr):
        """ Download the page_xml data from Transkribus and process
            the text of a page. Returns an error if the page 
            does not contain TextRegions, BaseLines or actual text in 
            the lines. Otherwise, it returns a page object (i.e. a dict). """
        # Store the namespace string used by the Transkribus page_xml format:
        ns = "{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}"
        
        my_page = self.client.get_page_xml(colId, docId, pageNr)
        
        check_for_errors = self.check_for_errors(my_page)
        if check_for_errors:
            sys.exit(f"ERROR processing {colId}/{docId}, page {pageNr}: {check_for_errors}")
        else:
            # Extract the lines of my_page and build a page object:
            page = {"lines": []}
            for line in my_page.Page.iter(f"{ns}TextLine"): # Cf. the section "tree iteration" in https://lxml.de/tutorial.html
                # Get the attributes of the TextRegion:
                custom_attributes_region = self.get_custom_attributes(line.getparent().attrib['custom'])
                regionNr = custom_attributes_region['index']
                # In the following line you could filter TextRegions tagged with a specific tag (like "paragraph"):
                if custom_attributes_region.get("type") == "paragraph": # Filter all TextRegions tagged as "paragraph".
                    lineNr = self.get_custom_attributes(line.attrib['custom'])['index']
                    # Build a line object
                    raw_data = line.TextEquiv.Unicode
                    cleaned = self.cleaner.replace_abbreviations(raw_data)
                    words = self.cleaner.tokenize(cleaned)
                    words = self.cleaner.resolve_macrons(words)
                    new_line = {'identifier': f"r{regionNr}l{lineNr}",
                                'raw_data': raw_data,
                                'cleaned_data': cleaned,
                                'words': words}
                    page["lines"].append(new_line)

            # Resolve linebreaks on this page:
            page = self.cleaner.resolve_linebreaks(page)

            return page

    def print_page(self, page, raw_text=False):
        """ Prints a page object to the command line. """

        for line in page['lines']:
            print(f"{line['identifier'].rjust(8)} {self.cleaner.auto_spacer(line)}")
            
            if raw_text:
                print(f"{''.rjust(8)} {line['raw_data']}")
                
    def logout(self):
        self.client.logout()
