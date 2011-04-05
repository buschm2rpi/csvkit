#!/usr/bin/env python

import datetime

from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Time
from sqlalchemy.schema import CreateTable

DIALECTS = {
    'mssql': 'mssql.pyodbc',
    'mysql': 'mysql.mysqlconnector',
    'oracle': 'oracle.cx_oracle',
    'postgresql': 'postgresql.psycopg2',
    'sqlite': 'sqlite.pysqlite'
}

def make_column(column_name, normal_type, normal_column):
    column_kwargs = {'nullable': False}
    type_kwargs = {}

    if normal_type == bool:
        column_type = Boolean  
    elif normal_type == int:
        column_type = Integer
    elif normal_type == float:
        column_type = Float
    elif normal_type == datetime.datetime:
        column_type = DateTime
    elif normal_type == datetime.date:
        column_type = Date
    elif normal_type == datetime.time:
        column_type = Time
    elif normal_type == None:
        column_type = String
        type_kwargs['length'] = 32
    elif normal_type == str:
        column_type = String
        type_kwargs['length'] = max([len(d) if d else 0 for d in normal_column])
    else:
        raise ValueError('Unexpected normalized column type: %s' % normal_type)

    for d in normal_column:
        if d == None:
            column_kwargs['nullable'] = True
            break

    column = Column(column_name, column_type(**type_kwargs), **column_kwargs)

    return column

def make_create_table(column_names, normal_types, normal_columns, dialect=None):
    metadata = MetaData()
    table = Table('csvsql', metadata)

    for i in range(len(column_names)):
        c = make_column(column_names[i], normal_types[i], normal_columns[i])
        table.append_column(c)

    if dialect:
        module = __import__('sqlalchemy.dialects.%s' % DIALECTS[dialect], fromlist=['dialect'])
        dialect = module.dialect() 

    return CreateTable(table).compile(dialect=dialect)