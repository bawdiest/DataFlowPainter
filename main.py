#!/usr/bin/env python
# coding: utf-8

# In[1]:


import graphviz
import pandas as pd
import sys


# Process parameters
try: infile = sys.argv[1]
except: infile = 'demo/input.csv'

#try: output = sys.argv[2]
#except: output = 'output'
output = 'output'

print('Painting DataFlow from input file ' + infile + '...', end="")

data_df = pd.read_csv(infile, header=0, sep=",")


columns = ['Object', 'Type']
s_df = data_df[['Source', 'Source Type']]
t_df = data_df[['Target', 'Target Type']]
s_df.columns = columns
t_df.columns = columns

nodes_df = pd.concat([s_df,t_df], ignore_index=True, axis=0)


type_dict = {"CP" : 'images/CP.png', 
             "aDSO": 'images/aDSO.png', 
             "CV" : 'images/CV.png', 
             "Query": 'images/BExQuery.PNG', 
             "IO": 'images/InfoObject.PNG', 
             "DataSource": 'images/DataSource.png',
            "Table": 'images/Table.png'}

nodes_df['image'] = nodes_df['Type'].map(type_dict)
nodes_df.drop_duplicates(subset=['Object'], keep='first', inplace=True)


datamodel_graph = graphviz.Digraph(comment='Data Model Target', format='png')

for i, node in nodes_df.iterrows():
    
    label_str = node['Object']
    label_str = '\n'.join(label_str[i:i+12] for i in range(0, len(label_str), 12))
    
    datamodel_graph.node(node['Object'], 
                         label = label_str, 
                         shape='underline', 
                         image = node['image'], 
                         imagepos='mc', 
                         labelloc='b',
                         fontname = 'Helvetica',
                         fontsize="10pt",
                         color="grey",
                         imagescale='false',
                         fixedsize='true',
                         height='1',
                         width='1'
                        )


for i, edge in data_df.iterrows():
    try:
        lbl = edge['Label']
        if type(lbl) != str: lbl = ''
    except:
        lbl = ''   
    
    
    datamodel_graph.edge(edge['Target'], edge['Source'],
                        label=lbl,
                        fontname='Helvetica',
                        fontsize='8pt',
                        #taillabel=lbl,
                        #headlabel=lbl,
                        #decorate='true',
                        #labelfontname='Helvetica',
                        #labelfontsize='8pt',
                        
                        dir='back')

try:
    datamodel_graph.render(output)
    print (' DONE')
except: print(' FAIL')