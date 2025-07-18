import sqlite3
from flask import Flask, redirect, render_template, request, url_for, session
import time

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
        print(output)

        if output == []:
            return redirect(url_for('login'))
        
        user_id = output[0][0]
        db_password = output[0][1]

        if db_password == password:
            session['user_id'] = user_id
            conn.close()
            return redirect(url_for('student_dashboard'))
        
        else:   
            return redirect(url_for('login'))

# User Registration
@app.route('/register', methods=['GET'])
def register():
    # Simply Generate Template here, nothing to do more
    return render_template('registration.html')

# Registering the user into the db
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

#Admin routes
#Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #Open DB
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM admins WHERE username = ?', (username,))
        output = cursor.fetchall()
        admin_password = output[0][0]

        if ((password == admin_password)):
            session['user'] = username
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
        cursor.execute("DELETE FROM quizzes WHERE chapter_id = ? AND subject_id = ?", (chapter_id, subject_id))
        cursor.execute("DELETE FROM questions WHERE chapter_id = ? AND subject_id = ?", (chapter_id, subject_id))

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

# Edit Subject
@app.route('/admin/dashboard/subject', methods=['GET', 'POST'])
def edit_subject():
    # retrieve subject id
    subject_id = int(request.args.get('subject_id'))

    # if using get
    if request.method =='GET':
        # Open Db
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

# Delete Subject
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
        cursor.execute("DELETE FROM chapters WHERE subject_id = ?", (subject_id,))
        cursor.execute("DELETE FROM quizzes WHERE subject_id = ?", (subject_id,))
        cursor.execute("DELETE FROM questions WHERE subject_id = ?", (subject_id,))
        
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
@app.route('/admin/quiz/edit', methods=['GET', 'POST'])
def edit_quiz(): 
    # Get quiz id
    quiz_id = request.args.get('quiz_id')

    #establish connection with db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # get from db
    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    output = cursor.fetchall()

    #initialize values from tuple
    id = output[0][0]
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
    quiz = {'id': id, 'name': name,'subject': subject,'chapter': chapter,'date': date, 'duration': duration, 'remarks': remarks}

    # Close connection
    conn.close()

    # Render Webpage
    return render_template('edit_quiz.html', quiz=quiz)

# Delete Quiz
@app.route('/admin/quiz/delete', methods=['GET','POST'])
def delete_quiz():
    # Get quiz id
    quiz_id = request.args.get('quiz_id')

    #establish connection with db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    #delete from db
    cursor.execute('DELETE FROM quizzes WHERE id = ?', (quiz_id,))
    cursor.execute('DELETE FROM questions WHERE quiz_id = ?', (quiz_id,))

    #commit
    conn.commit()

    #close db
    conn.close()

    return redirect(url_for('quiz_management'))

# New Quiz
@app.route('/admin/quiz/add', methods=['GET', 'POST'])
def new_quiz():
    if request.method == 'GET':
        #establish connection with db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # retreieve list of subject id and name from db
        cursor.execute('SELECT id, name FROM subjects')
        subjects_db = cursor.fetchall()

        # initliaze dictionary for render page
        subjects = []
        for subject in subjects_db:
            subjects.append({'id': subject[0], 'name': subject[1]})

        # retreive list of chapters from db
        cursor.execute('SELECT id, name FROM chapters')
        chapters_db = cursor.fetchall()

        # initialize dictionary for render page
        chapters = []
        for chapter in chapters_db:
            chapters.append({'id': chapter[0], 'name': chapter[1]})

        # close db
        conn.close()

        #return template
        return render_template('new_quiz.html', subjects = subjects, chapters=chapters)

    elif request.method == 'POST':
        # extract from form
        name = request.form.get('name')
        subject = int(request.form.get('subject'))
        chapter = int(request.form.get('chapter'))
        date = request.form.get('date')
        time = request.form.get('duration')
        remarks = request.form.get('remarks')

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # Write to db
        cursor.execute('INSERT INTO quizzes(name, subject_id, chapter_id, date_of_quiz, time_duration, remarks) VALUES (?, ?, ?, ?, ?, ?)', (name, subject, chapter, date, time, remarks))

        # Commit db
        conn.commit()

        #Close db
        conn.close()
        
        return redirect(url_for('quiz_management'))
        #return render_template('new_quiz.html')

# New Questions
@app.route('/admin/quiz/newq', methods=['GET', 'POST'])
def new_question():
    # if get
    if request.method == 'GET':
        # retrieve quiz_id from form
        quiz_id = request.args.get('quiz_id')

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # find chapter, subject and quiz name from quiz_id
        cursor.execute('SELECT chapter_id, subject_id FROM quizzes WHERE id = ?', (quiz_id,))
        output = cursor.fetchall()
        chapter_id = output[0][0]
        subject_id = output[0][1]

        #chapter name
        cursor.execute('SELECT name FROM chapters WHERE id = ?', (chapter_id,))
        output = cursor.fetchall()
        chapter_name = output[0][0]

        # quiz name
        cursor.execute('SELECT name FROM quizzes WHERE id = ?', (quiz_id,))
        output = cursor.fetchall()
        quiz_name = output[0][0]

        #subject name
        cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
        output = cursor.fetchall()
        subject_name = output[0][0]

        # initialize dict
        quiz = {'id': quiz_id, 'name': quiz_name, 'chapter_id': chapter_id, 'chapter_name': chapter_name, 'subject_id': subject_id, 'subject_name': subject_name}

        # close db
        conn.close()

        # output page
        return render_template("new_question.html", quiz=quiz)

    # if post
    elif request.method =='POST':
        # retreieve query elements
        quiz_id = request.args.get('quiz_id')
        chapter_id = request.args.get('chapter_id')
        subject_id = request.args.get('subject_id')

        # retreive form elements
        name = request.form.get('name')
        question = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = int(request.form.get('correct'))

        #open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # write db
        cursor.execute('INSERT INTO questions (name, quiz_id, chapter_id, subject_id, question_statement, option1, option2, option3, option4, correct_option) VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (name, quiz_id, chapter_id, subject_id, question, a, b, c, d, correct))

        # commit db
        conn.commit()

        # close db
        conn.close()

        # redirect back to home
        return redirect(url_for('quiz_management'))

# Delete Question
@app.route('/admin/quiz/deleteq', methods=['GET', 'POST'])
def delete_question():
    # if method get
    if request.method == 'GET':
        # Get question and quiz info from arg
        quiz_id = int(request.args.get('quiz_id'))
        question_id = int(request.args.get('question_id'))

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # find quiz_name and chapter_name
        cursor.execute('SELECT name, question_statement FROM questions WHERE id = ? AND quiz_id = ?', (question_id,quiz_id))
        output = cursor.fetchall()
        name = output[0][0]
        question = output[0][1]

        # Create Dictionary for page
        question = {'id': question_id, 'name': name, 'question': question}

        #close db
        conn.close()

        # generate page
        return render_template("delete_question.html", question=question)
    
    elif request.method == 'POST':
        # get question_id from args
        question_id = request.args.get('question_id')

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # find quiz_name and chapter_name
        cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))

        # commit db
        conn.commit()

        # close db
        conn.close()

        # redirect to quiz Management
        return redirect(url_for('quiz_management'))



    return

# Edit Question
@app.route('/admin/quiz/editq', methods=['GET', 'POST'])
def edit_question():
    # if method get
    if request.method == 'GET':
        # Get question and quiz info from arg
        question_id = int(request.args.get('question_id'))

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # find quiz_name and chapter_name
        cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
        output_db = cursor.fetchall()
        output = output_db[0]
        # questions ( id, name, quiz_id, chapter_id, subject_id, question_statement, option1, option2, option3, option4, correct_option);
        question_id = int(output[0])
        name = output[1]
        quiz_id = int(output[2])
        chapter_id = int(output[3])
        subject_id = int(output[4])
        question = output[5]
        a = output[6]
        b = output[7]
        c = output[8]
        d = output[9]
        correct = output[10]

        # Get chapter
        cursor.execute('SELECT name FROM chapters WHERE id = ?', (chapter_id, ))
        output = cursor.fetchall()
        chapter_name = output[0][0]

        # get subject
        cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id, ))
        output = cursor.fetchall()
        subject_name = output[0][0]

        # Create Dictionary for page
        question = {'id': question_id, 'name': name, 'chapter_name': chapter_name, 'subject_name':subject_name, 'question': question, 'a':a, 'b':b, 'c':c, 'd':d, 'correct':correct}

        #close db
        conn.close()

        # generate page
        return render_template("edit_question.html", question=question)
    
    elif request.method =='POST':
        # retreieve query elements
        question_id = request.args.get('question_id')

        # retreive form elements
        name = request.form.get('name')
        question = request.form.get('question')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        correct = int(request.form.get('correct'))

        #open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # write db
        cursor.execute('UPDATE questions SET name = ?, question_statement = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct_option = ? WHERE id = ?',
                       (name, question, a, b, c, d, correct, question_id))

        # commit db
        conn.commit()

        # close db
        conn.close()

        # redirect back to home
        return redirect(url_for('quiz_management'))
    return

