from datetime import datetime


class Utils:
    @staticmethod
    def get_current_time_millis():
        return int(datetime.now().timestamp() * 1000)
