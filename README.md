# Team Lab - SoSe 2016 - Project: Information Retrieval System

## Contributors

-  Prajit Dhar

-  Janis Pagel

## Goal

Create a fully functional Information Retrieval System, including Indexing, Query Support, Ranking, Evaluation and Crawling

## Usage

Start the system by typing

```sh
python airs-0.2.1.py
```

## Classes

### airs-0.2.1.py

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
