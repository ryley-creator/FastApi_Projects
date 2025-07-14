from datetime import datetime,timezone
from sqlalchemy import JSON, TIMESTAMP, Column, MetaData,Integer,String, Table,ForeignKey

metadata = MetaData()

roles = Table(
    'roles',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String(45),nullable=False),
    Column('permissions',JSON)
)

users = Table(
    'users',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('email',String,nullable=False),
    Column('username',String,nullable=False),
    Column('password',String,nullable=False),
    Column('registered_at',TIMESTAMP,default=datetime.now()),
    Column('role_id',Integer,ForeignKey('roles.id'))

)