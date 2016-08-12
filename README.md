# Team Lab - SoSe 2016 - Project: Information Retrieval System

## Contributors

-  Prajit Dhar

-  Janis Pagel

## Goal

Create a fully functional Information Retrieval System, including Indexing, Interactive Query Mode, Ranking and Evaluation.

## Usage

Start the system by typing

```sh
python airs-1.0.0.py [OPTIONS]
```

If you don't specify any options, the systems runs in an empty run without indexing any documents.
Please specify the number of documents you want to index and evaluate on using *-rand* or *-rank*.

## Options

You may specify several flags to individualize your indexing and evaluation:

```sh
python airs-1.0.0.py [-c PATH] [-rand N] [-rank N] [-s] [-p] [-e SYSTEM] [-i] [--version] [-h]
```

### -c / --corpus

Specify a path for corpus files. Default is ./amazon_reviews

### -rand / --random

Specify a number of randomized documents used for the inverted index.

### -rank / --ranking

Specify the number of documents which should be ranked.

The selection will start at the document with index 0; the specified number is the excluded upper bound. For example for the first 2000 documents to index and rank, give *-rank 2000*.

### -s / --store

Activate this flag if you want to store the inverted index into a pickle file.

### -p / --pickle

Activate this flag if you wish to read the inverted index from a stored pickle file.
This only works if there is an existing inverted index pickle file.

### -e / --eval

Specify which system you would like to evaluate. Type *-e bool* to evaluate the
boolean system, *-e tfidf* to evaluate the TF-IDF system and *-e prox* to evaluate
the proximity system. The default is *-e tfidf*.

### -i / --interactive

Activate this flag if you want to start an interactive session. This works together
with all flags.

You can use the *-e* flag to specify how the result for the query
should be ranked. Hence in this case the *-e* flag will not give an evaluation but
the system used for ranking for the interactive session. The default of *-e* is *tfidf*.
*-e bool* will return all found documents, *-e tfidf* and *-e prox* will return the 10
highest ranked documents.

You are asked to enter a query and will get the result displayed in the terminal.

### --version

Shows the version number.

### -h / --help

Shows information about the different flags and their usage.

## Data

The used data base is a collection of 10,000 Amazon reviews, stored in /amazon_reviews

## Classes

### airs-1.0.0.py

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

### modules/ranking.py

Class for ranking based on cosine similarity or proximity. The class provides
a sorted list of output documents for a query, based on the cosine ranking or
the proximity ranking.

### modules/evaluation.py

Class which entails functions for the evaluation process.

### modules/porter.py

A free porter stemmer, used from https://bitbucket.org/mchaput/stemming/src/5c242aa592a6d4f0e9a0b2e1afdca4fd757b8e8a/stemming/porter.py?at=default&fileviewer=file-view-default

### Not listed modules/classes

Classes which are not listed here are not used for now or will be used in future applications.

## Gold Annotations

The gold data is stored in the file golddata.txt.

## Output for first submission (09. May 2016)

The output for our index and a sample query is stored in output.txt
