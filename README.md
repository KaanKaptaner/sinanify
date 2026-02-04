# sinanify: Optimal Pixel Transport Visualization

**sinanify** is a Python-based computational visualization tool that morphs one image into another by solving the **Linear Assignment Problem (LAP)**. 

Unlike standard cross-dissolve transitions (fading), this project treats every pixel as a particle. It calculates the optimal path for every single pixel from the source image to the target image, minimizing a cost function based on color similarity and spatial proximity.

![sinanified](https://github.com/user-attachments/assets/de06f575-113f-4fc5-b390-0cd0e587d837)

## Mathematical Background

This project implements the **Hungarian Algorithm** (via `scipy.optimize.linear_sum_assignment`) to solve the combinatorial optimization problem.

The cost matrix $C$ for assigning pixel $i$ (from source) to pixel $j$ (in target) is defined as:

$$Cost_{i,j} = (1 - w) \cdot ||Color_i - Color_j|| + w \cdot ||Pos_i - Pos_j||$$

Where:
* **Color Distance:** Euclidean distance between RGB vectors.
* **Spatial Distance:** Euclidean distance between $(x,y)$ coordinates.
* **$w$ (Proximity Weight):** A hyperparameter balancing color matching vs. movement distance.

## 🚀 Features

* **Optimal Transport:** Guarantees the mathematically "best" movement for pixels based on the defined cost constraints.
* **Weighted Metrics:** Configurable balance between maintaining color accuracy and minimizing pixel travel distance.
* **Easing Animations:** Implements a cubic easing function (`t * t * (3 - 2 * t)`) for smooth, organic movement.
* **Scientific Stack:** Built on top of robust libraries: NumPy, SciPy, and Matplotlib.

## 🛠️ Installation

### Prerequisites
* Python 3.8 or higher

### Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/sinanify.git](https://github.com/YOUR_USERNAME/sinanify.git)
    cd sinanify
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *If `requirements.txt` is missing, install the core libraries manually:*
    ```bash
    pip install numpy scipy matplotlib pillow
    ```

## 💻 Usage

1.  **Prepare Images**
    Place your source and target images in an `imgs/` directory.
    * `imgs/source.jpg`
    * `imgs/target.jpg`

2.  **Configuration**
    Open `sinanify.py` and adjust the configuration constants at the top of the file if necessary:

    ```python
    IMG_SIZE = (48, 48)       # Resolution (Keep low due to algorithmic complexity)
    PROXIMITY_WEIGHT = 0.1    # 0.0 = Only Color matches, 1.0 = Only Position matches
    FRAMES = 110              # Animation duration
    ```

3.  **Run the Simulation**
    ```bash
    python sinanify.py
    ```

## ⚠️ Performance Note

The Hungarian Algorithm has a time complexity of **$O(n^3)$**. 
Because the number of "agents" ($n$) is the total pixel count ($Width \times Height$), the computational cost grows exponentially with resolution.

* **48x48 (2,304 pixels):** Runs in seconds.
* **64x64 (4,096 pixels):** May take significantly longer.
* **100x100+:** Not recommended for this exact implementation without optimization (e.g., approximation algorithms or Sinkhorn distances).

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
