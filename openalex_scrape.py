# Step 1: Import the required libraries
from pyalex import Works

# Step 2: Function to search papers and get abstracts
def get_abstracts_from_keywords(keywords):
    # Loop through each keyword
    for keyword in keywords:
        print(f"Searching for papers with keyword: {keyword}")
        
        # Initialize variables
        abstracts_collected = 0
        page = 1
        abstracts_to_collect = 5
        collected_papers = []

        # Loop until we collect 5 papers with abstracts
        while abstracts_collected < abstracts_to_collect:
            # Step 3: Search for papers using the keyword in title and abstract, with pagination
            #results = Works().search_filter(title_and_abstract=keyword).get(page=page, per_page=10)  # Fetch more papers per request
            results = Works().search_filter(title_and_abstract=keyword, type="journal-article").get(page=page, per_page=10)  # Fetch more papers per request
            
            # Step 4: Process the results
            for work in results:
                title = work['title']
                abstract_inverted_index = work.get('abstract_inverted_index', None)
                
                if abstract_inverted_index:
                    # Rebuild the abstract from the inverted index
                    abstract_words = sorted(abstract_inverted_index.items(), key=lambda x: x[1])
                    rebuilt_abstract = " ".join([word[0] for word in abstract_words])
                    # Collect the title and abstract
                    collected_papers.append({
                        'title': title,
                        'abstract': rebuilt_abstract
                    })
                    abstracts_collected += 1
                else:
                    # Skip papers without abstracts
                    continue
                
                if abstracts_collected >= abstracts_to_collect:
                    break

            # Move to the next page to fetch more papers if needed
            page += 1

        # Step 5: Print the collected papers with abstracts
        for paper in collected_papers:
            print(f"Title: {paper['title']}")
            print(f"Abstract: {paper['abstract']}")
            print('-' * 80)

# Step 6: Define the list of keywords
keywords = ['machine learning', 'artificial intelligence', 'computer vision']

# Step 7: Call the function with your keywords
get_abstracts_from_keywords(keywords)