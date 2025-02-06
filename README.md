# Vision Tuner 🚀

A real-time tunable OpenCV pipeline for lane detection (or general vision tasks). Adjust parameters via YAML config or GUI trackbars and visualize changes instantly. Works with **images**, **videos**, and **webcam feeds**.

![Example Output](https://via.placeholder.com/800x400.png?text=Input+vs+Output+Comparison) *(Replace with your example image/video)*

---

## Features ✨
- **Real-time tuning** for Canny edge detection and Hough line transforms.
- **YAML configuration** for easy parameter management.
- Supports **images**, **videos**, and **webcam feeds**.
- Built-in error handling and parameter validation.

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vision-tuner.git
   cd vision-tuner

2. Installing requirements:
    ```bash
    pip install -r requirements.txt



3. For Images :
    ```bash
    python src/image_processor.py --config config/params.yaml

   For Video:
    ```bash
    python src/video_processor.py