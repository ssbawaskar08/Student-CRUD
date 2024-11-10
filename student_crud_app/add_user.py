from app import app, db, User
from werkzeug.security import generate_password_hash

# Create the app context
with app.app_context():
    # Sample user details
    username = 'testuser'
    password = '12345678'  # Change this to the desired password
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    
    # Create a new user object
    new_user = User(username=username, password_hash=hashed_password)
    
    # Add the user to the database session
    db.session.add(new_user)
    
    # Commit the session to save the user in the database
    db.session.commit()

    print(f"User '{username}' added successfully with hashed password!")
