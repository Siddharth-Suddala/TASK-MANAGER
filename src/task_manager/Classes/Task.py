class Task:
    def __init__(self, id, title, description, user_id, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_at = created_at

    def get_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }
