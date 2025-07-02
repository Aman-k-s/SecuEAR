#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from matcher import match




# In[1]:


query_img = "depth_maps/aman left.png"
db_folder = "depth_maps"
threshold = 0.9

results = match(query_img, db_folder, threshold)

if results:
    print("Matching images found:")
    for img, score in results:
        print(f"{img}: similarity = {score:.4f}")
else:
    print("No good matches found.")


# In[ ]:


get_ipython().system('jupyter nbconvert --to script example_use.ipynb')

