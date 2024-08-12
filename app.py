#imoprting libraries

import io
import json

import numpy as np
import sympy as sp
from scipy import integrate
import html
import markdown

from flask import Flask, render_template, request, redirect, url_for, session,send_file, flash,jsonify,send_from_directory
import os
import time
import requests

from werkzeug.security import generate_password_hash, check_password_hash
import csv
import Tuning
import logging
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,PageBreak






app = Flask(__name__)
app.secret_key = 'myflaskapp'


#profile pic
app.config['UPLOAD_FOLDER'] = 'static/profile_pics/'  # Folder for profile pictures
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16 MB

#  user data
users = {
    "Saurab": generate_password_hash("thisispass"),
    "Shubham": generate_password_hash("thisispass"),
    "Krishna": generate_password_hash("thisispass")
}

user_data = {
    "Saurab": {"questions_solved": 0, "profile_pic": None, "daily_time_spent": 0, "questions_asked": 0, "todos_completed": 0, "questions_without_help": 0},
    "Shubham": {"questions_solved": 0, "profile_pic": None, "daily_time_spent": 0, "questions_asked": 0, "todos_completed": 0, "questions_without_help": 0},
    "Krishna": {"questions_solved": 0, "profile_pic": None, "daily_time_spent": 0, "questions_asked": 0, "todos_completed": 0, "questions_without_help": 0}
}
def load_questions(path):                                      #loading questions to
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    questions = []
    current_question = ''

    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace

        if line:  # If line is not empty after stripping whitespace
            current_question += line + '\n'  # Add line to current question text
        elif current_question:  # If line is empty and we have accumulated a question
            questions.append(current_question.strip())  # Append current question to questions list
            current_question = ''  # Reset current question string

    # Append the last question if there's any remaining
    if current_question:
        questions.append(current_question.strip())

    return questions


@app.route('/set_theme', methods=['POST'])
def set_theme():
    data = request.get_json()
    theme = data.get('theme')
    if theme in ['standard', 'dark']:
        session['theme'] = theme
        return jsonify(success=True)
    return jsonify(success=False), 400

def fetch_quote():
    try:
        response = requests.get('https://api.quotable.io/random')
        if response.status_code == 200:
            data = response.json()
            return f'"{data["content"]}" - {data["author"]}'
        else:
            return 'Failed to fetch quote'
    except requests.exceptions.RequestException as e:
        return f'Failed to fetch quote: {str(e)}'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            session['start_time'] = time.time()  # Track login time
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/set_view_mode/<mode>')
def set_view_mode(mode):
    if mode in ['standard', 'modern']:
        session['view_mode'] = mode
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        quote = fetch_quote()
        return render_template('dashboard.html', username=session['username'], quote=quote)
    else:
        return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        user_info = user_data[username]

        if request.method == 'POST':
            if 'profile_pic' in request.files:
                file = request.files['profile_pic']
                if file and file.filename != '':
                    filename = f"{username}_profile_pic.jpg"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    user_info['profile_pic'] = filename

            # Increment questions solved (dummy logic, can be changed)
            if 'increment_questions' in request.form:
                user_info['questions_solved'] += 1

            return redirect(url_for('profile'))

        return render_template('profile.html', user_info=user_info, username=username)
    else:
        return redirect(url_for('login'))


@app.route('/badges')
def badges():
    return render_template('badges.html')

@app.route('/user_level')
def user_level():
    return render_template('user_level.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/activity_log')
def activity_log():
    return render_template('activity_log.html')

@app.route('/profile_settings')
def profile_settings():
    return render_template('profile_settings.html')


@app.route('/select_subject', methods=['GET', 'POST'])
def select_subject():
    if 'username' in session:
        if request.method == 'POST':
            subject = request.form['subject']
            session['subject'] = subject
            return redirect(url_for('subject', subject_name=subject))
        return render_template('select_subject.html')
    else:
        return redirect(url_for('login'))

