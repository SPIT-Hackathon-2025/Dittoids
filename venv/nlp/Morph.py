from nltk.stem import PorterStemmer

def track_changes(original, modified):
    """Compare original and modified words to track added and deleted letters."""
    deleted = []
    added = []
    
    # Convert to list for easier character-by-character comparison
    original_list = list(original)
    modified_list = list(modified)

    # Pointer for both words
    i, j = 0, 0
    
    while i < len(original_list) and j < len(modified_list):
        if original_list[i] != modified_list[j]:  # If chars don't match
            deleted.append(original_list[i])
            i += 1  # Move pointer in original
        else:
            i += 1
            j += 1  # Move both pointers when chars match
    
    # Remaining characters in the original word are deleted
    deleted.extend(original_list[i:])
    
    # Remaining characters in the modified word are added
    added.extend(modified_list[j:])
    
    return "".join(deleted), "".join(added)

def generate_add_delete_table(word):
    ps = PorterStemmer()
    original = word
    transformed = word
    steps = []

    while True:
        new_form = ps.stem(transformed)
        if new_form == transformed:
            break  # Stop if no more changes occur
        
        deleted_chars, added_chars = track_changes(transformed, new_form)
        
        steps.append((transformed, deleted_chars, added_chars))
        transformed = new_form  # Move to the next step

    # Printing the Add-Delete Table
    print(f"\nRoot word: {original}")
    print("| Step | Word       | Deleted | Added |")
    print("|------|-----------|---------|-------|")
    for i, (word, deleted, added) in enumerate(steps):
        print(f"| {i+1:<4} | {word:<10} | {deleted:<7} | {added:<5} |")
    print(f"Final Stemmed Word: {transformed}")

# Example Usage
word = input("Enter a word: ")
generate_add_delete_table(word)
