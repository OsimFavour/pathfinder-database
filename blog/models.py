from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blog import db, app
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Purpose Parent
    purpose_posts = relationship("PurposePost", back_populates="author")
    # Relationship Parent
    relationship_posts = relationship("RelationshipPost", back_populates="author")
    # Fiction Posts Parent
    fiction = relationship("Fiction", back_populates="author")
    # Newsletters Parent
    newsletters = relationship("Newsletter", back_populates="author")
    # Book Upload Parent
    books = relationship("Upload", back_populates="book_author")
    # Comments Parent
    comments = relationship("Comment", back_populates="comment_author") 

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"usser_id": self.id}).decode("utf-8")
    
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except: 
            return None
        return User.query.gett(user_id)
    
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.password}')"


class PurposePost(db.Model):
    __tablename__  = "purpose_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Users Child
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="purpose_posts")

    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Comments Parent
    comment_purpose = relationship("Comment", back_populates="purpose_parent_post")


class RelationshipPost(db.Model):
    __tablename__ = "relationship_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Users Child
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))    
    author = relationship("User", back_populates="relationship_posts")

    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Comment Parent
    comment_relationship = relationship("Comment", back_populates="relationship_parent_post")

     
class Fiction(db.Model):
    __tablename__ = "fiction_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Users Relationship
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="fiction")

    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Comments Relationship
    comment_fiction = relationship("Comment", back_populates="fiction_parent_post")


    def __repr__(self):
        return f"Post('{self.author}', '{self.title}', '{self.date}')"


     
class Newsletter(db.Model):
    __tablename__ = "newsletters"
    id = db.Column(db.Integer, primary_key=True)

    # Users Relationship
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="newsletters")

    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # comments = relationship("Comment", back_populates="parent_post")


    def __repr__(self):
        return f"Post('{self.author}', '{self.title}', '{self.date}')"
    

class Upload(db.Model):
    __tablename__  = "book_uploads"
    id = db.Column(db.Integer, primary_key=True)

    # Users Relationship
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_author = relationship("User", back_populates="books")

    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)

    # Users Child
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    # Purpose Posts Child
    purpose_post_id = db.Column(db.Integer, db.ForeignKey("purpose_posts.id"))
    purpose_parent_post = relationship("PurposePost", back_populates="comment_purpose")

    # Relationship Posts Child
    relationship_post_id = db.Column(db.Integer, db.ForeignKey("relationship_posts.id"))
    relationship_parent_post = relationship("RelationshipPost", back_populates="comment_relationship")

    # Fiction Posts Child
    fiction_id = db.Column(db.Integer, db.ForeignKey("fiction_posts.id"))
    fiction_parent_post = relationship("Fiction", back_populates="comment_fiction")
    
    # Comment Text
    text = db.Column(db.Text, nullable=False)


# db.drop_all()
db.create_all()