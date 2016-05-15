# Team Lab - SoSe 2016 - Project: Information Retrieval System

## Contributors

-  Prajit Dhar

-  Janis Pagel

## Output for first upload

The output for our index and a sample query is stored in output.txt

## Goal

Create a fully functional Information Retrieval System, including Indexing, Query Support, Ranking, Evaluation and Crawling

## Usage

Start the system by typing

```sh
python airs-0.3.0.py
```

You are asked to enter your query. The output is a list of all documents, the query words occur in.

By now only boolean query is implemented, i.e. only documents in which all entered words occur are considered.

For testing purposes, only 10 randomly chosen documents are taken into account.

## Data

The used data base is a collection of 10,000 Amazon reviews, stored in /testfile_amazon_rewievs

## Classes

### airs-0.3.0.py

Main class, running the system and combine the different modules of the code.

### modules/parsedoc.py

Reading in the source files and providing the content as a string.

### modules/tokenizer.py

A simple tokenizer that gets a document as input and tokenizes it.

### modules/document.py

Class to represent a document, storing tokens, document length etc.

### modules/token.py

Class for representing a token, containing string, string length etc.

### modules/term.py

Class for representing a term, including pointers to the postings lists, normalizing of terms and storing the terms
on disk in an efficient way using folder structures.

### modules/postingslist.py

Class for storing the postings lists for each term.

### modules/query.py

Class for performing user queries and performing query processing and parsing

### Not listed Classes

Classes which are not listed here, are not used by now resp. will be used in future applications.
