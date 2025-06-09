import sys
import gc
from database_connect_embeddings import get_psql_session, TextEmbedding
from pull_db_content import search_embeddings, get_surrounding_sentences
from sentence_transformers import SentenceTransformer

# Identify how many search results till we have 5 matches that generate non-overlapping windows.

# Check if a matches context window overlaps with another matches context window.
def is_unique_to_window(existing_matches, current_match, group_window_size=5):
    
    for match in existing_matches:
        if match[3] != current_match[3]:
            continue
        if match[1] > current_match[1] + group_window_size or match[1] < current_match[1] - group_window_size:
            continue
        else:
            return False
    
    return True

# Getting unique matches from search results
def get_filtered_matches(search_results):
    unique_count = 0
    matches = []
    for result in search_results:

        if unique_count >= 5:
            break;
        if is_unique_to_window(matches, result):
            unique_count += 1
            
        matches.append(result)

    return matches

def group_entries(entry_ids, file_names, index_of_interest, group_window_size):

    # Identify if an entry with index index_of_interest needs grouping with other entries.

    # If it needs no grouping, return an array with just its index (will be handled as in get_surrounding_sentences) 
    # If it needs grouping with one or more entries, return array of indices of those entries.

    entry_id_of_interest = entry_ids[index_of_interest]
    file_name_of_interest = file_names[index_of_interest]

    group_idxs = [index_of_interest]

    for idx, (entry_id, file_name) in enumerate(zip(entry_ids, file_names)):
        if file_name != file_name_of_interest:
            continue;
        if (entry_id >= entry_id_of_interest - group_window_size) and (entry_id <= entry_id_of_interest + group_window_size):
            group_idxs.append(idx)

    return group_idxs

def consolidate_groupings(grouped_entries):
    # Given a list of lists with grouped entries, combine all lists that have one or more elements in common, then remove duplicates.
    # This should result in a number of lists equal to the number of matched contexts we want

    # Assumes we have run the function group_entries on each entry

    original_groups = grouped_entries[:]
    combined_groups = []

    while( len(original_groups) ):
        current_grouping = original_groups[0][:]
        original_groups.remove(original_groups[0])
        for other_entry in original_groups:
            for idx in current_grouping:
                if idx in other_entry:
                    current_grouping += other_entry
                    original_groups.remove(other_entry)
                    break;
        
        current_grouping = list(set(current_grouping))
        combined_groups.append(current_grouping)

    return combined_groups

def get_min_max_ids(entry_ids, file_names, combined_groups, group_window_size):

    min_ids = []
    max_ids = []

    for group in combined_groups:
        min_id = min([entry_ids[i] for i in group])
        max_id = max([entry_ids[i] for i in group])

        min_id = min_id - group_window_size
        max_id = max_id + group_window_size

        min_ids.append(min_id)
        max_ids.append(max_id)

    return min_ids, max_ids

def get_surrounding_sentences(entry_ids, file_names, group_window_size, session):

    grouped_entries = []
    for idx, id in enumerate(entry_ids):
        grouped_entries.append(group_entries(entry_ids, file_names, index_of_interest = idx, group_window_size = group_window_size))

    combined_groups = consolidate_groupings(grouped_entries)
    min_ids, max_ids = get_min_max_ids(entry_ids, file_names, combined_groups, group_window_size)
    surrounding_sentences = []

    for min_id, max_id in zip(min_ids, max_ids):
        surrounding_sentences.append(
            session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name)\
            .filter(TextEmbedding.id >= min_id)\
            .filter(TextEmbedding.id <= max_id)\
            .all()
        )
    
    return surrounding_sentences

def search_by_query(query, num_matches=5, group_window_size=5):

    session = get_psql_session()
    model = SentenceTransformer('SFR-Embedding-Mistral', device='cpu')
    query_embedding = model.encode(query)
    del model
    gc.collect()

    search_results = search_embeddings(query_embedding, session=session, limit=num_matches * (2*group_window_size + 1) )
    filtered_matches = get_filtered_matches(search_results)

    entry_ids = [i[0] for i in filtered_matches]
    file_names = [i[3] for i in filtered_matches]

    return get_surrounding_sentences(entry_ids=entry_ids, file_names=file_names, group_window_size=group_window_size, session=session)


if __name__=="__main__":

    query = "Tell me about children's rights in Germany."
    
    if len(sys.argv) > 1:
        query = sys.argv[1]

    context = search_by_query(query)

    for i in context:
        print(i, "\n")
