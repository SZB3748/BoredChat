from dataclasses import dataclass

@dataclass(slots=True)
class Message:
    "I wonder what this could be???"

    sender_id:int
    sender_name:str
    content:str

class Connection:
    "A connection. :O (no way)"

    def __init__(self, id:int, queue:list=[]):
        self.id = id
        self.queue = queue or []

    def enqueue_msg(self, msg:Message):
        self.queue.append(msg)

    def dequeue_msg(self)->Message|None:
        return self.queue.pop(0) if self.queue else None