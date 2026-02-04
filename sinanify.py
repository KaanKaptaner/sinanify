import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

IMG_SIZE = (48,48)
PROXIMITY_WEIGHT = 0.1
FRAMES = 110

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_SOURCE = os.path.join(BASE_DIR, "imgs", "source (1).jpg")
PATH_TARGET = os.path.join(BASE_DIR, "imgs", "target.jpg")

def load_image(path):
    try:
        img = Image.open(path).convert('RGB')
        img = img.resize(IMG_SIZE)
        return np.array(img)
    except FileNotFoundError:
        return None

def calculate_assignment(source_pixels, target_pixels, width, height):
    color_diff = np.linalg.norm(source_pixels[:, None, :] - target_pixels[None, :, :], axis=2)
    norm_color = color_diff / 441.67

    coords = np.array([(x, y) for y in range(height) for x in range(width)])
    pos_diff = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2)
    max_dist = np.sqrt(width**2 + height**2)
    norm_pos = pos_diff / max_dist

    cost_matrix = (1 - PROXIMITY_WEIGHT) * norm_color + PROXIMITY_WEIGHT * norm_pos
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    return row_ind, col_ind

def main():
    source_img = load_image(PATH_SOURCE)
    target_img = load_image(PATH_TARGET)
    
    if source_img is None or target_img is None:
        return

    source_pixels = source_img.reshape(-1, 3)
    target_pixels = target_img.reshape(-1, 3)
    width, height = IMG_SIZE

    row_ind, col_ind = calculate_assignment(source_pixels, target_pixels, width, height)

    coords = np.array([(x, y) for y in range(height) for x in range(width)])
    start_pos = coords
    
    target_x = col_ind % width
    target_y = col_ind // width
    end_pos = np.column_stack((target_x, target_y))

    colors = source_pixels / 255.0

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.invert_yaxis()
    ax.axis('off')
    ax.set_aspect('equal')
    
    scat = ax.scatter(start_pos[:, 0], start_pos[:, 1], c=colors, s=50, marker='s', edgecolors='none')

    def update(frame):
        if frame >= FRAMES:
            t = 1.0
        else:
            t = frame / FRAMES
        
        ease = t * t * (3 - 2 * t)
        current_pos = start_pos + (end_pos - start_pos) * ease
        
        scat.set_offsets(current_pos)
        return scat,

    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=FRAMES + 1,
        interval=30, 
        blit=True, 
        repeat=False
    )

    plt.show()

if __name__ == "__main__":
    main()