
# coding: utf-8

# In[1]:

def return_digits_only(input_str):
    output_str = ''.join([i for i in input_str if i.isdigit()])
    
    return output_str


# In[2]:

def return_date_posted_appl(input_date_str):
    
    date_str = input_date_str.strip('Posted: ')
    
    return date_str

def get_apple_job_data(html):
    
    from bs4 import BeautifulSoup
    
    job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}

    soup = BeautifulSoup(html, 'html.parser')
    
    data_table = soup.find(class_="sosumi").find_all('li')
    
    job_data_dict['job_title'] = soup.h2.get_text()
    job_data_dict['ref_number'] = return_digits_only(data_table[0].get_text())
    job_data_dict['date_posted'] = return_date_posted_appl(data_table[2].get_text())
    job_data_dict['location'] = data_table[1].get_text()
    
    return job_data_dict


# In[3]:

def get_intui_surgic_job_data(html):
    
    from bs4 import BeautifulSoup
    
    job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}
    
    soup = BeautifulSoup(html, 'html.parser')
        
    job_data_dict['job_title'] = soup.find(id='requisitionDescriptionInterface.reqTitleLinkAction.row1').get_text()
    job_data_dict['ref_number'] = soup.find(id='requisitionDescriptionInterface.reqContestNumberValue.row1').get_text()
    job_data_dict['date_posted'] = ''
    job_data_dict['location'] = soup.find(id='requisitionDescriptionInterface.ID1614.row1').get_text()
    
    return job_data_dict


# In[4]:

def get_udacity_job_data(html):
    
    from bs4 import BeautifulSoup
    
    job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}
    
    soup = BeautifulSoup(html, 'html.parser')
        
    job_data_dict['job_title'] = soup.find(class_="posting-headline").h2.get_text()
    job_data_dict['ref_number'] = ''
    job_data_dict['date_posted'] = ''
    job_data_dict['location'] = soup.find(class_="sort-by-time posting-category medium-category-label").get_text()
    
    return job_data_dict


# In[5]:

def get_tesla_motors_job_data(html):
    
    from bs4 import BeautifulSoup
    
    job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}
    
    soup = BeautifulSoup(html, 'html.parser')
        
    job_data_dict['job_title'] = soup.h1.get_text()
    job_data_dict['ref_number'] = soup.find_all(class_="formFieldNormal top")[0].get_text()
    job_data_dict['date_posted'] = ''
    job_data_dict['location'] = soup.find_all(class_="formFieldNormal top")[1].get_text()
    
    return job_data_dict


# In[37]:

def get_google_job_data(html):
    
    from bs4 import BeautifulSoup
    
    job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}
    
    soup = BeautifulSoup(html, 'html.parser')
        
    job_data_dict['job_title'] = soup.find(itemprop="name title").get_text()
    job_data_dict['ref_number'] = ''
    job_data_dict['date_posted'] = soup.find(itemprop="datePosted").get_text()
    job_data_dict['location'] = soup.find(itemprop="name").get_text()
    
    return job_data_dict


# In[38]:

def get_job_data(jobs_df):
    """
    Update jobs_df with the fields job_title, ref_number, date_posted, and location.
    These values will be scraped from the field job_desc_html. How the data is
    scraped will depend on the layout of the html. html layout is dependent on the 
    company.
    """
    import pandas as pd
    
    job_data_list = []
    
    for i in range(len(jobs_df['job_desc_html'])):
        
        job_data_dict = {'job_title':'', 'ref_number':'', 'date_posted':'', 'location':''}
        
        if(jobs_df.iloc[i]['company'] == 'Apple'):
            job_data_dict = get_apple_job_data(jobs_df.iloc[i]['job_desc_html'])
            
        elif(jobs_df.iloc[i]['company'] == 'Intuitive Surgical'):
            job_data_dict = get_intui_surgic_job_data(jobs_df.iloc[i]['job_desc_html'])
        
        elif(jobs_df.iloc[i]['company'] == 'Udacity'):
            job_data_dict = get_udacity_job_data(jobs_df.iloc[i]['job_desc_html'])
            
        elif(jobs_df.iloc[i]['company'] == 'Tesla Motors'):
            job_data_dict = get_tesla_motors_job_data(jobs_df.iloc[i]['job_desc_html'])
            
        elif(jobs_df.iloc[i]['company'] == 'Google'):
            job_data_dict = get_google_job_data(jobs_df.iloc[i]['job_desc_html'])
        
        job_data_list.append(job_data_dict)
    
    return pd.DataFrame(job_data_list)


# In[39]:

def load_jobs_from_html(job_path):
    
    from bs4 import BeautifulSoup
    import pandas as pd

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


# In[40]:

if __name__ == "__main__":
    
    import sql_pandas
    
    file_path = input('Please enter the file path of the file containing'
                       ' the html you would like to add to the library.\n')
    new_jobs_df = load_jobs_from_html(file_path)
    
    company =  input('Please enter the company name associated with the file.\n')
    new_jobs_df['company'] = company
    
    # Execute main content.
    print(get_job_data(new_jobs_df))


# In[ ]:



