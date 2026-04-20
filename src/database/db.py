from src.database.config import supabase
import bcrypt

# Teacher Login Functions

def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashedPassword):
    return bcrypt.checkpw(password.encode(), hashedPassword.encode())


def check_teacher_exists(username):
    # Check if username already exists
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()

    if response.data:
        teacher = response.data[0]

        if check_password(password, teacher["password"]):
            return teacher

    return None


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data


def create_student(student_name, face_embedding=None, voice_embedding=None):
    data = {'name': student_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

