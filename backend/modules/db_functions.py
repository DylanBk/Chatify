import bcrypt
from sqlalchemy import select, insert, and_

from . import log_config
from . import db_config
from . import models

logger = log_config.logger
log_error = log_config.log_error

Session = db_config.Session

User = models.User
UserRelationship = models.UserRelationship
Chat = models.Chat
Theme = models.Theme


def sort_ids(id_1, id_2):
    a1 = []
    n1 = []
    a2 = []
    n2 = []

    for i, j in zip(id_1, id_2):
        if i.isnumeric():
            n1.append(i)
        elif i.isalpha():
            a1.append(i)
        if j.isnumeric():
            n2.append(j)
        else:
            a2.append(j)

    a1.sort(), n1.sort()
    a2.sort(), n2.sort()

    x = f"{a1}{n1}"
    y = f"{a2}{n2}"

    if x > y:
        return x, y
    return y, x


# --- DATABASE FUNCTIONS ---

def setup():
    with Session() as s:
        if not s.query(User).filter(and_(User.email == "admin@chatify.com")).first():
            admin = User("Chatify Admin", "admin@chatify.com", "Password123#", "Password123#")
            s.add(admin)
            s.commit()

            print("db setup completed")


# -- USERS --

# - AUTH -

def user_exists(email):
    with Session() as s:
        user = s.query(User).filter(and_(User.email == email)).one_or_none()

    return user

def enc_pw(pw):
    s = bcrypt.gensalt(10)
    b = pw.encode('utf-8')

    return bcrypt.hashpw(b, s)

def check_pw(email, pw):
    with Session() as s:
        b = pw.encode('utf-8')
        user_pw = s.query(User.password).filter(and_(User.email == email)).one_or_none()[0]
    return bcrypt.checkpw(b, user_pw)

def get_session_data(email):
    with Session() as s:
        try:
            user = s.query(User).filter(and_(User.email == email)).one_or_none()

            if user:
                return {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role
                }
            raise ValueError("User does not exist")
        except Exception as e:
            logger.error(f"Error getting session data for {email}: {e}")

            return False

# - CRUD -

def create_user(username, email, pw):
    pw = enc_pw(pw)
    user = User(email, username, pw)

    with Session() as s:
        try:
            s.add(user)
            s.commit()

            return True
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}", exc_info=True)

            return False

def get_user(*kwargs):
    id = kwargs.get('id', None)
    email = kwargs.get('email', None)

    with Session() as s:
        if id:
            user = s.query(User).filter(and_(User.id == id)).one_or_none()
        else:
            user = s.query(User).filter(and_(User.email == email)).one_or_none()

    return user

def update_user(id, updates):
    with Session() as s:
        try:
            user = s.query(User).filter(and_(User.id == id))

            if user:

                for c, v in updates.items():
                    setattr(user, c, v)

                s.commit()

                return True
            raise ValueError("User does not exist")
        except Exception as e:
            logger.error(f"Error updating user {id}: {e}")

            return False

def delete_user(id, pw):
    with Session() as s:
        try:
            user = s.query(User).filter(and_(User.id == id)).one_or_none()

            if user:
                s.delete(user)
                s.commit()

                return True
            raise ValueError("User does not exist")
        except Exception as e:
            logger.error(f"Error deleting user {id}: {e}")


# -- USER RELATIONSHIPS --

