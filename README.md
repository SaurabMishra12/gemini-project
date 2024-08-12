# Step Mentor

Brief about the Idea: The idea involves developing a system that helps the Students practice questions. It will generate clear problem statements using GenAI, suggest relevant formulas, and present solutions step-by-step in the given time frame; the prototype features GenAI API for question descriptions and chatbot and machine learning for formula suggestions. Opportunity : How different is it from any other existing ideas out there? The proposed model stands out with its comprehensive learning support, leveraging advanced technologies like Prompt Engineering and Machine learning. It offers a personalized learning experience akin to having a personal tutor. These features distinguish it from existing platforms, ensuring a unique and effective study tool for JEE students. The dataset used for practising questions is imported from Online Data Lakes; some of the questions are handpicked from this dataset to show the potential of the prototypes in handling the different levels of questions.

How will it be able to solve the problem?

The app solves the problem of effective question practice for JEE students through several key mechanisms: Comprehensive Guidance: By providing step-by-step solutions, formula suggestions, and chatbot assistance, the app guides students through the question-solving process, ensuring they understand each step thoroughly. Free Accessibility: Offering free access to all users, the app removes cost barriers and ensures inclusivity, allowing students from diverse backgrounds to benefit from high-quality educational support. Empowerment through Practice: By facilitating regular practice and providing detailed explanations and assistance, the app empowers students to develop their problem-solving skills and deepen their understanding of physics concepts, ultimately improving their performance in the JEE exam.

List of features offered by the solution :

GenAI Question Description: Automatically generate clear and concise descriptions for questions using the Prompt Engineering and GenAI model.

• Stepwise Solution Presentation: Divide solutions into step-by-step explanations, guiding students through each problem-solving stage.

• The platform offers a range of innovative features to enhance the learning experience. It includes a Reference Book with digital textbooks and academic resources, a Formulae Sheet for quick access to essential formulas, and Practice Tests that users can customize for exam preparation. Performance Analytics provide visual insights into progress, while Peer Study Groups facilitate collaborative learning. Users can manage their tasks with To-Do Lists and track important academic Dates with a calendar. The Syllabus Tracker monitors progress on coursework, and the Student Community offers a space for interaction and support. Important updates are shared through the Notice feature, and daily Latest Quotes provide motivation. Quizzes offer interactive assessments, and Expert Mentorship connects users with guidance from professionals. A comprehensive Resource Library includes various educational materials, and Mental Health and Wellness resources support overall well-being. AI-driven Note-Taking tools help organize and summarize information, while VR and AR Experiences offer immersive learning opportunities. AI-Powered Content generates personalized study materials, and users can attend Virtual Events and Webinars hosted by experts. The platform also includes AI-Powered Career Mapping for planning career paths, Virtual Lab Simulations for conducting experiments, and AI-Powered Scientific Calculations to assist with complex calculations.

• Formula Suggestions: Analyze question contexts and suggest relevant formulas to users to aid problem-solving.

• Chatbot Assistance: Integrate a chatbot assistant powered by GenAI to provide real-time support, explanations, and tips for solving questions.

• Web Dashboard: Provide a user-friendly web-based dashboard for easy navigation, question selection, and access to features.

• User Authentication: Implement secure user authentication to ensure privacy and access control.

• Question Practice: Offer students a comprehensive database of questions from previous years of JEE to practice and improve their skills.

• Personalized Learning: Adapt to each student's pace and needs, providing customized guidance and support throughout the learning process.

• Feedback Mechanism: Incorporate a feedback mechanism for users to provide input, report issues, and suggest improvements.

• Free Accessibility: Provide free access to all features, ensuring inclusivity and affordability for students from diverse backgrounds.

Technology used :

The "StepMentor" could utilize Google GenAI tools for machine learning, data processing and prompt engineering. Specifically:

Streamlit is used to create an interactive web application. Pandas manages and processes the user data, such as saving which buttons were clicked or handling login information. PIL and Fitz are used for processing images of questions that users upload, extracting the text or relevant information. Pytesseract performs OCR on these images to convert the text into a format that can be processed and analyzed by your application. Scikit-learn: Used for model development. Google Generative AI is used to generate hints, explanations, or solutions for the questions users ask, providing a sophisticated, AI-driven tutoring experience. io is used for handling file operations, such as reading and writing the CSV files that store user data and feedback.
