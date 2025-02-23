import base64
import bcrypt
from sqlalchemy import select, insert, and_, or_

from . import log_config
from . import db_config
from . import models

logger = log_config.logger
log_error = log_config.log_error

Session = db_config.Session

User = models.User
UserRelationship = models.UserRelationship
Chat = models.Chat
Message = models.Message
Theme = models.Theme

# sort ids before passing them into a function that relies on the ids being in order
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

    a1 = ''.join(a1)
    n1 = ''.join(n1)
    a2 = ''.join(a2)
    n2 = ''.join(n2)

    x = f"{a1}{n1}"
    y = f"{a2}{n2}"

    if x > y:
        return id_1, id_2
    return id_2, id_1

# --- DATABASE FUNCTIONS ---

def setup():
    with Session() as s:
        check = s.query(User).filter(User.email == "admin@chatify.com").one_or_none()
        if not check:
            pw = enc_pw('Password123#')
            admin = User("admin@chatify.com", "Chatify Admin", pw, "Admin")

            s.add(admin)
            s.commit()

        print("database setup complete")

def populate(): # ! remove before build
    with Session() as s:
        pw = enc_pw("Password132#")
        users = [User("user1@domain.com", "User 1", pw), User("user2@domain.com", "User 2", pw)]
        
        for u in users:
            s.add(u)
        s.commit()

    with Session() as s:
        u1 = s.query(User).filter(User.email == "user1@domain.com").one_or_none()
        u2 = s.query(User).filter(User.email == "user2@domain.com").one_or_none()
        ur = UserRelationship(u1.id, u2.id, 0)

        s.add(ur)
        s.commit()

    with Session() as s:
        a = s.query(User).filter(User.email == "admin@chatify.com").one_or_none()
        u1 = s.query(User).filter(User.email == "user1@domain.com").one_or_none()
        u2 = s.query(User).filter(User.email == "user2@domain.com").one_or_none()
        chat = Chat(a.id, u1.id)
        chat = Chat(u1.id, u2.id)

        s.add(chat)
        s.commit()

    print("populated db tables")


# -- USERS --

# - AUTH -

def user_exists(email):
    with Session() as s:
        user = s.query(User).filter(User.email == email).one_or_none()

    return user

def enc_pw(pw):
    s = bcrypt.gensalt(10)
    b = pw.encode('utf-8')

    return bcrypt.hashpw(b, s)

def check_pw(email, pw):
    with Session() as s:
        b = pw.encode('utf-8')
        user_pw = s.query(User.password).filter(User.email == email).one_or_none()[0]
    return bcrypt.checkpw(b, user_pw)

def get_session_data(email):
    with Session() as s:
        try:
            user = s.query(User).filter(User.email == email).one_or_none()

            if user:
                return {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role
                }
            raise ValueError("User does not exist")
        except Exception as e:
            log_error(f"Error getting session data for {email}", e)

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
            log_error(f"Error creating user {username}", e)

            return False

def get_user(*kwargs):
    id = kwargs.get('id', None)
    email = kwargs.get('email', None)

    with Session() as s:
        if id:
            user = s.query(User).filter(User.id == id).one_or_none()
        else:
            user = s.query(User).filter(User.email == email).one_or_none()

    return user

def get_user_data_safe(id):
    with Session() as s:
        try:
            user = s.query(User).filter(User.id == id).one_or_none()

            if user:
                data = {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                    'pfp': base64.b64encode(user.pfp).decode('utf-8'),
                    'status': user.status
                }

                return data
            raise ValueError("User does not exist")
        except Exception as e:
            error = log_error(f"Error getting safe user data for {id}", e)

            return error

def update_user(id, updates):
    with Session() as s:
        try:
            user = s.query(User).filter(User.id == id).one_or_none()

            if user:
                for c, v in updates.items():
                    setattr(user, c, v)

                s.commit()

                return True
            raise ValueError("User does not exist")
        except Exception as e:
            log_error(f"Error updating user {id}", e)

            return False

def delete_user(id, pw):
    with Session() as s:
        try:
            user = s.query(User).filter(User.id == id).one_or_none()

            if user:
                s.delete(user)
                s.commit()

                return True
            raise ValueError("User does not exist")
        except Exception as e:
            log_error(f"Error deleting user {id}", e)

# -- USER RELATIONSHIPS --

