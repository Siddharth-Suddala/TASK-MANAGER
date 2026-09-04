class User:
    def __init__(self, id, username,email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role


    def get_dictionary(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }