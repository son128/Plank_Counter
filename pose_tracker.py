import cv2
import mediapipe as mp

LEFT_SIDE = {"shoulder": 11, "hip": 23, "ankle": 27}
RIGHT_SIDE = {"shoulder": 12, "hip": 24, "ankle": 28}

class PoseTracker:
    def __init__(self, detection_conf=0.5, tracking_conf=0.5):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.results = None

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(rgb)
        return self.results

    def draw(self, frame):
        # ve skeleton
        if self.results and self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )
        return frame

    def get_landmark(self, index):
        # tra ve (x, y, visibility) cua landmark, hoac None
        if self.results is None or self.results.pose_landmarks is None:
            return None
        lm = self.results.pose_landmarks.landmark[index]
        return lm.x, lm.y, lm.visibility
    def get_side_points(self, frame, min_visibility=0.5):
        # chon ben nhin ro hon
        h, w = frame.shape[:2]
        best_points = None
        best_score = -1

        for side in (LEFT_SIDE, RIGHT_SIDE):
            landmarks = {name: self.get_landmark(idx) for name, idx in side.items()}
            if any(lm is None for lm in landmarks.values()):
                continue

            # Điểm của một bên = visibility thấp nhất trong 3 khớp
            score = min(lm[2] for lm in landmarks.values())
            if score > best_score:
                best_score = score
                best_points = {name: (lm[0] * w, lm[1] * h)
                               for name, lm in landmarks.items()}

        if best_points is None or best_score < min_visibility:
            return None
        return best_points