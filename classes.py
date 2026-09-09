




class Note:
    def __init__(self, obs_timestamp:str, note_text:str):
        self.timestamp:str = obs_timestamp
        self.text:str = note_text

    def note_info(self):
        print(f"{self.timestamp}:{self.text}")



class RangeNote:
    def __init__(self):#note_text:str, obs_timestamp_start:str|None = None,  obs_timestamp_end:str|None = None
        self.obs_timestamp_start:str|None = None
        self.obs_timestamp_end:str|None = None
        self.note_text:str = "empty"

    def set_obs_time_start(self, obs_timestamp_start:str):
        self.obs_timestamp_start = obs_timestamp_start

    def set_obs_time_end(self, obs_timestamp_end:str):
        self.obs_timestamp_end = obs_timestamp_end

    def note_info(self):
        print(f"{self.obs_timestamp_start}-{self.obs_timestamp_end}:{self.note_text}")