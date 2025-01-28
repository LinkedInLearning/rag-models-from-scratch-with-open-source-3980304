import os
import re
# import sys
# !{sys.executable} -m pip install wikipedia
import wikipedia


search_results = wikipedia.search("Human Rights", 1000)
articles = []

for article in search_results:
    try:
        wiki_result = wikipedia.WikipediaPage(result)
        articles.append( (wiki_result.title, wiki_result.content) )
    except:
        print("Error with article: {}".format(article))


# Directory to store the articles
output_dir = "all_articles"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize filenames
def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\/:*?"<>| ]', '_', filename)

# Save each article as a text file
for title, content in articles:
    try:
        # Sanitize the title for the filename
        sanitized_title = sanitize_filename(title)
        file_path = os.path.join(output_dir, f"{sanitized_title}.txt")
        
        # Write the content to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Article '{title}' saved as '{sanitized_title}'.")
    except Exception as e:
        print(f"Error saving article '{title}': {e}")

print(f"Articles have been saved in the '{output_dir}' directory.")
