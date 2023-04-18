from collections import defaultdict


class sequence_message:
    def __init__(self,request_id,global_seq_no,metadata) -> None:
        self.global_seq_no = global_seq_no
        self.request_id = request_id
        self.metadata = metadata