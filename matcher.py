#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import torch
import torch.nn as nn
from torchvision import models
from utils import get_embedding, cosine_similarity


# # Load MobileNetV2

# In[ ]:


mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.classifier = nn.Identity()  # Remove classifier head
mobilenet.eval()


# ### Match a query image against all depth maps in db_folder_path.
# ##### Returns: list of (filename, similarity) above threshold

# In[3]:


def match(query_img_path, db_folder_path, threshold=0.9):
    """
    Match a query image against all depth maps in db_folder_path.
    Returns: list of (filename, similarity) above threshold
    """
    query_embedding = get_embedding(query_img_path, mobilenet)
    matches = []

    for file in os.listdir(db_folder_path):
        if file.endswith(".png"):
            file_path = os.path.join(db_folder_path, file)
            db_embedding = get_embedding(file_path, mobilenet)
            score = cosine_similarity(query_embedding, db_embedding)
            if score >= threshold:
                matches.append((file, score))

    return sorted(matches, key=lambda x: x[1], reverse=True)


# In[ ]:




