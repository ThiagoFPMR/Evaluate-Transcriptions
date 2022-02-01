from Levenshtein import distance as lev

def iter_lev (og_iter, new_iter):
    """
    Calculates the lev distance between two iterables filled with strings.
    """
    return lev(' '.join(og_iter), ' '.join(new_iter))

def substitution_step (og, new, changelog, index):
    """
    This function performs the substitution step when the words selected be the indices do not
    match. It picks whether to peform deletion, insertion or replacement, then updates the indices
    and adds the operation to the changelog.

    Returns the updated index tuple.

    Parameters
    -------------
    og : iterable
        An iterable of substrings that represents the target string
        that servers for comparsion
    new : iterable
        An iterable of substrings that represents the string that is
        being compared
    changelog : iterable
        An iterable that allows for the storage of the changes necessary
        to turn 'new' into 'og'
    index : tuple
        A tuple indicating which element of each iterable is selected
    """
    # Creates a version of the string where the selected word is deleted
    deleted = new.copy()
    deleted.pop(index[1])
    # Creates a version of the string where a new word is inserted before the selected word
    inserted = new.copy()
    inserted.insert(index[1], og[index[0]])
    # Creates a version of the string where the selected word is replaced
    replaced = new.copy()
    replaced[index[1]] = og[index[0]]
    # Figures out which operation leads to the lowest levenshtein distance and picks that one as the operation to be done
    if iter_lev(og, deleted) <= iter_lev(og, inserted) and iter_lev(og, deleted) <= iter_lev(og, replaced):
        changelog.append((index[1], 'deleted', ''))
        return (index[0], index[1]+1)
    elif iter_lev(og, inserted) <= iter_lev(og, deleted) and iter_lev(og, inserted) <= iter_lev(og, replaced):
        changelog.append((index[1], 'inserted', og[index[0]]))
        return (index[0]+1, index[1])
    else:
        changelog.append((index[1], 'replaced', og[index[0]]))
        return (index[0]+1, index[1]+1)

def compare_transcriptions(og, new, changelog, index=(0,0)):
    """
    Compares two strings by using levenshtein distance to find out how to turn 'new'
    into 'og' with the fewest operations possible.

    Parameters
    -------------
    og : iterable
        An iterable of substrings that represents the target string
        that servers for comparsion
    new : iterable
        An iterable of substrings that represents the string that is
        being compared
    changelog : iterable
        An iterable that allows for the storage of the changes necessary
        to turn 'new' into 'og'
    index : tuple
        A tuple indicating which element of each iterable is selected; should not
        be manually defined
    """
    print(len(og), index[0], len(new), index[1])
    if index[0] >= len(og) and index[1] >= len(new):
        return
    elif index[0] >= len(og):
        for i, word in enumerate(new[index[1]:]):
            changelog.append((i, 'deleted', ''))
        return
    elif index[1] >= len(new):
        for i, word in enumerate(og[index[0]:]):
            changelog.append((i, 'inserted', word))    
        return    
    elif og[index[0]] == new[index[1]]:
        new_index = (index[0]+1, index[1]+1)
        return compare_transcriptions(og, new, changelog, new_index)
    else:
        new_index = substitution_step(og, new, changelog, index)
        return compare_transcriptions(og, new, changelog, new_index)
