
# coding: utf-8

# In[1]:

import pandas as pd

db_location = "data/job_hunter.db"
db_table_name = "job_desc_library"


# In[2]:

def feature_vect_from_text_matlab(script_location):
    
    import os
    from oct2py import octave
    
    cwd = os.getcwd()
    
    octave.addpath(cwd + script_location)
    features = octave.data_convert()
    
    return features


# In[3]:

def train_NN_matlab(script_location, X_train, y_train_i, y_train_sm):
    
    import os
    from oct2py import octave
    
    cwd = os.getcwd()
    
    octave.addpath(cwd + script_location)
    theta1_i, theta2_i, theta1_sm, theta2_sm = octave.main_NN(X_train, y_train_i, y_train_sm)
    
    return (theta1_i, theta2_i, theta1_sm, theta2_sm)


# In[6]:

def load_jobs_from_html(job_path):
    
    from bs4 import BeautifulSoup

    # Use Beautiful soup constructor to parse through the html and build a more organized data structure.    
    try:
        html = open(job_path, encoding="utf8")
    except:
        raise
    else:
        html = open(job_path)
    
    soup = BeautifulSoup(html.read(), 'html.parser')
    
    html_list = []
    
    for child in soup.children:
        if(child.name):
            html_list.append((str(child),child.get_text()))
    
    return pd.DataFrame(html_list, columns=['job_desc_html', 'job_desc_text'])


# In[7]:

def ndarray_to_str_list(feature_matrix):
    output_list = []
    
    for element in feature_matrix:
        dummy_str = ''
        for num in element:
            dummy_str = dummy_str + str(int(num))
        output_list.append(dummy_str)
    
    return output_list


# In[8]:

def str_list_to_ndarray(df_features):
    import numpy as np
    feature_matrix_list = []
    
    for i in df_features.index:
        feature_int_list = []
        
        for feature_str_element in list(df_features.loc[i, 'job_desc_word_occurance_feature_vector']):
            feature_int_list.append(int(feature_str_element))
        
        feature_matrix_list.append(np.array(feature_int_list))
        
    df_features['job_desc_word_occurance_feature_vector'] = feature_matrix_list


# In[10]:

def new_jobs_to_lib():
    file_path = input('Please enter the file path of the file containing'
                       ' the html you would like to add to the library.\n')
    import os
    cwd = os.getcwd()
        
    # Load new jobs from html file.
    new_jobs_df = load_jobs_from_html(file_path)
    
    rel_JSON_output_path = '\\matlab_scripts\\feature_vector\\new_job_desc.JSON'
    new_jobs_df['job_desc_text'].to_json(cwd + rel_JSON_output_path)
    
    script_location = '\\matlab_scripts\\feature_vector'
    feature_matrix = feature_vect_from_text_matlab(script_location)
    
    new_jobs_df['job_desc_word_occurance_feature_vector'] = ndarray_to_str_list(feature_matrix)
    new_jobs_df['user_interest_rating'] = 0
    new_jobs_df['user_skills_match_rating'] = 0
    new_jobs_df['predicted_interest_rating'] = 0
    new_jobs_df['predicted_skills_match_rating'] = 0
    new_jobs_df['interest_score'] = 0
    new_jobs_df['skills_match_score'] = 0
    new_jobs_df['overall_score'] = 0

    company = input('Please enter the company name for all job descriptions in file. If multiple companies hit the <enter> key to skip this step.')
    new_jobs_df['company'] = company
    
    import python_scripts.job_data as jd
    job_data_df = jd.get_job_data(new_jobs_df)
    new_jobs_df = pd.concat([new_jobs_df, job_data_df], axis=1)
    
    new_jobs_df['other_data'] = ''
    
    import python_scripts.sql_pandas as sql_pandas
    sqlite_file = db_location
    table_name = db_table_name
    sql_pandas.append_df_to_sql(new_jobs_df, sqlite_file, table_name)
    


# In[12]:

def permutate_dataframe(input_dataframe):
    import numpy as np
    
    return input_dataframe.reindex(np.random.permutation(input_dataframe.index))


# In[1]:

