import db_config
import os

conf = db_config.postgre_config()
conf.set_os_environ()

print(os.environ.get("POSTGRE_HOST"))
print(os.environ.get("POSTGRE_PORT"))
print(os.environ.get("POSTGRE_USER"))
print(os.environ.get("POSTGRE_NAME"))