def create_user_relationship(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            user1 = s.query(User).filter(User.id == id_1).one_or_none()
            user2 = s.query(User).filter(User.id == id_2).one_or_none()

            if user1 and user2:
                ur = UserRelationship(id_1, id_2, 1)

                s.add(ur)
                s.commit()

                return True
            raise Exception("One or both users do not exist")
        except Exception as e:
            log_error(f"Error creating user relationship {id_1} to {id_2}", e)

            return False

def get_user_relationship(id_1, id_2=None):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            if id_2:
                id = f"ur/{id_1}/{id_2}"
                ur = s.query(UserRelationship).filter(UserRelationship.id == id).one_or_none()

                if ur:
                    return ur
                raise ValueError(f"User relationship does not exist between {id_1} and {id_2}")
            urs = s.query(UserRelationship).filter(or_(UserRelationship.id_1 == id_1, UserRelationship.id_2 == id_1)).all()

            return urs
        except Exception as e:
            log_error(f"Error getting user relationship/s for {id_1}", e)

            return False

def update_user_relationship(id_1, id_2, status):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            id = f"ur/{id_1}/{id_2}"
            ur = s.query(UserRelationship).filter(UserRelationship.id == id).one_or_none()

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
            log_error(f"Error updating user relationship between {id_1} and {id_2}", e)

            return False

# -- CHATS --

# - CRUD -

def create_chat(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            user1 = s.query(User).filter(User.id == id_1).one_or_none()
            user2 = s.query(User).filter(User.id == id_2).one_or_none()

            if user1 and user2:
                chat = Chat(id_1, id_2)

                s.add(chat)
                s.commit()

                return True
            raise ValueError("One or both users do not exist")
        except Exception as e:
            log_error(f"Error creating chat between {id_1} and {id_2}", e)

            return False

def get_chat_data(id_1, chat_id=None):
    with Session() as s:
        try:
            if chat_id:
                _, a, b = chat_id.split('/')

                friend = s.query(User).filter(User.id == a).one_or_none()
                if friend.id == id_1:
                    friend = s.query(User).filter(User.id == b).one_or_none()

                id_1, id_2 = sort_ids(a, b)

                chat = s.query(Chat).filter(Chat.id == chat_id).one_or_none()
                messages = s.query(Message).filter(Message.chat == chat_id).all()

                if chat:
                    message_data = []

                    for i, j in enumerate(messages):
                        message = {
                            'id': j.id,
                            'senderId': j.sender_id,
                            'senderUsername': j.sender_username,
                            'chat': j.chat,
                            'content': j.content,
                            'timestamp': j.timestamp
                        }
                        message_data.append(message)

                    data = {
                        'id': chat.id,
                        'id_1': chat.id_1,
                        'id_2': chat.id_2,
                        'username': friend.username,
                        'status': friend.status if friend.status else '',
                        'pfp': base64.b64encode(friend.pfp).decode('utf-8'),
                        'messages': message_data if message_data else 'No messages yet'
                    }
                    # print(f"\ndata: {data} \n")

                    return data
                raise ValueError(f"Chat does not exist between {id_1} and {id_2}")

            chats = s.query(Chat).filter(or_(Chat.id_1 == id_1, Chat.id_2 == id_1)).all()
            data = {}

            for i, j in enumerate(chats):
                user = s.query(User).filter(User.id == j.id_1).one_or_none()

                if user.id == id_1: # depending on how the ids were sorted when the chat was created, user's id could be id_1 or id_2
                    user = s.query(User).filter(User.id == j.id_2).one_or_none() # this prevents the code trying to return a chat between user x and user x

                last_message = s.query(Message).filter(Message.chat == j.id).order_by(Message.timestamp.desc()).first()

                if last_message:
                    last_message = {
                        'senderId': last_message.sender_id,
                        'content': last_message.content
                    }

                if user:
                    data[i] = {
                        'id': j.id,
                        'id_1': j.id_1,
                        'id_2': j.id_2,
                        'pfp': base64.b64encode(user.pfp).decode('utf-8'),
                        'username': user.username,
                        'status': user.status if user.status else '',
                        'lastMessage': last_message
                    }

                    return data
                else:
                    raise ValueError(f"User with id {id_1} OR {id_2} does not exist")
        except Exception as e:
            log_error(f"Error getting chat/s for {id_1}", e)

            return False

def update_chat(id_1, chat_id, update):
    with Session() as s:
        try:
            chat = s.query(Chat).filter(Chat.id == chat_id).one_or_none()
            print("\n", id_1, chat_id, chat, update, "\n")
            print(f"\n update: {update} \n")

            match update['option']:
                case "send":
                    msg = Message(update['sender_id'], update['sender_username'], chat_id, update['data'], update['timestamp'])
                    s.add(msg)
                case "edit":
                    msg = s.query(Message).filter(and_(Message.chat == chat_id, Message.sender == id_1)).first()
                    setattr(msg, Message.content, update['data'])
                case "delete":
                    msg = s.query(Message).filter(and_(Message.chat == chat_id, Message.sender == id_1)).first()
                    s.delete(msg)
                case default:
                    raise ValueError(f"Invalid update option: {update['option']}")

            s.commit()
        except Exception as e:
            log_error(f"Error updating messages for {chat_id}: {update}", e)

            return False

def delete_chat(id_1, id_2):
    id_1, id_2 = sort_ids(id_1, id_2)

    with Session() as s:
        try:
            id = f"ch/{id_1}/{id_2}"
            chat = s.query(Chat).filter(Chat.id == id).one_or_none()

            if chat:
                s.delete(chat)
                s.commit()

                return True
            raise ValueError(f"Chat does not exist between {id_1} and {id_2}")
        except Exception as e:
            log_error(f"Error deleting chat for {id_1}", e)

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
            log_error(f"Error creating theme {name}", e)

            return False

def get_theme(id):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(Theme.id == id).one_or_none()

            if theme:
                return theme
            raise ValueError(f"Theme {id} does not exist")
        except Exception as e:
            log_error(f"Error getting theme {id}", e)

            return False

def update_theme(id, updates):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(Theme.id == id).one_or_none()

            if theme:
                for c, v in updates.items():
                    setattr(theme, c, v)

                s.commit()

                return True
            raise ValueError("Theme does not exist")
        except Exception as e:
            log_error(f"Error updating theme {id}", e)

            return False

def delete_theme(id):
    with Session() as s:
        try:
            theme = s.query(Theme).filter(Theme.id == id).one_or_none()

            if theme:
                s.delete(theme)
                s.commit()

                return True
            raise ValueError("Theme does not exist")
        except Exception as e:
            log_error(f"Error deleting theme {id}", e)

            return False