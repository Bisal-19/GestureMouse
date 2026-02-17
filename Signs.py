def get_meaning(fingers):
    """
    Takes the list of fingers [1,1,0,0,0] and returns a word.
    """
    if fingers == [0, 0, 0, 0, 0]:
        return "STOP / NO"
    if fingers == [1, 1, 1, 1, 1]:
        return "HELLO (Open Palm)"
    if fingers == [0, 1, 1, 0, 0]:
        return "VICTORY"
    if fingers == [1, 0, 0, 0, 0]:
        return "LIKE"
    if fingers == [0, 1, 0, 0, 0]:
        return "LOOK THERE"
    if fingers == [1, 1, 0, 0, 1]:
        return "I LOVE YOU"

    return ""  # Unknown sign
