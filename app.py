from flask import Flask, render_template

app = Flask(__name__)

# Student login and Registration
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_details():
    # Write to sqlite
    return render_template('registered.html')

#Admin routes
@app.route('/admin/login', methods=['GET'])
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
@app.route('/admin/dashboard', methods=['GET','POST'])
def admin_dashboard():
    return

# Add Subject
@app.route('/admin/dashboard/New_s', methods=['GET','POST'])
def new_subject():
    return

# New Chapter
@app.route('/admin/dashboard/New_c', methods=['GET', 'POST'])
def new_chapter():
    return


#Quiz Management
@app.route('/admin/quiz', methods=['GET', 'POST'])
def quiz_management():
    return

@app.route('/admin/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    return

@app.route('/admin/quiz/newq', methods=['GET', 'POST'])
def add_question():
    return

# Admin_summary
@app.route('/admin/summary', methods=['GET', 'POST'])
def admin_summary():
    return



# student routes
@app.route('/student/dashboard', methods=['GET', 'POST'])
def student_dashboard():
    return

# Attempting the quiz
@app.route('/student/att_quiz', methods=['GET', 'POST'])
def a_quiz():
    return

# View upcoming quiz
@app.route('/student/view_quiz', methods=['GET', 'POST'])
def view_quiz():
    return

#View Quiz Scores
@app.route('/student/scores', methods=['GET', 'POST'])
def view_scores():
    return

#summary
@app.route('/student/summary', methods=['GET', 'POST'])
def student_summary():
    return
# App routes (For admin)
# Admin_dashboard - New Subject, New chapter, 
# Quiz Management - Add Quiz, New question
# Summary

# App routes (for student)
# Dashboard
# Quiz_Attempt
# ViewQuiz
# Scores
if __name__ == '__main__':
    app.run(debug=True)