from typing import Any
from dataclasses import dataclass


@dataclass
class SetupConfig:
    current_log_line: int
    current_task: str
    log_file_name: str

    @staticmethod
    def from_dict(objs: Any) -> list['SetupConfig']:
        result = []
        for obj in objs:
            _current_log_line = int(obj.get("current_log_line"))
            _current_task = str(obj.get("current_task"))
            _log_file_name = obj.get("log_file_name")
            result.append(SetupConfig(_current_log_line,
                          _current_task, _log_file_name))
        return result

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
