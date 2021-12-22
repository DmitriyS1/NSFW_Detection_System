#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, inspect, Table, Column, Integer, String, MetaData)
from db.repositories import user_repository

# eng = create_engine('postgresql+psycopg2://back:aHR!##9887ASDsda@localhost:5444/hr_bot')
# insp = inspect(eng)

# with eng.connect() as  con:
#     rs = con.execute("SELECT VERSION()")
#     print(rs.fetchone())

#     meta = MetaData(eng)
#     users = Table('users', meta, 
#         Column('id', Integer, primary_key=True),
#         Column('first_name', String)
#     )

#     con.close()

# # Inspector functions

# t_names = insp.get_table_names()
# print("Table names: ", t_names)

# for n in t_names:
#     print(insp.get_columns(n))

d = user_repository.get(1)
print(d)