import sqlite3
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = 'admin'


# Student login and Registration
@app.route('/', methods=['GET', 'POST'])
def login():
    # Get part is simply generating the page
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # very password and login and redirect to dashboard
        return

@app.route('/register', methods=['GET'])
def register():
    # Simply Generate Template here, nothing to do more
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_details():
    # Write to sqlite
    return render_template('registered.html')


admin_username = "admin"
admin_password = "password"
#Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if ((username == admin_username) and (password == admin_password)):
            session['user'] = admin_username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', login_fail = 1)
        
# Admin Dashboard
@app.route('/admin/dashboard', methods=['GET','POST'])
def admin_dashboard():
    # List of subjects
    subjects_new = []

    # Extract list of subjects and ID
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM subjects")
    rows = cursor.fetchall()
    print(rows)

    # Add subjects in dictionary
    for row in rows:
        subjects_new.append({ 'id': row[0], 'name': row[1], 'chapters': []})

    # Initialize the dictionary for 
    for i in range(len(subjects_new)):
        chapters = []
        cursor.execute("SELECT id, name FROM chapters WHERE subject_id = ?", (subjects_new[i]['id'],))
        db_chapters = cursor.fetchall()
        for chapter in db_chapters:
            cursor.execute("SELECT COUNT(*) FROM questions where chapter_id = ?", (chapter[0],))
            noq = cursor.fetchall()
            chapters.append({'id': chapter[0], 'name': chapter[1], 'noq': noq[0][0]})
        subjects_new[i]['chapters'] = chapters
    

    # Scan for each ID and create list for chapters

    return render_template('admin_dashboard.html', subjects=subjects_new)

# Edit Chapter
@app.route('/admin/edit_chapter/')
def edit_chapter(chapter_id, subject_id):
    return render_template("edit chapter", chapter_id = chapter_id, subject_id = subject_id)

# Delete Chapter
@app.route('/admin/delete_chapter/')
def delete_chapter(chapter_id, subject_id):
    return

# New Chapter
@app.route('/admin/dashboard/New_c', methods=['GET', 'POST'])
def new_chapter(subject_id):
    return

# Add Subject
@app.route('/admin/dashboard/New_s', methods=['GET','POST'])
def new_subject():
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