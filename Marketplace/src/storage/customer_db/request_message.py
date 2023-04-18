from collections import defaultdict

class request_message:
    def __init__(self,sender_id,request_id,local_seq_no,request,metadata,type) -> None:
        self.request_id = request_id
        self.sender_id = sender_id
        self.local_seq_no = local_seq_no
        self.request = request
        self.metadata = metadata 
        self.type = type