# Admin_summary
@app.route('/admin/summary', methods=['GET', 'POST'])
def admin_summary():
    # Open db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # No. of attempts for each quiz and average score, highest scorer
    cursor.execute('SELECT COUNT(*), AVG(total_scored), MAX(total_scored), quiz_id FROM scores GROUP BY quiz_id')
    output = cursor.fetchall()
    quiz_scores = []
    subject_scores = []
    for row in output:
        noattempts = row[0]
        average = row[1]
        max = row[2]
        quiz_id = row[3]

        cursor.execute('SELECT name FROM quizzes WHERE id = ?', (quiz_id,))
        output = cursor.fetchall()
        quiz_name = output[0][0]

        quiz_scores.append({'id': quiz_id, 'name': quiz_name, 'attempts': noattempts, 'avg': average, 'max': max})

    # Subject wise user attempts
    cursor.execute('SELECT COUNT(*), AVG(total_scored), MAX(total_scored), subject_id FROM scores INNER JOIN quizzes ON scores.quiz_id = quizzes.id GROUP BY subject_id')
    output = cursor.fetchall()

    for row in output:
        noattempts = row[0]
        average = row[1]
        max = row[2]
        subject_id = row[3]

        cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
        output = cursor.fetchall()
        subject_name = output[0][0]

        subject_scores.append({'id': subject_id, 'name': subject_name, 'attempts': noattempts, 'avg': average, 'max': max})

    conn.close()

    return render_template('admin_summary.html', quizzes= quiz_scores, subjects=subject_scores)

