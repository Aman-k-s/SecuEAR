#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import cv2


# ## Load a grayscale image, convert to 3-channel and normalize.
# #### Returns: Tensor of shape (1, 3, 224, 224)

# In[ ]:


def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = np.stack([img]*3, axis=-1)  # Convert to 3-channel
    img = Image.fromarray(img.astype(np.uint8))

    transform = transforms.Compose([
        transforms.ToTensor(),  # Shape: (3, 224, 224)
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return transform(img).unsqueeze(0)



# # Pass preprocessed image through MobileNetV2 and get feature embedding.

# In[ ]:


def get_embedding(img_path, model):
    model.eval()
    with torch.no_grad():
        tensor = preprocess_image(img_path)
        embedding = model(tensor)
    return embedding.squeeze(0)  # Shape: (1280,)


# In[ ]:


def cosine_similarity(emb1, emb2):
    return F.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0)).item()


# In[ ]:




