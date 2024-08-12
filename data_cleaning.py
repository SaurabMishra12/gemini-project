import pandas as pd

# Load the CSV file
file_path = 'C:/Users/msaur/Documents/projects python/step_mentor_project/subjects-questions.csv'
data = pd.read_csv(file_path)

# Print the column names to debug
print("Column names in the CSV file:", data.columns)

# Create dictionaries to hold questions for each subject
questions = {
    'Physics': [],
    'Chemistry': [],
    'Maths': [],
    'Biology': []
}

# Assuming the CSV has columns 'Subject' and 'eng' (for questions)
for _, row in data.iterrows():
    subject = row['Subject']
    question = row['eng']
    if subject in questions:
        questions[subject].append(question)

# Save questions to separate text files with each question on a new line, numbered sequentially
for subject, qs in questions.items():
    with open(f'{subject.lower()}questions.txt', 'w', encoding='utf-8') as f:
        for i, question in enumerate(qs, start=1):
            f.write(f"{i}. {question}\n\n")

print("Questions have been separated and saved into text files.")