def create_user_relationship(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            user1 = s.query(User).filter(and_(User.id == id_1)).one_or_none()
            user2 = s.query(User).filter(and_(User.id == id_2)).one_or_none()

            if user1 and user2:
                ur = UserRelationship(id_1, id_2, 1)

                s.add(ur)
                s.commit()

                return True
            raise Exception("One or both users do not exist")
        except Exception as e:
            logger.error(f"Error creating user relationship {id_1} to {id_2}: {e}")

            return False

def get_user_relationship(id_1, id_2=None):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            if id_2:
                id = f"ur/{id_1}/{id_2}"
                ur = s.query(UserRelationship).filter(and_(UserRelationship.id == id)).one_or_none()

                if ur:
                    return ur
                raise ValueError(f"User relationship does not exist between {id_1} and {id_2}")
            urs = s.query(UserRelationship).filter(and_(UserRelationship.id_1 == id_1)).all()

            return urs
        except Exception as e:
            logger.error(f"Error getting user relationship/s for {id_1}: {e}")

            return False

def update_user_relationship(id_1, id_2, status):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            id = f"ur/{id_1}/{id_2}"
            ur = s.query(UserRelationship).filter(and_(UserRelationship.id == id)).one_or_none()

            if ur:
                if ur.status != status:
                    if status == 6:
                        s.delete(ur)
                        s.commit()

                        return True
                    ur.status = status
                    s.commit()

                    return True
                raise ValueError("User relationship status is already set to that value")
            raise ValueError(f"User relationship does not exist between {id_1} and {id_2}")
        except Exception as e:
            logger.error(f"Error updating user relationship between {id_1} and {id_2}: {e}")

            return False


# -- CHATS --

# - CRUD -

def create_chat(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            user1 = s.query(User).filter(and_(User.id == id_1)).one_or_none()
            user2 = s.query(User).filter(and_(User.id == id_2)).one_or_none()

            if user1 and user2:
                chat = Chat(id_1, id_2)

                s.add(chat)
                s.commit()

                return True
            raise ValueError("One or both users do not exist")
        except Exception as e:
            logger.error(f"Error creating chat between {id_1} and {id_2}: {e}")

            return False

def get_chat(id_1, id_2=None):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            if id_2:
                id = f"ch/{id_1}/{id_2}"
                chat = s.query(Chat).filter(and_(Chat.id == id)).one_or_none()

                if chat:
                    return chat
                raise ValueError(f"Chat does not exist between {id_1} and {id_2}")
            chats = s.query(Chat).filter(and_(Chat.id_1 == id_1)).all()

            return chats
        except Exception as e:
            logger.error(f"Error getting chat/s for {id_1}: {e}")

            return False

def update_chat(id_1, id_2, update):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            id = f"ch/{id_1}/{id_2}"
            chat = s.query(Chat).filter(and_(Chat.id == id)).one_or_none()

            if chat:
                match update.option:
                    case "message":
                        chat.messages.append(update.data)
                    case "edit":
                        chat.messages[-1] = update.data
                    case "delete":
                        chat.messages[-1] = None
                    case default:
                        raise ValueError(f"Invalid update option: {update.option}")
                return chat.messages
            raise ValueError(f"Chat does not exist between {id_1} and {id_2}")
        except Exception as e:
            logger.error(f"Error updating message for {id_1}: {e}")

            return False

def delete_chat(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            id = f"ch/{id_1}/{id_2}"
            chat = s.query(Chat).filter(and_(Chat.id == id)).one_or_none()

            if chat:
                s.delete(chat)
                s.commit()

                return True
            raise ValueError(f"Chat does not exist between {id_1} and {id_2}")
        except Exception as e:
            logger.error(f"Error deleting chat for {id_1}: {e}")

            return False


# -- THEMES --

# - CRUD -

def create_theme(name, colours):
    bg, fg, primary, secondary, danger = colours.items()

    with Session() as s:
        try:
            theme = Theme(name, bg, fg, primary, secondary, danger)

            s.add(theme)
            s.commit()

            return True
        except Exception as e:
            logger.error(f"Error creating theme {name}: {e}")

            return False

def get_theme(id):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(and_(Theme.id == id)).one_or_none()

            if theme:
                return theme
            raise ValueError(f"Theme {id} does not exist")
        except Exception as e:
            logger.error(f"Error getting theme {id}: {e}")

            return False

def update_theme(id, updates):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(and_(Theme.id == id)).one_or_none()

            if theme:
                for c, v in updates.items():
                    setattr(theme, c, v)

                s.commit()

                return True
            raise ValueError("Theme does not exist")
        except Exception as e:
            logger.error(f"Error updating theme {id}: {e}")

            return False

def delete_theme(id):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(and_(Theme.id == id)).one_or_none()

            if theme:
                s.delete(theme)
                s.commit()

                return True
            raise ValueError("Theme does not exist")
        except Exception as e:
            logger.error(f"Error deleting theme {id}: {e}")

            return False