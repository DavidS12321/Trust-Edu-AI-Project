import openai

def generate_question(difficulty):

    print("Generating question with difficulty:", difficulty)
    
    # the prompt we are sending to chatGPT
    prompt = f"""
    Generate a 2nd-grade math question with difficulty: {difficulty}.
    The question should involve simple arithmetic, with the difficulty increasing as follows:
    Make sure the list just shows the answers.
    
    - "easy": simple Addition or simple subtraction (e.g., 10 + 5) (e.g., 19 - 6)
    - "medium": simple multiplication (e.g, 7 * 3)
    - "hard": Harder multiplication problems (e.g., 10 * 10) 

    Provide 4 distinct answer choices, and make sure that the correct answer is one of the options.
    Please follow the exact format below:

    Question:
    [Insert math expression here]

    Answer Choices:
    [number]
    [number]
    [number]
    [number]

    Correct Answer:
    [number]

    Ensure that the answers are all numbers, and there are no additional labels like "Options:" or "Answers:".
    """

    # request the given chatgpt model a chat and get the response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.7
        )
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None, None, None

    question_data = response['choices'][0]['message']['content'].strip()

    print("Raw question data:", question_data)

    question_data = question_data.replace('*', 'x')

    # parsing chatGPT's response:
    try:
        # split repsonse to filter empty lines
        lines = [line.strip() for line in question_data.split("\n") if line.strip()]

        print("Raw parsed lines:", lines)

        # extract filler words to accurately have the correct list of options 

        question_line_index = lines.index("Question:") + 1 
        if question_line_index < len(lines):
            question = lines[question_line_index].strip()
        else:
            raise ValueError("Missing question content after 'Question:'")

        print("Extracted Question:", question)

        choices_start = lines.index("Answer Choices:") + 1
        choices_end = lines.index("Correct Answer:")
        options = [line.strip() for line in lines[choices_start:choices_end] if line.strip()]

        print("Extracted Options:", options)

        if len(options) != 4:
            raise ValueError("There are not exactly four answer choices.")

        correct_answer_line_index = lines.index("Correct Answer:") + 1
        if correct_answer_line_index < len(lines):
            correct_answer = lines[correct_answer_line_index].strip()
        else:
            raise ValueError("The correct answer is missing after 'Correct Answer:'")

        print("Extracted Correct Answer:", correct_answer)

        return question, correct_answer, options
    except Exception as e:
        print(f"Error parsing the response: {e}")
        return None, None, None

# method to increase or decrease difficulty of question based on current performance
def adjust_difficulty(current_difficulty, correct_count, total_count):

    accuracy = 0
    
    if total_count > 1:
        accuracy = correct_count / total_count
        print(accuracy)

    if accuracy > 0.8:
        return "hard"
    elif accuracy > 0.5:
        return "medium"
    else:
        return "easy"