# 🎬 Movie Wishlist Tracker

A full-stack web application for discovering, tracking, and reviewing movies. Users can create wishlists, track their viewing status, and share reviews with the community.

## 📋 Project Overview

Movie Wishlist Tracker is a web application that allows users to:
- ❤️ **Discover** movies added by the admin
- 📝 **Wishlist** movies they plan to watch
- ✅ **Track** their viewing status (Want to Watch, Watching, Watched)
- 💬 **Leave reviews** and read other users' reviews
- 🔐 **Secure authentication** with user accounts

Admin users have special privileges to manage the movie database by adding, updating, and deleting movies.

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB (NoSQL)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Language Composition**:
  - HTML: 65%
  - Python: 30.3%
  - CSS: 4.7%

## 📁 Project Structure

```
Movie_wishlist_tracker/
├── app.py                 # Main Flask application
├── db.sql                 # Database schema (legacy reference)
├── templates/             # HTML templates
│   ├── admin.html        # Admin dashboard
│   ├── home.html         # Movie listing page
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   ├── movie_detail.html # Movie detail view
│   ├── wishlist.html     # User's wishlist
│   └── update_status.html # Update movie status
├── static/               # Static files
│   └── style.css         # Application styling
├── uploads/              # User uploads directory
└── README.md             # Project documentation
```

## ✨ Features

### User Features
- **User Authentication**
  - Sign up with username, email, and password
  - Secure login
  - Session management

- **Movie Discovery**
  - Browse all available movies
  - Search movies by title
  - View detailed movie information and reviews

- **Wishlist Management**
  - Add movies to personal wishlist
  - Track viewing status (Want to Watch, Watching, Watched)
  - Update status for tracked movies
  - Remove movies from wishlist

- **Reviews & Community**
  - Read reviews from other users
  - Post personal reviews and ratings
  - Engage with the community

### Admin Features
- **Movie Management**
  - Add new movies to the database
  - Update movie descriptions
  - Delete movies from the system
  - View all users and movies
  - Admin credentials: username `admin`, password `1001`

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MongoDB (running locally on port 27017)
- Flask
- PyMongo

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dhodduraaj/Movie_wishlist_tracker.git
   cd Movie_wishlist_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install flask pymongo
   ```

3. **Set up MongoDB**
   - Ensure MongoDB is running on `localhost:27017`
   - The application will automatically create the database on first run

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - You will be redirected to the signup page

## 🔐 Authentication

### Regular User
1. Create an account via signup page
2. Log in with your credentials
3. Access the movie catalog and manage your wishlist

### Admin Access
1. Click on login
2. Enter credentials:
   - **Username**: `admin`
   - **Password**: `1001`
3. Access admin dashboard to manage movies and users

## 📊 Database Schema

### Collections/Tables

**users**
- `id`: User ID
- `username`: Username
- `email`: Email address
- `password`: Password (plaintext - see security notes)

**movies**
- `id`: Movie ID
- `title`: Movie title
- `description`: Movie description

**wishlist**
- `id`: Wishlist entry ID
- `user_id`: Reference to user
- `movie_id`: Reference to movie
- `status`: Tracking status (Want to Watch, Watching, Watched)

**reviews**
- `id`: Review ID
- `user_id`: Reference to user
- `movie_id`: Reference to movie
- `review`: Review text

## 📝 Available Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirects to signup |
| `/signup` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/home` | GET | Browse movies |
| `/search` | GET | Search movies by title |
| `/movie/<id>` | GET, POST | View movie details & reviews |
| `/wishlist` | GET, POST | View & manage wishlist |
| `/add_to_wishlist/<id>` | GET | Add movie to wishlist |
| `/update_status/<id>` | GET, POST | Update movie status |
| `/admin` | GET, POST | Admin dashboard |
| `/update_movie/<id>` | POST | Update movie description |
| `/delete_movie/<id>` | POST | Delete movie |
| `/logout` | GET | Logout user |

## ⚠️ Security Notes

**Important**: This project is a learning/development project. Please note the following security considerations:

1. **Passwords**: Currently stored in plaintext. In production, use password hashing (e.g., bcrypt, werkzeug.security)
2. **Secret Key**: `app.secret_key = "supersecretkey"` should be changed to a secure random value
3. **Admin Credentials**: Hardcoded in the application. Use environment variables in production
4. **Input Validation**: Implement proper input validation and sanitization
5. **MongoDB Connection**: No authentication used. Secure MongoDB with credentials
6. **SQL Injection/NoSQL Injection**: Implement proper parameterization and validation

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Dhodduraaj**
- GitHub: [@Dhodduraaj](https://github.com/Dhodduraaj)

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Last Updated**: May 2026
**Status**: Active Development
