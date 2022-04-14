import db_config

conf = db_config.postgre_config()
print(conf.dbname)
print(conf.host)
print(conf.port)
print(conf.user)
