from dataclasses import dataclass
import os
import yaml


@dataclass
class postgre_config:
    def __init__(self):
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, yaml.BaseLoader)["DATABASE"]
            self.dbname = cfg["POSTGRE_NAME"]
            self.host = cfg["POSTGRE_HOST"]
            self.port = cfg["POSTGRE_PORT"]
            self.user = cfg["POSTGRE_USER"]
            self.password = cfg["POSTGRE_PASSWORD"]
        
    def set_os_environ(self):
        os.environ["POSTGRE_HOST"] = self.host
        os.environ["POSTGRE_PORT"] = self.port
        os.environ["POSTGRE_USER"] = self.user
        os.environ["POSTGRE_PASSWORD"] = self.password
        os.environ["POSTGRE_NAME"] = self.dbname

    host: str
    port: int
    user: str
    password: str
    dbname: str

