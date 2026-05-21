import csv
import random

def generate():
    # Load existing cases to avoid duplicates
    all_inputs = []
    try:
        with open('verification_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_inputs.append(row['input_text'])
    except FileNotFoundError:
        pass

    new_test_inputs = [
        "HELLO WORLD", "Hello World", "hELLO wORLD", "I am HAPPY.", "This is a TEST.",
        "123", "12.34", "Section 5.2", "Call 911!", "Price: $10.00",
        "Date: 05/14/2026", "(Parentheses)", "[Brackets]", "{Braces}",
        "Slash/Backslash\\", "Hyphen-ated", "Dash--double",
        "Quote 'single' and \"double\"",
        "heart", "beach", "teacher", "bed", "educated", "reduced",
        "about", "above", "according", "across", "after", "afternoon", "afterward",
        "again", "against", "also", "almost", "already", "altogether", "although", "always",
        "because", "before", "behind", "below", "beneath", "beside", "between", "beyond",
        "children", "could", "should", "would", "friend", "good", "great", "him", "herself",
        "immediate", "little", "letter", "myself", "necessary", "neither", "paid", "perceive",
        "perhaps", "quick", "receive", "rejoice", "said", "such", "themselves", "today",
        "together", "tomorrow", "tonight", "your",
        "stronger", "longest", "standing", "motherly", "fatherhood", "knowingly",
        "questioning", "rightful", "someone", "underneath", "youngest", "working",
        "The quick brown fox jumps over the lazy dog.",
        "A bird in the hand is worth two in the bush.",
        "To be or not to be, that is the question.",
        "All that glitters is not gold.",
        "In the beginning God created the heaven and the earth.",
        "It was the best of times, it was the worst of times.",
        "Call me Ishmael.", "I wandered lonely as a cloud.",
        "The lady doth protest too much, methinks.",
        "Knowledge is power.", "Time is money.", "Practice makes perfect.",
        "Life is what happens when you're busy making other plans.",
        "antidisestablishmentarianism", "supercalifragilisticexpialidocious",
        "floccinaucinihilipilification", "pseudopseudohypoparathyroidism",
        "U.S.A.", "NASA", "UNESCO", "HTML", "CSS",
        "user@example.com", "https://www.liblouis.org",
        "Word  word   word", "  Leading and trailing  ",
        "© ® ™", "€ £ ¥", "α β γ",
    ]

    for inp in new_test_inputs:
        if inp not in all_inputs:
            all_inputs.append(inp)

    # Add more random sentences to reach 400 total
    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "apple", "banana", "cherry"]
    while len(all_inputs) < 400:
        sentence = " ".join(random.choices(words, k=6)).capitalize() + "."
        if sentence not in all_inputs:
            all_inputs.append(sentence)
            
    with open('verification_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'input_text', 'expected_brf'])
        for i, text in enumerate(all_inputs):
            writer.writerow([i+1, text, ""])

if __name__ == "__main__":
    generate()
    print("Generated verification_data.csv with 400 test cases.")