# Search for admin
@app.route('/admin/search', methods=['GET','POST'])
def admin_search():
    # Admin can search users, subjects, chapters, quizzes
    # If get
    if request.method =='GET':
        return render_template('admin_search.html')
    # If post
    if request.method == 'POST':
        # First get the term from the form
        query = request.form.get('query')
        type = request.form.get('option')
        formatted_query = f"%{query}%"

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        
        users = []
        subjects = []
        chapters = []
        quizzes = []

        # If users
        if type == 'users':
            # Get a list of users
            cursor.execute('SELECT * FROM users WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            for row in output:
                # users(id, name, username, Qualification);
                users.append({'id': row[0], 'username': row[1], 'qualification': row[2]})

        # IF subject
        if type  == 'subjects':
            # Get a list of users
            cursor.execute('SELECT * FROM subjects WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # users(id, name, username, Qualification);
                subjects.append({'id': row[0], 'name': row[1], 'description': row[2]})

        # if chapter
        if type  == 'chapters':
            # Get a list of users
            cursor.execute('SELECT * FROM chapters WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # users(id, name, username, Qualification);
                cursor.execute('SELECT name FROM subjects WHERE id = ?', (row[1],))
                subject_db = cursor.fetchall()
                subject_name = subject_db[0][0]
                chapters.append({'id': row[0], 'subject_name': subject_name, 'name': row[2], 'description': row[3]})

        # if quiz
        if type  == 'quizzes':
            # Get a list of users
            cursor.execute('SELECT * FROM quizzes WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # quizzes(id, name, subject_id, chapter_id, date_of_quiz, time_duration, remarks TEXT)
                quizzes.append({'id': row[0], 'name': row[1], 'description': row[6], 'subject_id': row[2], 'chapter_id': row[3], 'date': row[4], 'duration': row[5]})

        conn.close()

        return render_template('admin_search_results.html', users=users, subjects=subjects, chapters=chapters, quizzes=quizzes)

# Log abmind out
@app.route('/admin/logout')
def admin_logout():
    session.clear()

    return redirect(url_for('login'))

# student routes
# Student Dashboard
@app.route('/student/dashboard', methods=['GET', 'POST'])
def student_dashboard():
    user_id = session['user_id']

    #open db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes WHERE date_of_quiz = date('now')")
    quizzes_today_db = cursor.fetchall()

    quizzes = []
    for quiz in quizzes_today_db:
        id = quiz[0]
        cursor.execute('SELECT * FROM scores WHERE user_id = ? AND quiz_id = ?', (user_id, id))
        out = cursor.fetchall()
        print(out)
        not_attempted = 1
        if len(out) != 0:
            not_attempted = 0
        name = quiz[1]
        duration = quiz[5]
        cursor.execute('SELECT COUNT(*) FROM questions WHERE quiz_id = ?', (id,))
        output = cursor.fetchall()
        noq = output[0][0]

        quizzes.append({'id': id, 'name': name, 'duration': duration, 'noq': noq, 'not_attempted': not_attempted})

    cursor.execute("SELECT * FROM quizzes WHERE date_of_quiz > date('now')")
    upcoming_quizzes_db = cursor.fetchall()

    upcoming_quizzes = []
    for quiz in upcoming_quizzes_db:
        id = quiz[0]
        name = quiz[1]
        date = quiz[4]
        duration = quiz[5]
        cursor.execute('SELECT COUNT(*) FROM questions WHERE quiz_id = ?', (id,))
        output = cursor.fetchall()
        noq = output[0][0]

        upcoming_quizzes.append({'id': id, 'name': name, 'date': date,'duration': duration, 'noq': noq})

    return render_template('user_dashboard.html', quizzes=quizzes, upcoming_quizzes = upcoming_quizzes)

# Seeing the details of the quiz
@app.route('/student/quiz/view', methods=['GET', 'POST'])
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
    id = output[0][0]
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
    quiz = {'id': id, 'name': name,'subject': subject,'chapter': chapter,'date': date, 'duration': duration, 'remarks': remarks}

    # Close connection
    conn.close()

    # Render Webpage
    return render_template('view_quiz.html', quiz=quiz)

# Start the quiz
@app.route('/student/quiz/start', methods=['GET', 'POST'])
def start_quiz():
    quiz_id = request.args.get('quiz_id')
    session['quiz_id'] = quiz_id
    session['current_question'] = 0
    session['start_time'] = time.time()
    session['answers'] = []
    session['correct'] = []

    return redirect(url_for('attempt_quiz'))

# Start attempt
@app.route('/student/quiz/attempt', methods=['GET', 'POST'])
def attempt_quiz():
    quiz_id = session['quiz_id']

    # Connect db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM questions WHERE quiz_id =  ?', (quiz_id,))
    output_db = cursor.fetchall()

    
    if session['current_question'] > len(output_db):
        return redirect(url_for('submit_quiz'))

    output = output_db[session['current_question']]

    conn.close()

    question_id = int(output[0])
    question = output[5]
    a = output[6]
    b = output[7]
    c = output[8]
    d = output[9]

    question = {'id': question_id, 'quiz_id': quiz_id, 'question': question, 'a': a, 'b': b, 'c': c, 'd': d,}
    return render_template('attempt_question.html', question = question)

# Submit route for each individual question
@app.route('/student/quiz/submit_question', methods=['POST'])
def submit_answer():
    option = int(request.form.get('option'))

    question_id = request.args.get('question_id')

    # Connect db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # Get answers from questions
    cursor.execute('SELECT correct_option FROM questions WHERE id = ?', (question_id, ))
    output = cursor.fetchall()
    correct = output[0][0]

    cursor.execute('SELECT COUNT(*) FROM questions WHERE id = ?', (question_id,))
    output = cursor.fetchall()
    noq = output[0][0]

    conn.close()

    
    session['correct'].append(correct)
    session['answers'].append(option)

    session['current_question'] += 1

    if session['current_question'] >= noq:
        return redirect(url_for('submit_quiz'))

    return redirect(url_for('attempt_quiz'))

# Submit the entire quiz (available at every question)
@app.route('/student/quiz/submit_quiz', methods=['GET','POST'])
def submit_quiz():
    score = 0
    for i in range(len(session['correct'])):
        if session['answers'][i] == session['correct'][i]:
            score += 1
    
    # Connect db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    quiz_id = session['quiz_id']
    user_id = session['user_id']

    cursor.execute('INSERT INTO scores(quiz_id, user_id, total_scored) VALUES (?, ?, ?)', (quiz_id, user_id, score))
    # scores(id, quiz_id, user_id, time_stamp_of_attempt, total_scored);

    conn.commit()
    conn.close()

    return redirect(url_for('student_dashboard'))

# View Past Quiz Scores
@app.route('/student/scores', methods=['GET', 'POST'])
def view_scores():
    user_id = session['user_id']

    #open db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scores WHERE user_id = ?", (user_id,))
    scores_db = cursor.fetchall()

    scores = []
    for score in scores_db:
        #TABLE(id, quiz_id, user_id, time_stamp_of_attempt, total_scored);
        id = score[1]
        #date
        cursor.execute('SELECT name FROM quizzes WHERE id = ?', (id,))
        output = cursor.fetchall()
        name = output[0][0]
        #no of questions
        cursor.execute('SELECT COUNT(*) FROM questions WHERE quiz_id = ?', (id,))
        output = cursor.fetchall()
        noq = output[0][0]

        timestamp = score[3]

        user_score = score[4]
        scores.append({'id': id, 'name': name, 'noq': noq, 'timestamp': timestamp, 'score': user_score})

    conn.close()

    return render_template("view_scores.html", scores=scores)

# Student summary
@app.route('/student/summary', methods=['GET', 'POST'])
def student_summary():
    # Open db
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Average score of all quizzes
    # No of quizzes attempted
    cursor.execute('SELECT COUNT(*), AVG(total_scored) FROM scores WHERE user_id = ?', (session['user_id'],))
    output = cursor.fetchall()

    stats = {'no': 0, 'avg': 0}
    stats['no'] = output[0][0]
    stats['avg'] = output[0][1]

    #Subject wise quizzes marks
    cursor.execute('SELECT COUNT(*), AVG(total_scored), MAX(total_scored), subject_id FROM scores INNER JOIN quizzes ON scores.quiz_id = quizzes.id WHERE user_id = ? GROUP BY subject_id', (session['user_id'],))
    output = cursor.fetchall()

    chapter_stats = []
    for row in output:
        noa = row[0]
        avg = row[1]
        max = row[2]
        subject_id = row[3]

        chapter_stats.append({'id': subject_id, 'noa': noa, 'avg': avg, 'max': max})

    #Month wise no. of quizzes
    cursor.execute("SELECT strftime('%m', date_of_quiz) AS month, COUNT(*) FROM quizzes GROUP BY month")
    output = cursor.fetchall()

    monthwise = []
    for row in output:
        monthwise.append({'month': row[0], 'count': row[1]})

    return render_template('user_summary.html', chapters = chapter_stats, months=monthwise)

# Student Search
@app.route('/student/search', methods=['GET', 'POST'])
def student_search():
    # Student can search Subjects, Chapters, and Quizzes
    # If get
    if request.method =='GET':
        return render_template('user_search.html')
    # If post
    if request.method == 'POST':
        # First get the term from the form
        query = request.form.get('query')
        type = request.form.get('option')
        formatted_query = f"%{query}%"

        # Open db
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        subjects = []
        chapters = []
        quizzes = []

        # IF subject
        if type  == 'subjects':
            # Get a list of users
            cursor.execute('SELECT * FROM subjects WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # users(id, name, username, Qualification);
                subjects.append({'id': row[0], 'name': row[1], 'description': row[2]})

        # if chapter
        if type  == 'chapters':
            # Get a list of users
            cursor.execute('SELECT * FROM chapters WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # users(id, name, username, Qualification);
                cursor.execute('SELECT name FROM subjects WHERE id = ?', (row[1],))
                subject_db = cursor.fetchall()
                subject_name = subject_db[0][0]
                chapters.append({'id': row[0], 'subject_name': subject_name, 'name': row[2], 'description': row[3]})

        # if quiz
        if type  == 'quizzes':
            # Get a list of users
            cursor.execute('SELECT * FROM quizzes WHERE name LIKE ?', (formatted_query,))
            output = cursor.fetchall()
            
            for row in output:
                # quizzes(id, name, subject_id, chapter_id, date_of_quiz, time_duration, remarks TEXT)
                quizzes.append({'id': row[0], 'name': row[1], 'description': row[6], 'subject_id': row[2], 'chapter_id': row[3], 'date': row[4], 'duration': row[5]})

        conn.close()

        return render_template('user_search_results.html', subjects=subjects, chapters=chapters, quizzes=quizzes)

# Log student out
@app.route('/student/logout')
def student_logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)