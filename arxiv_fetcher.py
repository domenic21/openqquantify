import requests
import xml.etree.ElementTree as ET
import sqlite3


categories = ["quant-ph", "cs.ET", "cs.CR"] # List of categories to fetch from arXiv, you can add more categories as needed.
# "quant-ph" for quantum physics, "cs.ET" for computer science - Emerging Technologies, "cs.CR" for computer science - Cryptography and Security


def fetch_arxiv_data(category=categories, max_results=10): # Default to quantum physics category
    query = "+OR+".join([f"cat:{c}" for c in category]) # Create a query string for the arXiv API using the categories
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&max_results={max_results}"
    response = requests.get(url)
    response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)
    root = ET.fromstring(response.content) # Parse the XML response from the arXiv API using ElementTree, ET is a module in Python's standard library for parsing XML and HTML documents.
    # ElementTree provides a simple and efficient way to navigate and manipulate XML data.
    entries = [] # Initialize an empty list to store the entries


    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'): # Find all entries in the Atom feed 
        title_elem = entry.find('{http://www.w3.org/2005/Atom}title') # Find the title element
        summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary') # Find the summary element
        title = title_elem.text.strip() if title_elem is not None and title_elem.text is not None else "" # Strip whitespace from the title
        summary = summary_elem.text.strip() if summary_elem is not None and summary_elem.text is not None else "" # Strip whitespace from the summary
        entries.append({'title': title, 'summary': summary}) # Append the title and summary to the entries list

    return entries #return the list of entries

def cache_arxiv_data(entries): # Cache the fetched arXiv data in a SQLite database
    conn = sqlite3.connect('cache.db')
    c = conn.cursor() # Create a cursor object to execute SQL commands , a cursor is used to interact with the database as it allows you to execute SQL commands and fetch results.
    c.execute('CREATE TABLE IF NOT EXISTS cache (prompt TEXT PRIMARY KEY, response TEXT)')

    for entry in entries:
        prompt = entry['title'] # Use the title as the prompt
        response = entry['summary'] # Use the summary as the response
        c.execute('INSERT OR IGNORE INTO cache (prompt, response) VALUES (?, ?)', (prompt, response)) # Insert the prompt and response into the cache table, ignoring duplicates

    conn.commit()
    conn.close()