@app.route('/subject/<subject_name>', methods=['GET', 'POST'])
def subject(subject_name):
    if 'username' in session:
        if subject_name == 'physics':
            questions = load_questions('physics_questions.txt')
            num_questions = len(questions)
            session['subject'] = subject_name
            session['num_questions'] = num_questions
            return render_template('physics_questions.html', questions=enumerate(questions, start=1), solved_questions=user_data[session['username']]['questions_solved'])
        elif subject_name in ['maths', 'chemistry']:
            flash(f"{subject_name.capitalize()} Coming Soon!")
            return render_template('dashboard.html', username=session['username'])
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/select_year')
def select_year():
    if 'username' in session:
        years = list(range(2008, 2025))
        return render_template('select_year.html', years=years)
    else:
        return redirect(url_for('login'))

@app.route('/select_shift/<int:year>')
def select_shift(year):
    if 'username' in session:
        shifts = ['Shift 1', 'Shift 2']
        return render_template('select_shift.html', year=year, shifts=shifts)
    else:
        return redirect(url_for('login'))

@app.route('/previous_year_questions/<int:year>/<shift>')
def previous_year_questions(year, shift):
    if 'username' in session:
        # Load the previous year questions based on the selected year and shift
        # For now, just a placeholder
        questions = [f"Question {i+1} for {year} {shift}" for i in range(10)]
        return render_template('previous_year_questions.html', questions=questions, year=year, shift=shift)
    else:
        return redirect(url_for('login'))

@app.route('/timer/<int:qid>')
def timer(qid):
    start_time = time.time()
    return redirect(url_for('solve_question', qid=qid, timer=start_time))

@app.route('/solve_question/<int:qid>', methods=['GET', 'POST'])
def solve_question(qid):
    if 'username' in session and 'subject' in session and 'num_questions' in session:
        subject = session['subject']
        num_questions = session['num_questions']

        questions = load_questions(f'{subject}_questions.txt')  # Adjust path based on subject

        if qid > num_questions or qid < 1:
            return redirect(url_for('dashboard'))

        question = questions[qid - 1].strip()
        timer = request.args.get('timer', 0, type=int)

        return render_template('solve_question.html', question=question, qid=qid, num_questions=num_questions, timer=timer)
    else:
        return redirect(url_for('login'))

@app.route('/explain_question', methods=['POST'])
def explain_question_route():
    question = request.form['question']
    explanation = Tuning.explain_question(question)
    return explanation

@app.route('/generate_hint', methods=['POST'])
def generate_hint_route():
    question = request.form['question']
    hint = Tuning.generate_hint(question)
    return hint

@app.route('/get_formulae', methods=['POST'])
def get_formulae_route():
    question = request.form['question']
    formulae = Tuning.get_formulae(question)
    return formulae

@app.route('/get_solution', methods=['POST'])
def get_solution_route():
    question = request.form['question']
    solution = Tuning.get_solution(question)
    return solution

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' in session:
        if request.method == 'POST':
            feedback_text = request.form['feedback']
            problem = request.form['problem']
            with open('feedback.txt', 'a') as file:
                file.write(f'{session["username"]}: {problem} - {feedback_text}\n')
            flash('Thank you for your feedback!')
        return render_template('feedback.html')
    else:
        return redirect(url_for('login'))

@app.route('/ask_questions', methods=['GET', 'POST'])
def ask_questions():
    if 'username' in session:
        if request.method == 'POST':

            asked_question = request.form['question']
            user_data[session['username']]['questions_asked'] += 1
            with open(f'_questions.txt', 'a') as file:
                file.write(f'{asked_question}\n\n')
            ans = Tuning.answer_asked_question(asked_question)
            return render_template('questions.html', answer=ans)
        return render_template('questions.html')
    else:
        return redirect(url_for('login'))

