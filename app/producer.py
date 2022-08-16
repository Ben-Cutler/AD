import random

class Producer:
    def __init__(self, max_to_send) -> None:
        self.max_to_send = max_to_send

    def messages(self):
        sent = 0
        while sent < self.max_to_send:
            yield {
                'msg_txt': chr(random.randrange(ord(' '), 127)) * 100,
                'phone_num': random.randrange(0, 10000000000)
            }
            sent = sent +1