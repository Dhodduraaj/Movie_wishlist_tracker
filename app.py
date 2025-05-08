from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # your MySQL password
    database="movie_tracker"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (uname, email, pwd))
        conn.commit()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        # Always execute and fetch to clear results
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        user = cursor.fetchone()

        # Admin check (handled after query is fetched)
        if uname == 'admin' and pwd == '1001':
            return redirect('/admin')

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template('login.html')

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL password
        database="movie_tracker"
    )


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # This returns rows as dictionaries
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()

    return render_template('home.html', movies=movies)


@app.route('/search')
def search():
    query = request.args.get('query')
    if 'user_id' not in session:
        return redirect('/login')
    
    cursor.execute("SELECT * FROM movies WHERE title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    
    return render_template('home.html', movies=results)
    

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    if request.method == 'POST':
        if 'review' in request.form:
            review = request.form['review']
            cursor.execute("INSERT INTO reviews (user_id, movie_id, review) VALUES (%s, %s, %s)", (user_id, movie_id, review))
        elif 'status' in request.form:
            status = request.form['status']
            cursor.execute("REPLACE INTO wishlist (user_id, movie_id, status) VALUES (%s, %s, %s)", (user_id, movie_id, status))
        conn.commit()

    cursor.execute("SELECT * FROM movies WHERE id=%s", (movie_id,))
    movie = cursor.fetchone()
    cursor.execute("SELECT review FROM reviews WHERE movie_id=%s", (movie_id,))
    reviews = cursor.fetchall()
    return render_template('movie_detail.html', movie=movie, reviews=reviews)

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    if request.method == 'POST':
        movie_id = request.form['movie_id']
        new_status = request.form['status']
        cursor.execute("""
            UPDATE wishlist 
            SET status = %s 
            WHERE user_id = %s AND movie_id = %s
        """, (new_status, user_id, movie_id))
        conn.commit()
        return redirect('/wishlist')

    cursor.execute("""
        SELECT m.id, m.title, w.status 
        FROM wishlist w 
        JOIN movies m ON w.movie_id = m.id 
        WHERE w.user_id = %s
    """, (user_id,))
    wishlist_items = cursor.fetchall()
    return render_template('wishlist.html', wishlist=wishlist_items)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL password
        database="movie_tracker"
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get movies and users
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if request.method == 'POST':
        # Adding new movie to the database
        title = request.form['title']
        description = request.form['description']
        cursor.execute("INSERT INTO movies (title, description) VALUES (%s, %s)", (title, description))
        conn.commit()

        return redirect('/admin')

    conn.close()
    return render_template('admin.html', users=users, movies=movies)


# Update Movie Description Route
@app.route('/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    new_description = request.form['new_description']
    
    # Update the movie description in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET description = %s WHERE id = %s", (new_description, movie_id))
    conn.commit()
    conn.close()

    return redirect('/admin')

# Delete Movie Route
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    # Delete the movie from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    conn.close()

    return redirect('/admin')

@app.route('/add_to_wishlist/<int:movie_id>')
def add_to_wishlist(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    # Check if already in wishlist
    cursor.execute("SELECT * FROM wishlist WHERE user_id = %s AND movie_id = %s", (user_id, movie_id))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("INSERT INTO wishlist (user_id, movie_id, status) VALUES (%s, %s, %s)",
                       (user_id, movie_id, "Want to Watch"))
        conn.commit()
    
    return redirect('/wishlist')

@app.route('/update_status/<int:movie_id>', methods=['GET', 'POST'])
def update_status_page(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        new_status = request.form.get('status')
        cursor.execute("""
            UPDATE wishlist 
            SET status = %s 
            WHERE user_id = %s AND movie_id = %s
        """, (new_status, session['user_id'], movie_id))
        conn.commit()
        return redirect('/wishlist')
    
    return render_template('update_status.html', movie_id=movie_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
