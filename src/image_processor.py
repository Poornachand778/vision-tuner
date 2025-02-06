import cv2
import yaml
import argparse
import numpy as np

def validate_config(config):
    """Ensure parameters are valid"""
    assert config["canny"]["threshold1"] < config["canny"]["threshold2"], "Canny threshold1 must be < threshold2"
    assert config["canny"]["blur_kernel"] % 2 == 1, "Blur kernel must be odd"

def process_image(config):
    try:
        img = cv2.imread(config["input"]["path"])
        if img is None:
            raise FileNotFoundError(f"Image not found at {config['input']['path']}")
        
        # Preprocessing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (config["canny"]["blur_kernel"], config["canny"]["blur_kernel"]), 0)
        
        # Canny Edge Detection
        edges = cv2.Canny(blurred, config["canny"]["threshold1"], config["canny"]["threshold2"])
        cv2.imshow("Edges", edges)
        cv2.waitKey(0)
        # Hough Lines
        lines = cv2.HoughLinesP(
            edges,
            rho=config["hough"]["rho"],
            theta=np.deg2rad(config["hough"]["theta"]),
            threshold=config["hough"]["threshold"],
            minLineLength=config["hough"]["min_line_length"],
            maxLineGap=config["hough"]["max_line_gap"]
        )
        
        # Draw lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        cv2.imshow("Output", img)
        cv2.waitKey(0)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tunable Image Processor")
    parser.add_argument("--config", type=str, default="config/params.yaml", help="Path to config file")
    args = parser.parse_args()
    
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
    
    validate_config(config)
    process_image(config)