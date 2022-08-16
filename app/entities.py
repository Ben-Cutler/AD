from dataclasses import dataclass

@dataclass
class Alert:
    queue_id: str
    n_msgs: int
    fail_rate: float
    num_senders: int
    poll_rate: int