# pathfinder.com
An educative blog website written with the flask framework that inspires young people on 
purpose, good and quality relationships, and also communicates good principles with 
fictions. It's a modified version of pathfinder.org located in my repository, including 
more functionalities, more features and new databases.

# Features
- User authentication: Users can create an account, log in using Flask-Login or Google authentication using Google OAuth2.
- View Stories: Registered users can gain access to limitless content ranging from blog posts on purpose, to knowing more about how quality relationships work to reading inspiring stories that can foster transformation.
- Search Feature: This feature helps users quickly find relevant stories that match their interest or needs, making it easier for them to discover new content and stay engaged with our blog.
- Download books: If reading is not enough and you want a piece of the content with you always, we have a download section where books can be downloaded for free.
- Commenting: Users can comment on which stories inspired them the most.
- Newsletter: Users can subscribe to our newsletter with their email addresses to receive updates on our latest blog posts.
- Contact the Author: Users can reach out to the author beyond subscribing to the mail list in case there are more things the user wants to know about beyond the blog posts.

# Technologies
- Flask
- Flask-Login
- Google OAuth2
- Flask-SQLAlchemy
- Werkzeug Security
- HTML/CSS
- Bootstrap

# Installation
- Clone the repository: "git clone https://github.com/OsimFavour/pathfinder.com"
- Install dependencies: "pip install -r requirements.txt"
- Set up the database: "flask db upgrade"
- Start the server: "export FLASK_APP=main.py", "flask run"

# Usage
- Navigate to the login page and create an account or login using Flask-Login or Google-authentication.
- Once logged in, users gain access to inspiring blog posts on various topics or search for desired relevant topics specific to their needs at the moment.
- Users can also comment on each other's stories and subscribe to our newsletter to receive updates on our latest blog posts, and can also make downloads if they want.
