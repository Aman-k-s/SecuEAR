import open3d as o3d
import numpy as np
import cv2
import os

def generate_depth_map(filename, width=224, height=224):
    input_path = os.path.join("ply_scans", filename)
    output_filename = filename.replace(".ply", ".png")
    output_path = os.path.join("depth_maps", output_filename)

    mesh = o3d.io.read_triangle_mesh(input_path)
    if not mesh.has_triangles():
        print(f" Skipped: {filename}")
        return

    mesh.compute_vertex_normals()

    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False, width=width, height=height)
    vis.add_geometry(mesh)

    # Updated viewpoint
    ctr = vis.get_view_control()
    bbox = mesh.get_axis_aligned_bounding_box()
    center = bbox.get_center()
    extent = bbox.get_extent()

    cam_pos = center + [1.0 * extent[0], 0, 0]  # Adjust distance
    ctr.set_lookat(center)
    ctr.set_front([1, 0, 0])  # side view
    ctr.set_up([0, 1, 0])
    ctr.set_zoom(0.6)  # Moderate zoom

    vis.poll_events()
    vis.update_renderer()

    depth = vis.capture_depth_float_buffer()
    depth_np = np.asarray(depth)

    # Normalize and invert
    depth_norm = cv2.normalize(depth_np, None, 0, 255, cv2.NORM_MINMAX)
    depth_uint8 = depth_norm.astype(np.uint8)
    depth_uint8 = cv2.bitwise_not(depth_uint8)

    os.makedirs("depth_maps", exist_ok=True)
    cv2.imwrite(output_path, depth_uint8)
    print(f"Saved: {output_path}")

    vis.destroy_window()

if __name__ == "__main__":
    os.makedirs("depth_maps", exist_ok=True)
    for file in os.listdir("ply_scans"):
        if file.endswith(".ply"):
            generate_depth_map(file)



