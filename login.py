import server

db = server.get_db()

def create_account(username, password):
    """
    Creates a new account
    :param username: username of individual
    :param password: password of individual
    :return: description of success of account creation
    """
    if (db.users.find({"username": username}).count() > 0):
        return "User already exists!"
    else:
        db.users.insert({"username": username, "password": password})
        return "Success! Your account has been created."

def open_account(username, password):
    """
    Opens a user's account
    :param username: username of individual
    :param password: password entered
    :return: description of success of logging in
    """
    if (db.users.find({"username": username})[0]["password"] != password):
        return "Invalid username/password."
    else:
		return "Success!"

#print(open_account("amanocha", "password"))