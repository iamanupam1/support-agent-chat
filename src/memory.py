class MemoryStore:
    def __init__(self):
        self.sessions = {}

    def get(self, session_id):
        return self.sessions.get(session_id, [])

    def add(self, session_id, user, assistant):
        self.sessions.setdefault(session_id, []).append({"role": "user", "content": user})
        self.sessions[session_id].append({"role": "assistant", "content": assistant})

memory = MemoryStore()
