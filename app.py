from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "supersecretkey"

client = MongoClient('mongodb://localhost:27017/')
db = client['movie_tracker']

@app.route('/')
def index():
    return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        user_id = db.users.count_documents({}) + 1
        db.users.insert_one({'id': user_id, 'username': uname, 'email': email, 'password': pwd})
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        # Admin check
        if uname == 'admin' and pwd == '1001':
            return redirect('/admin')

        user = db.users.find_one({'username': uname, 'password': pwd})

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    movies = list(db.movies.find())

    return render_template('home.html', movies=movies)


@app.route('/search')
def search():
    query = request.args.get('query')
    if 'user_id' not in session:
        return redirect('/login')
    
    results = list(db.movies.find({'title': {'$regex': query, '$options': 'i'}}))
    
    return render_template('home.html', movies=results)
    

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    if request.method == 'POST':
        if 'review' in request.form:
            review = request.form['review']
            db.reviews.insert_one({'user_id': user_id, 'movie_id': movie_id, 'review': review})
        elif 'status' in request.form:
            status = request.form['status']
            db.wishlist.replace_one({'user_id': user_id, 'movie_id': movie_id}, {'user_id': user_id, 'movie_id': movie_id, 'status': status}, upsert=True)

    movie = db.movies.find_one({'id': movie_id})
    if not movie:
        return "Movie not found", 404
    reviews = list(db.reviews.find({'movie_id': movie_id}))
    return render_template('movie_detail.html', movie=movie, reviews=reviews)

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    if request.method == 'POST':
        movie_id = int(request.form['movie_id'])
        new_status = request.form['status']
        db.wishlist.update_one({'user_id': user_id, 'movie_id': movie_id}, {'$set': {'status': new_status}})
        return redirect('/wishlist')

    pipeline = [
        {'$match': {'user_id': user_id}},
        {'$lookup': {'from': 'movies', 'localField': 'movie_id', 'foreignField': 'id', 'as': 'movie'}},
        {'$unwind': '$movie'},
        {'$project': {'id': '$movie.id', 'title': '$movie.title', 'status': 1}}
    ]
    wishlist_items = list(db.wishlist.aggregate(pipeline))
    return render_template('wishlist.html', wishlist=wishlist_items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    movies = list(db.movies.find())
    users = list(db.users.find())

    if request.method == 'POST':
        # Adding new movie to the database
        title = request.form['title']
        description = request.form['description']
        movie_id = db.movies.count_documents({}) + 1
        db.movies.insert_one({'id': movie_id, 'title': title, 'description': description})

        return redirect('/admin')

    return render_template('admin.html', users=users, movies=movies)


# Update Movie Description Route
@app.route('/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    new_description = request.form['new_description']
    
    # Update the movie description in the database
    result = db.movies.update_one({'id': movie_id}, {'$set': {'description': new_description}})
    if result.matched_count == 0:
        return "Movie not found", 404

    return redirect('/admin')

# Delete Movie Route
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    # Delete the movie from the database
    result = db.movies.delete_one({'id': movie_id})
    if result.deleted_count == 0:
        return "Movie not found", 404

    return redirect('/admin')

@app.route('/add_to_wishlist/<int:movie_id>')
def add_to_wishlist(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']

    # Check if movie exists
    movie = db.movies.find_one({'id': movie_id})
    if not movie:
        return "Movie not found", 404

    # Check if already in wishlist
    existing = db.wishlist.find_one({'user_id': user_id, 'movie_id': movie_id})
    
    if not existing:
        db.wishlist.insert_one({'user_id': user_id, 'movie_id': movie_id, 'status': 'Want to Watch'})
    
    return redirect('/wishlist')

@app.route('/update_status/<int:movie_id>', methods=['GET', 'POST'])
def update_status_page(movie_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    # Check if movie exists
    movie = db.movies.find_one({'id': movie_id})
    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        new_status = request.form.get('status')
        db.wishlist.update_one({'user_id': session['user_id'], 'movie_id': movie_id}, {'$set': {'status': new_status}})
        return redirect('/wishlist')
    
    return render_template('update_status.html', movie_id=movie_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
