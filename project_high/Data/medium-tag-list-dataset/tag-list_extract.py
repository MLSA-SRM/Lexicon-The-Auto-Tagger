# Loads medium_top_1000_tags.csv
# Extracts First Column into a list
# Exports list as file

import pandas as pd 

df_tag = pd.read_csv('C:/Users/Powerhouse/Desktop/Project High/Data/medium-tag-list-dataset/medium_top_1000_tags.csv')

tag_list = df_tag[df_tag.columns[0]].tolist()
tag_list.sort()

df_tag = pd.DataFrame(data=tag_list, columns=['Tags'])
df_tag.to_csv('medium_tag_1000.csv')
#print(tag_list)