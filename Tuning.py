import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyAhJ41L42PQLRRsIaGns8eXnkx0hPA0Q88"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-1.5-pro')

def answer_asked_question(ask_question):
    request_answer = " show me the correct detailed solution of  ) ", ask_question
    api_response_answer = model.generate_content(request_answer)
    return api_response_answer.text

def image_asked_question(questions_image):
    request_image_solution= "Show me the solution of question shown in the image", questions_image
    api_response_image_solution = model.generate_content(request_image_solution)
    return api_response_image_solution

def explain_question(question):
    request_explaination=" Explain the following problem statement only without providing any solution", question
    api_response_explaination=model.generate_content(request_explaination)
    return api_response_explaination.text

def get_solution(question):
    request_solution= " show me the correct detailed solution of  ) ",question
    api_response_sol= model.generate_content(request_solution)
    return api_response_sol.text

def generate_hint(question):
    request_hint = " show me only the hint needed to solve this  ) ", question
    api_response_hint = model.generate_content(request_hint)
    return api_response_hint.text

def get_formulae(question):
    request_formulae="provide the relevant formula(s) for solving it:don't give me the solution or answer",question
    api_response_formulae=model.generate_content(request_formulae)
    return api_response_formulae.text

def generate_study_plan(study_details):
    request_study_plan = f"Generate a personalized study plan for the following details: {study_details}"
    api_response_study_plan = model.generate_content(request_study_plan)
    return api_response_study_plan.text


def generate_notes(notes_details):    #for notes making
    request_notes_making = f"Generate a detail notes on the following details: {notes_details}"
    api_response_notes_making= model.generate_content(request_notes_making)
    return api_response_notes_making.text

def generate_career_map(career_details):
    request_career_map = f"Generate a personalized career map with insights, recommendations, and industry trends for the following details: {career_details}"
    api_response_career_map = model.generate_content(request_career_map)
    return api_response_career_map.text
