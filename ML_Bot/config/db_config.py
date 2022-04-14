from dataclasses import dataclass
import yaml


@dataclass
class postgre_config:
    def __init__(self):
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)["database"]
            self.dbname = cfg["db-name"]
            self.host = cfg["host"]
            self.port = cfg["port"]
            self.user = cfg["user"]
            self.password = cfg["password"]
        
        return self

    host: str
    port: int
    user: str
    password: str
    dbname: str