@app.route('/personalized_study_plan', methods=['GET', 'POST'])
def personalized_study_plan():
    if request.method == 'POST':
        study_details = request.form['study_details']
        study_plan = Tuning.generate_study_plan(study_details)
        return render_template('study_plan.html', study_plan=study_plan)
    return render_template('personalized_study_plan.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobileno = request.form['mobileno']
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        dob = request.form['dob']

        # Save user data to CSV
        with open('user_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, email, mobileno, newpassword, confirmpassword, dob])

        return redirect(url_for('sign_in'))

    return render_template('sign_in.html')


app.config['REFERENCE_BOOK_FOLDER'] = 'pdfs'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the 'pdfs' directory exists at the root level of your project
pdf_directory = os.path.join(app.root_path, app.config['REFERENCE_BOOK_FOLDER'])
if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)

@app.route('/get_pdfs')
def get_pdfs():
    if 'username' in session:
        try:
            reference_book_folder = app.config['REFERENCE_BOOK_FOLDER']
            logging.debug(f"REFERENCE_BOOK_FOLDER: {reference_book_folder}")

            # Verify the directory exists
            if not os.path.isdir(reference_book_folder):
                raise FileNotFoundError(f"Directory '{reference_book_folder}' does not exist")

            pdfs = [f for f in os.listdir(reference_book_folder) if f.endswith('.pdf')]
            logging.debug(f"PDFs found: {pdfs}")

            return jsonify(pdfs)
        except Exception as e:
            logging.error("Error fetching PDFs: %s", str(e))
            return jsonify({"error": str(e)}), 500
    else:
        return redirect(url_for('login'))

@app.route('/pdfs/<filename>')
def open_pdf(filename):
    try:
        return send_from_directory(pdf_directory, filename)
    except FileNotFoundError:
        flash('File not found!', 'error')
        return redirect(url_for('reference_book'))

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'username' in session:
        if 'pdfFile' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('reference_book'))
        file = request.files['pdfFile']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('reference_book'))
        if file and file.filename.lower().endswith('.pdf'):
            file.save(os.path.join(pdf_directory, file.filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('reference_book'))
        else:
            flash('Invalid file type. Please upload a PDF file.', 'error')
            return redirect(url_for('reference_book'))
    else:
        return redirect(url_for('login'))


@app.route('/notifications')
def notifications():
    return render_template('notice.html')
@app.route('/reference_book')
def reference_book():
    if 'username' in session:
        if not os.path.exists(pdf_directory):
            flash('PDF directory not found!', 'error')
            return redirect(url_for('dashboard'))
        books = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        return render_template('reference_page.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    try:
        return send_from_directory(pdf_directory, filename, as_attachment=True)
    except FileNotFoundError:
        flash('File not found!', 'error')
        return redirect(url_for('reference_book'))




@app.route('/formula_sheet')
def formula_sheet():
    return render_template('formula_sheet.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)



# In-memory storage for to-do items
# In-memory storage for to-do items
todo_items = []

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'username' in session:
        if request.method == 'POST':
            item_text = request.form.get('item')
            time_frame = request.form.get('time_frame')
            if item_text:
                todo_items.append({
                    'text': item_text,
                    'completed': False,
                    'time_frame': time_frame
                })
            return redirect(url_for('todo'))
        return render_template('todo.html', todo_items=todo_items)
    else:
        return redirect(url_for('login'))

@app.route('/complete_todo/<int:item_id>', methods=['POST'])
def complete_todo(item_id):
    if 'username' in session:
        if 0 <= item_id < len(todo_items):
            todo_items[item_id]['completed'] = True
        return redirect(url_for('todo'))
    else:
        return redirect(url_for('login'))


@app.route('/motivational_videos')
def motivational_videos():
    return render_template('motivational_videos.html')


@app.route('/peerstudygroup')
def peerstudygroup():
    return render_template('peerstudygroup.html')

# Route for performance tracker page
@app.route('/performance_tracker', methods=['GET', 'POST'])
def performance_tracker():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            # Retrieve performance data from the form
            daily_time_spent = request.form.get('daily_time_spent')
            questions_solved = request.form.get('questions_solved')
            todos_completed = request.form.get('todos_completed')
            timetable_followed = request.form.get('timetable_followed')
            hours_studied = request.form.get('hours_studied')
            test_marks = request.form.get('test_marks')
            questions_without_help = request.form.get('questions_without_help')

            # Save the performance data to a CSV file
            with open(f'{username}_performance.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([daily_time_spent, questions_solved, todos_completed, timetable_followed, hours_studied, test_marks, questions_without_help])

            flash('Performance data saved successfully!')

        return render_template('performance_tracker.html', username=username)
    else:
        return redirect(url_for('login'))

def extract_questions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    questions = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        # Extract questions based on some heuristic or format
        questions += text.split('\n')  # Example, adjust as needed
    return questions

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf = request.files['pdf']
        num_questions = int(request.form['num_questions'])
        time_frame = int(request.form['time_frame'])

        pdf_path = f"./uploads/{pdf.filename}"
        pdf.save(pdf_path)
        questions = extract_questions_from_pdf(pdf_path)
        selected_questions = questions[:num_questions]

        return render_template('test.html', questions=selected_questions, time_frame=time_frame)

    return render_template('index.html')

@app.route('/submit_test', methods=['POST'])
def submit_test():
    # Handle test submission here
    answers = request.form.to_dict()
    # Process the answers
    return redirect(url_for('result_page'))

@app.route('/generate_test', methods=['POST'])
def generate_test():
    # Generate the test and pass necessary data to the template
    time_frame = request.form.get('time_frame', 30)  # Default to 30 minutes if not provided
    questions = ["Question 1", "Question 2"]  # Replace with actual questions
    return render_template('test.html', time_frame=time_frame, questions=questions)


@app.route('/result_page')
def result_page():
    # Example result page
    return "Results will be displayed here."

@app.route('/notice')     #for notice page
def notice():
    return render_template('notice.html')

@app.route('/syllabus_tracker')     #for syllabus tracker  page
def syllabus_tracker():
    return render_template('syllabus_tracker.html')


@app.route('/maths_syllabus_tracker')     #for syllabus tracker  page
def maths_syllabus_tracker():
    return render_template('maths_syllabus_tracker.html')

@app.route('/physics_syllabus_tracker')     #for syllabus tracker  page
def physics_syllabus_tracker():
    return render_template('physics_syllabus_tracker.html')

@app.route('/chemistry_syllabus_tracker')     #for syllabus tracker  page
def chemistry_syllabus_tracker():
    return render_template('chemistry_syllabus_tracker.html')


@app.route('/more_features')     #for More Features  page
def more_features():
    return render_template('more_features.html')


# Function to fetch data from Wikipedia API
def fetch_wikipedia_data(query):
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    response = requests.get(api_url)
    data = response.json()

    if 'query' in data and 'search' in data['query']:
        # Extracting the first search result
        search_results = data['query']['search']
        if search_results:
            top_result = search_results[0]
            title = top_result.get('title', 'No title found.')
            snippet = top_result.get('snippet', 'No snippet found.')
            page_id = top_result.get('pageid', 'No page ID found.')
            page_url = f"https://en.wikipedia.org/?curid={page_id}"
            return f"{title}: {snippet}...\nMore details at: {page_url}"
        else:
            return "No search results found."
    else:
        return "No data found."

# Function to fetch data from a news API (example: NewsAPI.org)
def fetch_news_data(query):
    api_url = f"https://newsapi.org/v2/everything?q={query}&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(api_url)
    data = response.json()

    if 'articles' in data and data['articles']:
        # Extracting the first article
        top_article = data['articles'][0]
        title = top_article.get('title', 'No title found.')
        description = top_article.get('description', 'No description found.')
        url = top_article.get('url', 'No URL found.')
        return f"{title}: {description}...\nRead more at: {url}"
    else:
        return "No news articles found."

# Enhanced function to fetch data from multiple sources
def fetch_external_data(query):
    wikipedia_result = fetch_wikipedia_data(query)
    news_result = fetch_news_data(query)

    return f"Wikipedia:\n{wikipedia_result}\n\nNews:\n{news_result}"

# Function to handle chatbot responses
def get_chatbot_response(user_input):
    user_input = user_input.lower()

    if "acejee ai" in user_input:
        return "Step Mentor is a comprehensive AI system designed to assist students in their JEE preparation. How can I help you with AceJee AI?"
    elif any(greeting in user_input for greeting in ["hello", "hi", "hlw", "hey"]):
        return "Hello! How can I help you with AceJee AI today?"
    elif "how can you help me" in user_input:
        return "I can help you in your JEE preparation."
    elif "i am Saurab" in user_input or "Saurab" in user_input:
        return "Hello, creator! Are you eager to introduce a new feature today?"
    elif any(farewell in user_input for farewell in ["bye", "goodbye"]):
        return "Goodbye! Have a great day!"
    elif "latest news" in user_input:
        # Fetch and return real-time data
        return fetch_external_data("latest news about JEE")
    else:
        # Fetch and return general data from Wikipedia and news sources
        return fetch_external_data(user_input)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get("message")
    response = get_chatbot_response(user_input)
    return jsonify({"response": response})


@app.route('/create_notes')
def create_notes():
    return render_template('notes_making.html')

@app.route('/notes_making', methods=['POST'])
def notes_making():
    notes = request.form['notes']
    solution = Tuning.generate_notes(notes)

    sanitized_solution = html.escape(solution)
    html_solution = markdown.markdown(sanitized_solution)

    return jsonify({'solution': html_solution})

@app.route('/save_notes_as_pdf', methods=['POST'])
def save_notes_as_pdf():
    data = request.json
    notes = data.get('notes', '')
    response = data.get('response', '')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading1']

    story.append(Paragraph("Notes:", heading_style))
    story.append(Spacer(1, 12))
    for paragraph in notes.split('\n'):
        story.append(Paragraph(paragraph, normal_style))
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    story.append(Paragraph("Generated Response:", heading_style))
    story.append(Spacer(1, 12))
    for paragraph in html.unescape(response).split('\n'):
        story.append(Paragraph(paragraph, normal_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="notes.pdf",
        mimetype="application/pdf"
    )

@app.route('/ai_calculations')     #for More Features  page
def ai_calculations():
    return render_template('ai_calculations.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    equation = data['equation']
    parameters = data['parameters']

    try:
        # Parse parameters
        param_dict = {}
        if parameters:
            param_pairs = parameters.split(',')
            for pair in param_pairs:
                key, value = pair.split('=')
                param_dict[key.strip()] = float(value.strip())

        # Use sympy for symbolic calculations
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(equation)

        # If it's an equation, solve it
        if '=' in equation:
            left, right = equation.split('=')
            expr = sp.Eq(sp.sympify(left), sp.sympify(right))
            result = sp.solve(expr)
        else:
            # If parameters are provided, substitute and evaluate
            if param_dict:
                result = expr.subs(param_dict).evalf()
            else:
                result = expr

        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    simulation_type = data['simulationType']
    iterations = data['iterations']
    parameters = json.loads(data['parameters']) if data['parameters'] else {}

    try:
        if simulation_type == 'randomWalk':
            result = random_walk(iterations)
        elif simulation_type == 'heatDiffusion':
            result = heat_diffusion(iterations, parameters)
        elif simulation_type == 'monteCarlo':
            result = monte_carlo(iterations, parameters)
        elif simulation_type == 'fluidDynamics':
            result = fluid_dynamics(iterations, parameters)
        else:
            return jsonify({'error': 'Invalid simulation type'}), 400

        return jsonify({
            'message': f'{simulation_type} simulation completed successfully.',
            'data': result.tolist() if isinstance(result, np.ndarray) else result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def random_walk(iterations):
    return np.cumsum(np.random.normal(0, 1, iterations))


def heat_diffusion(iterations, parameters):
    # Simplified 1D heat diffusion
    alpha = parameters.get('alpha', 0.1)
    dx = parameters.get('dx', 0.1)
    dt = parameters.get('dt', 0.01)
    L = parameters.get('L', 1.0)

    x = np.linspace(0, L, int(L / dx))
    u = np.zeros(len(x))
    u[0] = parameters.get('initialTemp', 100)

    for _ in range(iterations):
        u[1:-1] += alpha * dt / dx ** 2 * (u[2:] - 2 * u[1:-1] + u[:-2])

    return u


def monte_carlo(iterations, parameters):
    # Example: Estimate pi
    inside_circle = 0
    total_points = iterations

    for _ in range(total_points):
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        if x ** 2 + y ** 2 <= 1:
            inside_circle += 1

    pi_estimate = 4 * inside_circle / total_points
    return pi_estimate


def fluid_dynamics(iterations, parameters):
    # Simplified 1D Burgers' equation
    nu = parameters.get('nu', 0.01)
    dx = parameters.get('dx', 0.01)
    dt = parameters.get('dt', 0.001)
    L = parameters.get('L', 1.0)

    x = np.linspace(0, L, int(L / dx))
    u = np.sin(2 * np.pi * x)

    for _ in range(iterations):
        u[1:-1] = u[1:-1] - u[1:-1] * dt / dx * (u[1:-1] - u[:-2]) + \
                  nu * dt / dx ** 2 * (u[2:] - 2 * u[1:-1] + u[:-2])

    return u

@app.route('/ar_vr_experience')     #for More Features  page
def ar_vr_experience():
    return render_template('ar_vr_experience.html')


@app.route('/event')     #for More Features  page
def event():
    return render_template('events.html')

@app.route('/ai_content')     #for More Features  page
def ai_content():
    return render_template('ai_content.html')


@app.route('/mental_health')
def mental_health():
    return render_template('mental_health.html')

@app.route('/meditation')
def meditation():
    return render_template('meditation.html')

@app.route('/resource_library')
def resource_library():
    return render_template('resource_library.html')

@app.route('/lab_simulations')
def lab_simulations():
    return render_template('lab_simulations.html')

@app.route('/quizes')
def quizes():
    return render_template('quizes.html')

@app.route('/personalize_quizzes')
def personalize_quizzes():
    return render_template('personalize_quizes.html')


@app.route('/create_career_map')
def create_career_map():
    return render_template('career_mapping.html')

@app.route('/career_mapping', methods=['POST'])
def career_mapping():
    data = request.json
    career_input = data.get('career', '')

    recommendations = Tuning.generate_career_map(career_input)

    return jsonify({'recommendations': recommendations})



@app.route('/virtual_experience')
def virtual_experience():
    return render_template('virtual_experiences.html')

@app.route('/expert_mentor')
def expert_mentor():
    return render_template('expert_mentor.html')

@app.route('/student_community')
def student_community():
    return render_template('student_community.html')



@app.route('/important-dates')
def important_dates():
    return render_template('important_dates.html')



@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        start_time = session.get('start_time', time.time())
        end_time = time.time()
        time_spent = end_time - start_time
        user_data[username]['daily_time_spent'] += time_spent

        with open(f'{username}_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Daily Time Spent', 'Questions Solved', 'Questions Asked', 'To-Dos Completed', 'Questions Without Help'])
            writer.writerow([username, user_data[username]['daily_time_spent'], user_data[username]['questions_solved'], user_data[username]['questions_asked'], user_data[username]['todos_completed'], user_data[username]['questions_without_help']])

        session.pop('username', None)
        session.pop('start_time', None)
        flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)