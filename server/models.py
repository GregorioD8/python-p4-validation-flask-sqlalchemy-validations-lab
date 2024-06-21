from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
# Initialize the database
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    # Define the columns for the Author model
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    
    # Add validators 
    # Validate the 'name' field
    @validates('name')
    def validate_name(self, key, name):
        
        # Ensure the name is not empty
        if not name:
            raise ValueError('Name field is required.')
        
        # Ensure the name is unique
        author = db.session.query(Author.id).filter_by(name=name).first()
        if author is not None:
            raise ValueError('Name must be unique.')
        return name
     
    # Validate the 'phone_number' field
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        
        # Ensure teh phone number is exactly 10 digits long
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be 10 digits.')
        return phone_number
    

class Post(db.Model):
    __tablename__ = 'posts'
    
    # Define the columns for the Post model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    # Validate the 'title' field
    @validates('title')
    def validate_title(self, key, title):
        # Ensure the title is not empty 
        if not title:
            raise ValueError('Title field is required.')
        # Ensure the title contains one of the clickbait phrases
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title
    

    # Validate teh 'content' and 'summary' fields
    @validates('content', 'summary')
    def validate_length(self, key, string):
        # Ensure content is at least 250 characters long
        if key == 'content':
            if len(string) < 250:
                raise ValueError('Post content must be greater than or equal to 250 characters long.')
        # Ensure summary is no more than 250 characters long
        if key == 'summary':
            if len(string) > 250:
                raise ValueError('Post summary must be greater than or equal to 250 characters long')
        return string
    
    @validates('category')
    def validate_category(self, key, category):
        # Ensure category is either 'Fiction' or 'Non-Fiction'
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be Fiction not Non-Fiction.')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
