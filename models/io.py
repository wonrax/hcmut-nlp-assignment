def get_questions(path):
    """
    This function reads the questions from the file and returns a list of
    questions.
    """
    questions = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line = line.replace("\n", "")
            questions.append(line)
    return questions

def write_to_file(string, path):
    """
    This function writes the string to the file.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(string)