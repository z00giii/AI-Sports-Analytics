import cv2
import torch
from ultralytics import YOLO

class SportsObjectDetector:
    def __init__(self, sport='basketball'):
        # Load sport-specific YOLOv8 model
        self.model = YOLO(f'weights/{sport}_yolov8.pt')
        self.tracker = BYTETracker()
        self.sport = sport
        self.class_map = self._get_class_map(sport)
        
    def _get_class_map(self, sport):
        if sport == 'basketball':
            return {0: 'player', 1: 'ball', 2: 'referee', 3: 'hoop'}
        else:  # football
            return {0: 'player', 1: 'ball', 2: 'referee', 3: 'goalpost'}
    
    def detect(self, frame):
        # Run YOLOv8 inference
        results = self.model(frame)
        
        # Extract and track objects
        detections = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            # Update tracker with new detections
            tracks = self.tracker.update(boxes, scores, class_ids, frame)
            
            for track in tracks:
                track_id = track.track_id
                bbox = track.tlwh
                class_id = track.class_id
                detections.append({
                    'track_id': track_id,
                    'bbox': bbox,
                    'class': self.class_map[class_id],
                    'confidence': track.score
                })
        
        return detections

# Usage example
detector = SportsObjectDetector(sport='basketball')
cap = cv2.VideoCapture('game_footage.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    detections = detector.detect(frame)
    visualize_detections(frame, detections)  # Custom visualization function
