
# coding: utf-8

# In[ ]:

def create_color_dict(color_keys):
    
    color_dict = {}
    color_counter = 0
    
    for key in color_keys:
        if (color_counter == 0):
            color_dict[key] = 'blue'
        elif(color_counter == 1):
            color_dict[key] = 'red'
        elif(color_counter == 2):
            color_dict[key] = 'green'
        elif(color_counter == 3):
            color_dict[key] = 'orange'
        elif(color_counter == 4):
            color_dict[key] = 'purple'
        else:
            color_dict[key] = 'grey'
        
        color_counter = color_counter +1
    
    return color_dict


# In[ ]:

def create_color_list(color_by_pdSeries):
    
    unique_items = color_by_pdSeries.unique()
    color_dict = create_color_dict(unique_items)
    
    color_list = []
    for item in color_by_pdSeries:
        color_list.append(color_dict[item])
    
    return color_list


# In[1]:

def create_job_chart(plot_data_df, x_data_header, y_data_header, color_by_header, data_labels_header=None,
                    output_file_path='Interest_vs_Qualifications_scatter.html'):  
    
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Title
    from bokeh.layouts import row, widgetbox
    from bokeh.models.widgets import DataTable, TableColumn
    
    plot_data_df['dot_colors'] = create_color_list(plot_data_df[color_by_header])
    
    # Create a ColumnDataSource object out of the plot_df dataframe
    source = ColumnDataSource(plot_data_df)
    
    hover = HoverTool(tooltips=[
            ("Job Title: ", "@job_title"),
            ("Ref #: ", "@ref_number"),
            ("Date Posted: ", "@date_posted"),
            ("Company: ", "@company"),
            ("Location: ", "@location"),
        ])
    Tools = [hover,'box_zoom,box_select,resize,reset,save,wheel_zoom']
    
    p = figure(plot_width=700, plot_height=700, tools=Tools)
    p.add_layout(Title(text="Job Posting Compatability Scatter Plot", align="center"), "above")
    p.add_layout(Title(text="Interest Exhibitted in the Job Posting", align="center"), "left")
    p.add_layout(Title(text="Compatability of Job Requirements and Skills", align="center"), "below")
    
    # create scatter plot
    p.scatter(x=x_data_header, y=y_data_header, color='dot_colors', size=5, source=source)
    
    if(data_labels_header != None):
        labels = LabelSet(x=x_data_header, y=y_data_header, text=data_labels_header, text_font_size='1', level='glyph',
                      x_offset=-25, y_offset=5, source=source, render_mode='canvas')
        p.add_layout(labels)
    
    columns = [
        TableColumn(field='date_posted', title='Date Posted'),
        TableColumn(field='job_title', title='Job Title'),
        TableColumn(field='ref_number', title='Reference Number'),
        TableColumn(field='company', title='Company'),
        TableColumn(field='location', title='Location'),
        TableColumn(field='overall_score', title='Compatability Score'),
    ]
    
    data_table = DataTable(source=source, columns=columns, width=650, height=700)
    
    output_file(output_file_path)
    show(row(p, widgetbox(data_table)))
    


# In[2]:

if __name__ == "__main__":
    # Execute main content.
    print("You are trying to run custom_charts.py on its own. This action is not currently supported, sorry for the inconvenience.")


# In[ ]:



