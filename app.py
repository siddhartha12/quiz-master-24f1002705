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
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        output = cursor.fetchall()
        user_id = output[0][0]
        db_password = output[0][1]

        if db_password == password:
            session['user'] = username 
            conn.close()
            return redirect(url_for('student_dashboard', user_id = user_id))
        
        else:   
            return redirect(url_for('login'))
        
@app.route('/register', methods=['GET'])
def register():
    # Simply Generate Template here, nothing to do more
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_details():
    # Initialize SQL
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # Retreive variables from form
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    qualification = request.form.get('qualification')

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    users = cursor.fetchall()
    if (len(users) == 0):
        # NO users with the same username, safe to register
        cursor.execute("INSERT INTO users(name, username, password, Qualification) VALUES (?, ?, ?, ?)", (name, username, password, qualification))
        conn.commit()
        return render_template('registered.html')

    else:
        return render_template('registration.html', message='Invalid Username')

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
    subjects = []

    # Extract list of subjects and ID
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM subjects")
    rows = cursor.fetchall()
    print(rows)

    # Add subjects in dictionary
    for row in rows:
        subjects.append({ 'id': row[0], 'name': row[1], 'chapters': []})

    # Initialize the dictionary for 
    for i in range(len(subjects)):
        chapters = []
        cursor.execute("SELECT id, name FROM chapters WHERE subject_id = ?", (subjects[i]['id'],))
        db_chapters = cursor.fetchall()
        for chapter in db_chapters:
            cursor.execute("SELECT COUNT(*) FROM questions where chapter_id = ?", (chapter[0],))
            noq = cursor.fetchall()
            chapters.append({'id': chapter[0], 'name': chapter[1], 'noq': noq[0][0]})
        subjects[i]['chapters'] = chapters
    

    # Scan for each ID and create list for chapters
    conn.close()
    return render_template('admin_dashboard.html', subjects=subjects)

# Edit Chapter
@app.route('/admin/edit_chapter/', methods=['GET','POST'])
def edit_chapter():
    # Get the chapter and the subject ids
    chapter_id = int(request.args.get('chapter_id'))
    subject_id = int(request.args.get('subject_id'))
    # Get method
    if request.method == 'GET':
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Get properties of the chapter
        cursor.execute("SELECT name, description FROM chapters WHERE id = ?", (chapter_id,))
        output = cursor.fetchall()
        print(output)
        chapter_name = output[0][0]
        description = output[0][1]

        # Get properties of the subject
        cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
        subject_name_db = cursor.fetchall()
        subject_name = subject_name_db[0][0]

        #Initialize dict for page input
        chapter = {'subject_id': subject_id, 'subject_name': subject_name, 'id': chapter_id, 'name': chapter_name, 'description': description}

        # Display the things on the html webpage
        conn.commit()
        conn.close()
        return render_template('edit_chapter.html', chapter=chapter)

    
    # Post method
    elif request.method == 'POST':
        print("post")
        print(subject_id)
        print(chapter_id)
        # Get from form
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Modify into the Database
        cursor.execute("UPDATE chapters SET name = ?, description = ? WHERE id = ?", (name, description, chapter_id))

        # Commit into db
        conn.commit()

        # close db
        conn.close()

        # redirect to dashboard
        return redirect(url_for('admin_dashboard'))

# Delete Chapter
@app.route('/admin/delete_chapter/', methods=['GET', 'POST'])
def delete_chapter():
    # Get the chapter and the subject ids
    chapter_id = int(request.args.get('chapter_id'))
    subject_id = int(request.args.get('subject_id'))
    # Get method
    if request.method == 'GET':
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Get properties of the chapter
        cursor.execute("SELECT name, description FROM chapters WHERE id = ?", (chapter_id,))
        output = cursor.fetchall()
        print(output)
        chapter_name = output[0][0]
        description = output[0][1]

        # Get properties of the subject
        cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
        subject_name_db = cursor.fetchall()
        subject_name = subject_name_db[0][0]

        #Initialize dict for page input
        chapter = {'subject_id': subject_id, 'subject_name': subject_name, 'id': chapter_id, 'name': chapter_name, 'description': description}

        # Display the things on the html webpage
        conn.commit()
        conn.close()
        return render_template('delete_chapter.html', chapter=chapter)

    
    # Post method
    elif request.method == 'POST':
        print("post")
        print(subject_id)
        print(chapter_id)
        
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Modify into the Database
        cursor.execute("DELETE FROM chapters WHERE id = ? AND subject_id = ?", (chapter_id, subject_id))

        # Commit into db
        conn.commit()

        # close db
        conn.close()

        # redirect to dashboard
        return redirect(url_for('admin_dashboard'))

    return

# New Chapter
@app.route('/admin/dashboard/New_c', methods=['GET', 'POST'])
def new_chapter():
    # Get subject id
    subject_id = int(request.args.get('subject_id'))

    # If method = get
    if request.method =='GET':

        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Retreive subject name
        cursor.execute("SELECT name FROM subjects WHERE id = ?", (subject_id,))
        name_output = cursor.fetchall()
        name = name_output[0][0]
        subject = {'name' : name, 'id': subject_id}
        conn.close()
        return render_template("new_chapter.html", subject=subject)
    
    elif request.method == 'POST':
        # Open Database
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        name = request.form.get('name')
        description = request.form.get('description')

        # Insert chapter into the table
        cursor.execute("INSERT INTO chapters( subject_id, name, description) VALUES (?, ?, ?)", (subject_id, name, description))

        # close connection
        conn.commit()
        conn.close()

        # redirect to dashboard
        return redirect(url_for("admin_dashboard"))
        




    return

# Add Subject
@app.route('/admin/dashboard/New_s', methods=['GET','POST'])
def new_subject():
    if request.method == 'GET':
        return render_template("new_subject.html")
    elif request.method == 'POST':
        # Get fields
        name = request.form.get('name')
        description = request.form.get('description')

        # Open db
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # write to db
        cursor.execute('INSERT INTO subjects(name, description) VALUES (?, ?)', (name, description))

        # close db
        conn.commit()
        conn.close()

        return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard/subject', methods=['GET', 'POST'])
def edit_subject():
    # retreive subject id
    subject_id = int(request.args.get('subject_id'))
    # if get
    if request.method =='GET':
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Retrieve information
        cursor.execute('SELECT name, description FROM subjects WHERE id = ?', (subject_id,))
        output = cursor.fetchall()
        name = output[0][0]
        description = output[0][1]
        subject = {'id': subject_id,'name': name,'description': description}

        # Display on page
        conn.close()
        return render_template("edit_subject.html", subject=subject)
    
    elif request.method == 'POST':
        # Retreive form information
        description = request.form.get('description')
        
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # write to subject
        cursor.execute("UPDATE subjects SET description = ? WHERE id = ?", (description, subject_id))

        # commit and close
        conn.commit()
        conn.close()

        return redirect(url_for('admin_dashboard'))


    # IF request post

@app.route('/admin/dashboard/subject/delete', methods=['GET', 'POST'])
def delete_subject():
    # retreive subject id
    subject_id = int(request.args.get('subject_id'))
    # if get
    if request.method =='GET':
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # Retrieve information
        cursor.execute('SELECT name, description FROM subjects WHERE id = ?', (subject_id,))
        output = cursor.fetchall()
        name = output[0][0]
        description = output[0][1]
        subject = {'id': subject_id,'name': name,'description': description}

        # Display on page
        conn.close()
        return render_template("delete_subject.html", subject=subject)
    
    elif request.method == 'POST':
        # Open Database
        conn = sqlite3.connect("app.db")    
        cursor = conn.cursor()

        # write to subject
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))

        # commit and close
        conn.commit()
        conn.close()

        return redirect(url_for('admin_dashboard'))


#Quiz Management
@app.route('/admin/quiz', methods=['GET', 'POST'])
def quiz_management():
    quizzes_send = []
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM quizzes")
    quizzes = cursor.fetchall()
    for quiz in quizzes:
        id = quiz[0]
        name = quiz[1]
        questions =[]
        cursor.execute('SELECT id, name FROM questions WHERE quiz_id = ?', (id,))
        quizzes = cursor.fetchall()
        for quiz in quizzes:
            question_id = quiz[0]
            question_name = quiz[1]
            questions.append({'id': question_id, 'name': question_name})
        quizzes_send.append({'id': id, 'name': name, 'questions': questions})

    conn.close()
    return render_template('quiz_management.html', quizzes = quizzes_send)

# View upcoming quiz
@app.route('/admin/quiz/view', methods=['GET', 'POST'])
def view_quiz():
    # Get quiz id
    quiz_id = request.args.get('quiz_id')

    #establish connection with db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # get from db
    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    output = cursor.fetchall()

    #initialize values from tuple
    name = output[0][1]
    subject_id = output[0][2]
    chapter_id = output[0][3]
    date = output[0][4]
    duration = output[0][5]
    remarks = output[0][6]

    # extract subject name
    cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
    sub_name_db = cursor.fetchall()
    subject = sub_name_db[0][0]

    #extract chapter name
    cursor.execute('SELECT name FROM chapters WHERE id = ?', (chapter_id,))
    ch_name_db = cursor.fetchall()
    chapter = ch_name_db[0][0]

    #Define dictionary for html
    # INSERT INTO quizzes(id, name, subject_id, chapter_id, date_of_quiz, time_duration, remarks)
    quiz = {'name': name,'subject': subject,'chapter': chapter,'date': date, 'duration': duration, 'remarks': remarks}

    # Close connection
    conn.close()

    # Render Webpage
    return render_template('view_quiz.html', quiz=quiz)

@app.route('/admin/quiz/add', methods=['GET', 'POST'])
def new_quiz():
    return

@app.route('/admin/quiz/newq', methods=['GET', 'POST'])
def new_question():
    return

@app.route('/admin/quiz/deleteq', methods=['GET', 'POST'])
def delete_question():
    return

@app.route('/admin/quiz/editq', methods=['GET', 'POST'])
def edit_question():
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