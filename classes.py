



class Note:
    def __init__(self, obs_timestamp:str, note_text:str):
        self.timestamp:str = obs_timestamp
        self.text:str = note_text

    def note_info(self):
        print(f"{self.timestamp}:{self.text}")
