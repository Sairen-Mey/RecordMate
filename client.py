import obsws_python as obs
import obs_config


class OBSManager:
    def __init__(self):
        self.client: obs.ReqClient|None = None
        self.event_client: obs.EventClient|None = None
        # self.connected: bool = False



    def connect(self) -> bool:
        try:
            if self.event_client is not None:
                self.event_client.disconnect()

            if self.client is not None:
                self.client.disconnect()

            self.client = obs.ReqClient(
                host=obs_config.host,
                port=obs_config.port,
                password=obs_config.password,
                timeout=3
            )
            self.event_client = obs.EventClient(
                host=obs_config.host,
                port=obs_config.port,
                password=obs_config.password,
            )



            return True

        except Exception as err:
            self.client = None
            self.event_client = None
            print(f"OBS connection error: {err}")

            return False

    def get_record_status(self):
        if self.client is None:
            return None

        return self.client.send("GetRecordStatus", raw=True)

    def get_is_obs_active(self) -> bool:
        status = self.get_record_status()

        if status is None:
            return False

        return bool(status["outputActive"])

    # def is_obs_recording(self) -> bool:
    #     status = self.get_record_status()
    #
    #     if status is None:
    #         return False
    #
    #     return

    def get_output_timecode(self) -> str:
        status = self.get_record_status()
        return status["outputTimecode"]



obs_manager = OBSManager()
