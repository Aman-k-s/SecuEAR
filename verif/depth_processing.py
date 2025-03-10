import os
import open3d as o3d
import numpy as np
import cv2

# Ensure output folder exists
OUTPUT_FOLDER = "depth_maps/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_ply(file, output_path):
    """
    Loads, cleans, and converts a .ply scan to a depth map.
    Returns the path of the saved depth map.
    """
    # Read directly from an in-memory file
    pcd = o3d.io.read_point_cloud(file)
    if not pcd.has_points():
        print("❌ ERROR: No valid points in the uploaded file.")
        return None

    # Clean the point cloud (remove noise)
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=5, std_ratio=1.2)
    cleaned_pcd = pcd.select_by_index(ind)

    # Generate and save depth map
    return generate_fixed_depth_map(cleaned_pcd, output_path)

def generate_fixed_depth_map(pcd, output_path, image_size=(256, 256)):
    """
    Converts a cleaned point cloud into a depth map and saves it.
    """
    if not pcd.has_points():
        print("❌ ERROR: No valid point cloud! Skipping.")
        return None

    # Normalize & Center Points
    points = np.asarray(pcd.points)
    centroid = np.mean(points, axis=0)
    points -= centroid
    max_range = np.max(np.linalg.norm(points, axis=1))
    points /= max_range  

    # Orthographic Projection (Front View)
    fx, fy, cx, cy = 250, 250, image_size[0] // 2, image_size[1] // 2
    depth_map = np.ones(image_size) * 255  

    for pt in points:
        x, y, z = pt
        img_x = int(fx * x + cx)
        img_y = int(fy * y + cy)

        if 0 <= img_x < image_size[0] and 0 <= img_y < image_size[1]:  
            depth_value = int((z + 1) * 127)  
            depth_map[img_y, img_x] = depth_value

    # Apply slight blur
    depth_map = depth_map.astype(np.uint8)
    depth_map = cv2.GaussianBlur(depth_map, (3, 3), 0)

    # Save depth map
    cv2.imwrite(output_path, depth_map)
    return output_path  # Return file path
