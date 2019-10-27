from dataclasses import dataclass
import yaml


@dataclass
class Configuration:
    current_version: str
    strategy: str
    tracked_files: list

    @staticmethod
    def parse(file):
        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)
        contents = contents or {}

        mandatory_fields = ["current_version", "strategy", "tracked_files"]
        for field in mandatory_fields:
            if contents.get(field) is None:
                raise ValueError(f"Configuration file is missing '{field}'")

        return Configuration(**contents)
