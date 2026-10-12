import urllib.request

def download_and_extract():
    # We will run our local server on port 8000
    url = "http://localhost:8000/index.html"
    print(f"Requesting web page from {url}...\n")
    
    try:
        # 1. Download the web page using urllib (Python's built-in HTTP library)
        response = urllib.request.urlopen(url)
        
        # Read the raw bytes and decode them into readable text
        html_content = response.read().decode('utf-8')
        
        print("--- RAW HTML DOWNLOADED ---")
        print(html_content)
        print("---------------------------\n")
        
        # 2. Extract useful information (Find the text between <title> and </title>)
        # We do this using simple string manipulation
        title_start_tag = "<title>"
        title_end_tag = "</title>"
        
        start_index = html_content.find(title_start_tag) + len(title_start_tag)
        end_index = html_content.find(title_end_tag)
        
        page_title = html_content[start_index:end_index]
        
        print(f"*** EXTRACTED DATA ***")
        print(f"The Title of the webpage is: '{page_title}'")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Did you start the local HTTP server in the web_root folder?")

if __name__ == "__main__":
    download_and_extract()