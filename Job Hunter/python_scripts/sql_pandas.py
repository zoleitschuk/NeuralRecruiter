
# coding: utf-8

# In[1]:

def append_df_to_sql(df_to_append, sqlite_file, table_name):
    
    from sqlalchemy import create_engine
    
    # Create your connection.
    engine = create_engine('sqlite:///' + sqlite_file)
    df_to_append.to_sql(name=table_name, con=engine, if_exists='append', index=False)


# In[2]:

def replace_db_with_df(df_to_append, sqlite_file, table_name):
    
    from sqlalchemy import create_engine
    
    # Create your connection.
    engine = create_engine('sqlite:///' + sqlite_file)
    df_to_append.to_sql(name=table_name, con=engine, if_exists='replace', index=False)


# In[3]:

def df_from_sql(sqlite_file, table_name):
    import pandas as pd
    from sqlalchemy import create_engine
    
    # Create your connection.
    engine = create_engine('sqlite:///' + sqlite_file)
    
    return pd.read_sql_table(table_name=table_name, con=engine)


# In[ ]:

if __name__ == "__main__":
    # Execute main content.
    print("You are trying to run sql_pandas.py on its own. sql_pandas.py is not currently set up to work this way.")