def manually_rate_jobs():
    number_to_rate = int(input('How many jobs would you like to rate?\n'))
    
    # Load data into dataframe from db
    import python_scripts.sql_pandas as sql_pandas
    sqlite_file = db_location
    table_name = db_table_name
    all_job_desc_df = sql_pandas.df_from_sql(sqlite_file, table_name)
    
    # Remove job_desc that have already been rated
    un_categorized_job_desc_df = all_job_desc_df[all_job_desc_df['user_interest_rating'] == 0]
    
    # Randomly select a subset of unrated job descriptions of size number_to_categorize
    job_desc_to_rate_df = permutate_dataframe(un_categorized_job_desc_df)[0 : number_to_rate]
    
    # For each job in subset have user rate based on level of interest and match to skills
    for i in job_desc_to_rate_df.index:
        
        print(all_job_desc_df.loc[i, 'job_desc_text'].encode(encoding='UTF-8',errors='ignore'))
        
        print('\n**********************************************************************')
        
        input_request_user_interest_rating = 'On a scale from 1 to 5, how interesting does this job sound?\n'
        all_job_desc_df.loc[i, 'user_interest_rating'] = int(input(input_request_user_interest_rating))
        
        input_request_user_skills_match_rating = 'On a scale from 1 to 5, how well does your skill set match the skills required for this position?\n'
        all_job_desc_df.loc[i, 'user_skills_match_rating'] = int(input(input_request_user_skills_match_rating))
        
        print('**********************************************************************\n')
    
    # Update the database with the new data.
    sqlite_file = db_location
    table_name = db_table_name
    sql_pandas.replace_db_with_df(all_job_desc_df, sqlite_file, table_name)    


# In[14]:

def manually_rank_jobs():
    # category_to_rank = prompt('What category would you like to rank?\n')
    print("Feature coming soon!")


# In[15]:

def get_predictions_matlab(script_location, X, Theta1, Theta2):
    
    import os
    from oct2py import octave
    
    cwd = os.getcwd()
    
    octave.addpath(cwd + script_location)
    predict_descrete, predict_continu = octave.predict(Theta1, Theta2, X)
    
    return (predict_descrete, predict_continu)


# In[16]:

def train_NN():
    print('Begining to train NN...')
    
    # Load data into dataframe from db
    import python_scripts.sql_pandas as sql_pandas
    sqlite_file = db_location
    table_name = db_table_name
    all_job_desc_df = sql_pandas.df_from_sql(sqlite_file, table_name)
    
    # Convert job_desc_word_occurance_feature_vector back to ndarray
    str_list_to_ndarray(all_job_desc_df)
    
    # Remove job_desc that have not been rated by the user and randomize the order
    all_rated_job_desc_df = permutate_dataframe(all_job_desc_df[all_job_desc_df['user_interest_rating'] != 0])
    
    # select a reasonable set of manually categorized jobs
    rows_in_df = len(all_rated_job_desc_df)
    if(rows_in_df <= 500):
        training_set_df = all_rated_job_desc_df
    else:
        training_set_df = all_rated_job_desc_df[0 : 500]
    
    # manipulate data into correct shape
    import numpy as np
    
    X = np.array(all_job_desc_df['job_desc_word_occurance_feature_vector'])
    X_training = np.array(training_set_df['job_desc_word_occurance_feature_vector'])
    y_training_i = np.array(training_set_df['user_interest_rating'])
    y_training_sm = np.array(training_set_df['user_skills_match_rating'])
    
    # pass data into NN and train
    script_location = '\\matlab_scripts\\categorization_NN'
    Theta1_i, Theta2_i, Theta1_sm, Theta2_sm = train_NN_matlab(script_location, X_training, y_training_i, y_training_sm)
    
    # run prediction on all jobs in db
    print('Training complete. Trained results will now be used to make predictions on all job descriptions in the library.\n')
    script_location = '\\matlab_scripts\\categorization_NN'
    predict_i, predict_i_continu = get_predictions_matlab(script_location, X, Theta1_i, Theta2_i)
    predict_sm, predict_sm_continu = get_predictions_matlab(script_location, X, Theta1_sm, Theta2_sm)
        
    # Update df with predictions
    all_job_desc_df['predicted_interest_rating'] = pd.DataFrame(predict_i)[0]
    all_job_desc_df['predicted_skills_match_rating'] = pd.DataFrame(predict_sm)[0]
    all_job_desc_df['interest_score'] = pd.DataFrame(predict_i_continu)[0]
    all_job_desc_df['skills_match_score'] = pd.DataFrame(predict_sm_continu)[0]
    
    # Update overall_score field.
    all_job_desc_df['overall_score'] = 2 * ((all_job_desc_df['interest_score']/5) * (all_job_desc_df['skills_match_score']/5)) / ((all_job_desc_df['interest_score']/5) + (all_job_desc_df['skills_match_score']/5))
    
    # Update the database with the new data.
    all_job_desc_df['job_desc_word_occurance_feature_vector'] = ndarray_to_str_list(all_job_desc_df['job_desc_word_occurance_feature_vector'])
    sqlite_file = db_location
    table_name = db_table_name
    sql_pandas.replace_db_with_df(all_job_desc_df, sqlite_file, table_name) 
    
    return all_job_desc_df


# In[20]:

def export_jobs():
    print('Export functionality coming soon!')
    


# In[21]:

def view_job_results():
    
    import python_scripts.custom_charts as custom_charts
    import python_scripts.sql_pandas as sql_pandas
    
    results_nav_message = ("\nResults Navigation. Actions available:\n"
                        "*************************************\n"
                        "Input Value:\t\tDescription:\n"
                        "--------------------------------------\n"
                        "a\t-\t View job chart.\n"
                        "b\t-\t Export jobs based on cutoff criteria.\n"
                        "back\t-\t Return to main navigation menu.\n"
                       )
    invalid_results_nav_message = ("\n"
                                "Sorry I did not understand. Please try again.\n"
                                "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"
                                "--------------------------------------------------"
                                )
    
    # Load data into dataframe from db
    sqlite_file = db_location
    table_name = db_table_name
    all_job_desc_df = sql_pandas.df_from_sql(sqlite_file, table_name)
    
    results_nav = ''
    
    while(results_nav != 'back'):
        
        print(results_nav_message)
        
        results_nav = input('What would you like to do?')
        
        # View job chart.
        if(results_nav == 'a'):
            
            x_header = 'skills_match_score'
            y_header = 'interest_score'
            color_by_header = 'company'
            labels_header = None
            output_path = "job_hunt_scatter.html"
            
            custom_charts.create_job_chart(all_job_desc_df, x_header, y_header, color_by_header, labels_header, output_path)
        
        # Export jobs based on cutoff criteria.
        elif(results_nav == 'b'):
            export_jobs()
        
        elif(results_nav =='back'):
            print('______________________________________________________')
        # User feedback for entering invalid text into input request.
        else:
            print(invalid_results_nav_message)


# In[22]:

def clear_all_ratings():
    
    # Load data into dataframe from db
    import python_scripts.sql_pandas as sql_pandas
    sqlite_file = db_location
    table_name = db_table_name
    all_job_desc_df = sql_pandas.df_from_sql(sqlite_file, table_name)
    
    all_job_desc_df['user_interest_rating'] = '0'
    all_job_desc_df['user_skills_match_rating'] = '0'
    
    # Update the database with the new data.
    sql_pandas.replace_db_with_df(all_job_desc_df, sqlite_file, table_name)
    


# In[23]:

def main_job_hunter():
    #*********************************************************************
    # Set up strings for text output to user during program navigation.
    #*********************************************************************
    welcome_message = ("=============================================\n"
                       "WELCOME!\n"
                       "============================================="
                       )
    
    farewell_message = ("=============================================\n"
                       "GOODBYE!\n"
                       "============================================="
                       )
    
    main_nav_message = ("\nMain Navigation. Actions available:\n"
                        "*************************************\n"
                        "Input Value:\t\tDescription:\n"
                        "--------------------------------------\n"
                        "1\t-\t Add new job descriptions to the library.\n"
                        "2\t-\t Manually rate job descriptions. This data is used to train NN, and\n"
                            "\t\tprovide accurate recomendations.\n"
                        "3\t-\t Navigate to the manual ranking menu. (Has no effect on NN training.)\n"
                        "4\t-\t Run neural network training algorithm to update recomendations.\n"
                        "5\t-\t Navigate to Export/View Results menu.\n"
                        "reset\t-\t Removes the user entered ratings for all job descriptions.\n"
                        "exit\t-\t Exits the program.\n"
                       )

    invalid_main_nav_message = ("\n"
                                "Sorry I did not understand. Returning you to main navigation.\n"
                                "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"
                                "--------------------------------------------------"
                                )
    
    #*********************************************************************
    # Functional content. Run program and request user for input.
    #*********************************************************************
    print(welcome_message)
    
    main_nav = ''
    while(main_nav != 'exit'):
        
        print(main_nav_message)
        
        main_nav = input('What action would you like to take?\n')
        
        if(main_nav == 'exit'):
            print(farewell_message)
        
        # Remove all user entered job ratings
        elif(main_nav == 'reset'):
            clear_all_ratings()
        
        # Input new jobs to the library.
        elif(main_nav == '1'):
            new_jobs_to_lib()
        
        # Manually rate jobs.
        elif(main_nav == '2'):
            manually_rate_jobs()
        
        # Manually rank jobs.
        elif(main_nav == '3'):
            manually_rank_jobs()
        
        # Run training algorithm.
        elif(main_nav == '4'):
            train_NN()
        
        # View/export results based on currently stored job library and trained thetas.
        elif(main_nav == '5'):
            view_job_results()
        
        # User feedback for entering invalid text into input request.
        else:
            print(invalid_main_nav_message)


# In[24]:

if __name__ == "__main__":
    # Execute main content.
    main_job_hunter()


# In[ ]:



