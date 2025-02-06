import cv2
import yaml
import numpy as np
from datetime import datetime

class VideoProcessor:
    def __init__(self, config_path="config/params.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.cap = None
        self.trackbar_window = "Parameters"
        self.initialize_ui()

    def initialize_ui(self):
        """Create trackbars for real-time tuning"""
        cv2.namedWindow(self.trackbar_window)
        cv2.createTrackbar("Canny Thresh1", self.trackbar_window, self.config["canny"]["threshold1"], 255, self.nothing)
        cv2.createTrackbar("Canny Thresh2", self.trackbar_window, self.config["canny"]["threshold2"], 255, self.nothing)
        cv2.createTrackbar("Hough Thresh", self.trackbar_window, self.config["hough"]["threshold"], 500, self.nothing)

    def nothing(self, x):
        """Dummy function for trackbar"""
        pass

    def process_frame(self, frame):
        """Process a single frame with current parameters"""
        t1 = cv2.getTrackbarPos("Canny Thresh1", self.trackbar_window)
        t2 = cv2.getTrackbarPos("Canny Thresh2", self.trackbar_window)
        h_thresh = cv2.getTrackbarPos("Hough Thresh", self.trackbar_window)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.config["canny"]["blur_kernel"], self.config["canny"]["blur_kernel"]), 0)
        edges = cv2.Canny(blurred, t1, t2)
        
        lines = cv2.HoughLinesP(
            edges,
            rho=self.config["hough"]["rho"],
            theta=np.deg2rad(self.config["hough"]["theta"]),
            threshold=h_thresh,
            minLineLength=self.config["hough"]["min_line_length"],
            maxLineGap=self.config["hough"]["max_line_gap"]
        )
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        return frame

    def run(self):
        """Main processing loop"""
        if self.config["input"]["source_type"] == "webcam":
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(self.config["input"]["path"])
        
        if not self.cap.isOpened():
            raise IOError("Cannot open video source")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame(frame)
            cv2.imshow("Output", processed_frame)
            
            if cv2.waitKey(1) == 27:  # Exit on ESC
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = VideoProcessor()
    processor.run()