from firebase_admin import credentials, db
import firebase_admin
import numpy as np
from utils import load_yaml


config_file_path = load_yaml("configs/database.yaml")


def get_face_embeddings_db():
    """
    Fetches all student face embeddings from Firebase Realtime Database.

    Returns:
        dict: Dictionary with student names as keys and their embeddings as numpy arrays
    """
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
            firebase_admin.initialize_app(cred, {
                "databaseURL": config_file_path["firebase"]["databaseURL"]
            })

        # Get reference to Students node
        students_ref = db.reference("Students")
        all_students = students_ref.get()

        # If no students found
        if not all_students:
            print("No students found in the database.")
            return {}

        # Create a dictionary of embeddings
        database = {}
        for student_key, student_info in all_students.items():
            name = student_info.get("name")
            embedding = np.array(student_info.get("embedding", []), dtype=np.float32)
            database[name] = embedding

        print(f"✅ Successfully loaded {len(database)} embeddings from the database.")
        return database

    except Exception as e:
        print(f"❌ Error loading face embeddings from Firebase: {str(e)}")
        return {}

    
def add_student(student_id, name, embedding):
    """
    Adds a new student to Firebase Realtime Database
    
    Args:
        student_id (str): Unique ID for the student (e.g., "Student_3")
        name (str): Student's name
        embedding (list): Face embedding vector
    """
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
            firebase_admin.initialize_app(cred, {
                "databaseURL": config_file_path["firebase"]["databaseURL"]
            })
        
        # Get reference to Students node
        students_ref = db.reference("Students")

        # Convert embedding to list if it's a numpy array
        embedding_list = embedding.tolist()

        # Create student data dictionary
        student_data = {
            "name": name,
            "embedding": embedding_list  # Store as native list
        }
        
        # Add the student to Firebase
        students_ref.child(student_id).set(student_data)
        
        print(f"✅ Successfully added student: {name} (ID: {student_id})")
        return True
        
    except Exception as e:
        print(f"❌ Error adding student: {str(e)}")
        return False
    

def remove_student(student_id):
    """
    Removes a student from Firebase Realtime Database
    
    Args:
        student_id (str): ID of the student to remove (e.g., "Student_3")
    
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
            firebase_admin.initialize_app(cred, {
                "databaseURL":  config_file_path["firebase"]["databaseURL"]
            })
        
        # Get reference to the specific student
        student_ref = db.reference(f"Students/{student_id}")
        
        # Check if student exists
        if not student_ref.get():
            print(f"❌ Student {student_id} not found")
            return False
        
        # Remove the student
        student_ref.delete()
        
        print(f"✅ Successfully removed student: {student_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error removing student: {str(e)}")
        return False


def replace_embedding(student_id, new_embedding):
    """
    Replaces a student's face embedding in Firebase
    
    Args:
        student_id (str): ID of the student (e.g., "Student_1")
        new_embedding (list): New face embedding vector
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
            firebase_admin.initialize_app(cred, {
                "databaseURL":  config_file_path["firebase"]["databaseURL"]
            })

        # Convert embedding to list if it's a numpy array
        embedding_list = new_embedding.tolist() 
        
        # Get reference to the student
        student_ref = db.reference(f"Students/{student_id}")
        
        # Check if student exists
        if not student_ref.get():
            print(f"❌ Student {student_id} not found")
            return False
        
        # Update the embedding (store as native list)
        student_ref.update({
            "embedding": embedding_list
        })
        
        print(f"✅ Successfully updated embedding for student: {student_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating embedding: {str(e)}")
        return False