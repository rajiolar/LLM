import os
from dotenv import load_dotenv
from together import Together
import random


# Load environment variables from the .env file
load_dotenv()


# Initialize the Together client with the API key
client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

"""
This module provides an interactive math quiz game for children aged 5-8, 
where questions are generated using the LLaMA model through the Together API. 
The quiz adapts in difficulty based on the user's performance, and it allows 
children to progress through levels depending on their score.

Functions:
- generate_math_question: Generates a math question based on the difficulty level using a GEN AI model.
- calculate_next_difficulty: Adjusts difficulty based on the user's score.
- math_quiz_game: The main function to run the quiz game, allowing users to input their age and interact with the quiz.
"""


def generate_math_question(difficulty_level):
    """
    Generates a math question using a GEN AI model (LLaMA) based on the difficulty level.

    Parameters:
    difficulty_level (int): The level of difficulty (1 for easy, 2 for medium, 3 for hard).

    Returns:
    str: The generated math question.
    """
    if difficulty_level == 1:
        prompt = "Generate a simple addition or subtraction math problem for a 6-year-old."
    elif difficulty_level == 2:
        prompt = "Generate a medium-difficulty math problem involving addition and subtraction for a 7-year-old."
    else:
        prompt = "Generate a complex math problem for an 8-year-old involving addition, subtraction, or simple multiplication."

    # Use Together API to generate a math problem
    response = client.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", 
        prompt=prompt,
        max_tokens=30, 
        temperature=0.4, 
        top_p=0.9, 
        stream=False
    )
    
    question = response.choices[0].text.strip()
    return question


def calculate_next_difficulty(score, total_questions):
    """
    Determines the next difficulty level based on the user's accuracy.

    Parameters:
    score (int): The number of correct answers provided by the user.
    total_questions (int): The total number of questions asked so far.

    Returns:
    int: The next difficulty level (1 for easy, 2 for medium, 3 for hard).
    """
    accuracy = score / total_questions
    if accuracy >= 0.8:
        return 3  # Hard difficulty if the child is doing well
    elif accuracy >= 0.5:
        return 2  # Medium difficulty
    else:
        return 1  # Easy difficulty


def math_quiz_game():
    """
    Runs the interactive math quiz game for children, generating math questions and adjusting 
    difficulty as the user progresses. The quiz adapts based on the user's score and age.

    The game:
    - Asks the user for their age to start with the appropriate difficulty.
    - Presents math questions from an AI model.
    - Tracks the user's score and adjusts difficulty accordingly.
    - Allows the user to move to the next difficulty level after each section.

    No parameters or returns; this function runs interactively.
    """
    total_sections = 3
    questions_per_section = 10
    total_questions = 0
    score = 0
    
    # Ask for user's age and set starting difficulty
    age = int(input("Enter your age: "))
    difficulty_level = 1 if age < 6 else 2 if age < 8 else 3
    
    for section in range(total_sections):
        print(f"\nSection {section + 1} (Difficulty Level: {difficulty_level}):")
        for question_num in range(questions_per_section):
            total_questions += 1
            # Generate a math question using LLaMA and display it
            question = generate_math_question(difficulty_level)
            print(f"Question {question_num + 1}: {question}")
            
            # Get user input for the answer (simulation; replace with actual evaluation logic as needed)
            try:
                user_answer = input("Your answer: ")
            except ValueError:
                print("Invalid input! Please enter a valid answer.")
                continue  # Ask the next question without penalizing

            # Simulate checking the answer for now (you could replace this with actual answer evaluation)
            correct = True if random.choice([True, False]) else False
            if correct:
                score += 1
                print("Correct!")
            else:
                print("Incorrect!")
        
        # Ask if the user wants to proceed to the next difficulty level
        if section < total_sections - 1:
            proceed = input("Do you want to move to the next level? (yes/no): ").strip().lower()
            if proceed != 'yes':
                break

        # Calculate the next difficulty level based on the current score
        difficulty_level = calculate_next_difficulty(score, total_questions)
        print(f"Your current score: {score}/{total_questions}")
    
    print(f"\nFinal Score: {score}/{total_questions}")


# Start the quiz game
if __name__ == "__main__":
    math_quiz_game()
