

class Note:
    def __init__(self, obs_timecode:str, note_text:str):
        self.timecode:str = obs_timecode
        self.text:str = note_text

    def note_info(self):
        print(f"{self.timecode}:{self.text}")



class RangeNote:
    def __init__(self):#note_text:str, obs_timecode_start:str|None = None,  obs_timecode_end:str|None = None
        self.range_note_id: int|None= None
        self.obs_timecode_start:str
        self.obs_timecode_end:str|None = None
        self.text:str|None = None


    def set_range_note_id(self, range_note_id:int):
        self.range_note_id = range_note_id

    def set_obs_time_start(self, obs_timecode_start:str):
        self.obs_timecode_start = obs_timecode_start

    def set_obs_time_end(self, obs_timecode_end:str):
        self.obs_timecode_end = obs_timecode_end

    def set_text(self, text:str):
        self.text = text

    def note_info(self):
        print(f"{self.obs_timecode_start}-{self.obs_timecode_end}:{self.text}")


class Session:
    def __init__(self, session_id:int, started_at:str, closed_at:str|None = None):
        self.session_id:int = session_id
        self.started_at:str = started_at
        self.closed_at:str = closed_at if closed_at is not None else None

    def session_info(self):
        if self.closed_at is None:
            print(f"[{self.session_id}] {self.started_at} - [EMPTY]")
        else:
            print(f"[{self.session_id}] {self.started_at} - {self.closed_at}")
