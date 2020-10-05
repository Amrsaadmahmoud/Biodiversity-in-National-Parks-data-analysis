
# coding: utf-8

# # :::About This Project:::

# For this project, i wll act as a data analyst for the National Park Service.
# 
# i wll be helping them analyze data on endangered species from several different parks.
# 
# The National Parks Service would like to perform some data analysis on the conservation statuses of these species and to investigate if there are any patterns or themes to the types of species that become endangered. During this project,i will analyze, clean up, and plot data, pose questions and seek to answer them in a meaningful way.
# 
# After i perform analysis, i wll be creating a presentation to share my findings with the National Park Service

# # :::Step one::: Gather the data:::

# In[48]:

#import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency


# In[4]:

#import the data set
df=pd.read_csv('E:/my_work_my_work/data analysis project/Biodiversity in National Parks/species_info.csv')


# In[5]:

#show the data
df.head(6)


# # Step two:::assess the data

# In[6]:

df.info()


# In[7]:

df.dtypes


# In[8]:

df.shape


# In[14]:

#How many different species are in the species DataFrame
number_of_species=df.scientific_name.nunique()
number_of_species


# In[16]:

#What are the different values of category in the DataFrame species
types_of_category=df.category.unique()
types_of_category


# In[18]:

#What are the different values of conservation_status
diff_values_of_conservation_status=df.conservation_status.unique()
diff_values_of_conservation_status


# In[20]:

# count how many scientific_name falls into each conservation_status criteria
conservation_count=df.groupby('conservation_status').scientific_name.nunique().reset_index()


# In[21]:

conservation_count


# # Step three:::clean the data

# ***replace NaN in conservation_status column  with 'No Intervention'***

# In[22]:

#code
df.conservation_status.fillna('No Intervention',inplace=True)


# In[23]:

#test
conservation_count_fixed=df.groupby('conservation_status').scientific_name.nunique().reset_index()
conservation_count_fixed


# # Step four:::perform EDA

# ***Plotting Conservation Status by Species***

# In[30]:

protection_counts = df.groupby('conservation_status').scientific_name.nunique().reset_index().sort_values(by='scientific_name')
    


# In[31]:

protection_counts


# In[32]:

plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()


# # Investigating Endangered Species

# ***Are certain types of species more likely to be endangered?***

# In[34]:

#Create a new column in species called is_protected, which is True if conservation_status 
#is not equal to 'No Intervention', and False otherwise.

df['is_protected']=df.conservation_status!='No Intervention'
#test
df.head(6)


# In[35]:

#Group the species data frame by the category and is_protected columns and 
#count the unique scientific_names in each grouping
category_counts=df.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# In[36]:

#test
category_counts


# In[42]:

#create category_counts as a pivot table
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()


# In[43]:

category_pivot


# In[44]:

category_pivot.columns=['category','not_protected','protected']


# In[45]:

category_pivot


# In[46]:

category_pivot['percent_protected']=category_pivot.protected/(category_pivot.protected+category_pivot.not_protected)


# In[47]:

category_pivot


# ***Let’s see if we can use it to answer the question “are certain types of species more likely to be endangered?”.***

# It looks like Mammals are more likely to be endangered than Birds, but is it a significant difference? i can do a significance test to see if this statement is true. In this test, our null hypothesis is that this difference is due to chance.

# **i use Chi-Squared Test for Significance**

# In[49]:

#Create a table called contingency and fill it with the correct values
contingency = [[30, 146],
              [75, 413]]


# In[50]:

pval = chi2_contingency(contingency)[1]
print(pval)


# ***No significant difference because pval > 0.05***

# In[51]:

#Let’s test another. Is the difference between Reptile and Mammal significant?
contingency_reptile_mammal = [[30, 146],
                              [5, 73]]


# In[52]:

pval_reptile_mammal = chi2_contingency(contingency_reptile_mammal)[1]
print(pval_reptile_mammal)


# ***Significant difference! pval_reptile_mammal < 0.05***

# # Now i can answer our initial question:

# 
# ***Are certain types of species more likely to be endangered?***

# I initially saw that there was a slight difference in the percentages of birds and mammals 
# that fall into a protected category. Our null hypothesis here is that this difference was a 
# result of chance.
# 
# When i ran our chi-squared test, i found a p-value of ~0.688, so i can conclude that 
# the difference between the percentages of protected birds and mammals is not significant
# and is a result of chance.
# 
# But, when i compared the percentages of protected reptiles and mammals and ran the same
# chi-squared test, i calculated a p-value of ~0.038, which is significant.
# 
# Therefore,i can conclude that certain types of species are more likely to be endangered than others.

# # Observations DataFrame

# In[53]:

df2=pd.read_csv('E:/my_work_my_work/data analysis project/Biodiversity in National Parks/observations.csv')


# In[54]:

df2.head(6)


# # In Search of Sheep

# A team of ruminant-enthused scientists has been tracking the movements 
# of various species of sheep across different national parks 
# and have asked for me assistance in analyzing the observation and species DataFrames to 
# help track sheep locations.
# 
# Because the observation DataFrame only contains the scientific names of species, 
# i will have to use the species DataFrame to look for any names that refer to sheep.

# In[55]:

#create a new column in species called is_sheep which is True if the common_names
#contains 'Sheep', and False otherwise
df['is_sheep'] = df.common_names.apply(lambda x: 'Sheep' in x)


# In[56]:

df.head(5)


# In[57]:

#Select the rows of species where is_sheep is True
df_is_sheep=df[df.is_sheep]


# In[58]:

df_is_sheep


# In[60]:

#Select the rows of species where is_sheep is True and category is Mammal
sheep_df = df[(df.is_sheep) & (df.category == 'Mammal')]


# In[61]:

sheep_df


# In[63]:

#Merging Sheep and Observation DataFrames
sheep_observations = df2.merge(sheep_df)


# In[64]:

sheep_observations


# In[66]:

#How many total sheep sightings
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()


# In[67]:

obs_by_park


# ***Plotting Sheep Sightings***

# In[69]:

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),
        obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()


# # Foot and Mouth Reduction Effort 

# Park Rangers at Yellowstone National Park have been running a program to reduce the rate of 
# foot and mouth disease at that park. The scientists want to test whether or not this program
# is working. They want to be able to detect reductions of at least 5 percentage points. For instance, 
# if 10% of sheep in Yellowstone have foot and mouth disease, they’d like to be able to know this,
# with confidence

# The only information that the scientists currently have is that last year it was recorded that 15% of sheep at Bryce National Park have foot and mouth disease

# In[70]:

baseline = 15

minimum_detectable_effect = 100*5./15

sample_size_per_variant = 870

yellowstone_weeks_observing = sample_size_per_variant/507.

bryce_weeks_observing = sample_size_per_variant/250.

print(bryce_weeks_observing)


# What do the results of the last exercise tell us?
# 
# Given a baseline of 15% occurrence of foot and mouth disease in sheep at Bryce National Park, i found that if the scientists wanted to be sure that a >5% drop in observed cases of foot and mouth disease in the sheep at Yellowstone was significant they would have to observe at least 870 sheep.
# Then, using the observation data i analyzed earlier, i found that this would take approximately one week of observing in Yellowstone to see that many sheep, or approximately two weeks in Bryce to see that many sheep

# # **** Congratulations! THE END******
