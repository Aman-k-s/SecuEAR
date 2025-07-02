#!/usr/bin/env python
# coding: utf-8

# In[1]:


import open3d as o3d
import numpy as np
import cv2

def convert_ply_to_depth(ply_path, output_path, size=(224, 224)):
    pcd = o3d.io.read_point_cloud(ply_path)
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(pcd)
    ctr = vis.get_view_control()
    ctr.set_zoom(0.7)
    vis.poll_events()
    vis.update_renderer()
    img = vis.capture_depth_float_buffer(True)
    vis.destroy_window()

    img = np.asarray(img)
    img = cv2.resize(img, size)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    img = img.astype(np.uint8)
    cv2.imwrite(output_path, img)


# In[ ]:




