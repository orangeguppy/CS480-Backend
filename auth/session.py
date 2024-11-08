import uuid

def generate_new_session_id():
    session_id = str(uuid.uuid4())
    return session_id