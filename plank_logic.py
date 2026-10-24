import numpy as np
import math as math
import time

def calc_angle(a, b, c):
    # a, b, c la cac toa do (x,y) tinh goc tai b
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = b - a
    bc = b - c

    dot = ba[0]*bc[0] + ba[1]*bc[1]
    lenba = math.sqrt(ba[0]**2 + ba[1]**2)
    lenbc = math.sqrt(bc[0]**2 + bc[1]**2)
    if lenba == 0 or lenbc == 0:
        return 0.0
    cos_angle = dot / (lenba * lenbc)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)   # tranh loi lam tron

    return np.degrees(np.arccos(cos_angle))

def body_tilt(shoulder, ankle):
    # do nghieng cua duong vai-mat ca so voi phuong nam ngang
    dx = ankle[0] - shoulder[0]
    dy = ankle[1] - shoulder[1]
    return math.degrees(math.atan2(abs(dy), abs(dx)))

MIN_HIP_ANGLE = 150
MAX_TILT = 10

def is_plank(shoulder, hip, ankle):
    angle = calc_angle(shoulder, hip, ankle)
    tilt = body_tilt(shoulder, ankle)

    straight = angle > MIN_HIP_ANGLE
    horizontal = tilt < MAX_TILT
    
    return straight and horizontal

START_DELAY = 1.0
LOST_TOLERANCE = 1.0

class plank_timer:
    def __init__(self):
        self.state = "Đứng"
        self.good_since = None
        self.bad_since = None
        self.start_time = None
        self.best = 0.0

    def update(self, is_good):
        # goi moi khung hinh voi true/flase, tra ve so giay hien tai
        now = time.time()

        if self.state == "Đứng":
            if is_good:
                if self.good_since is None:
                    self.good_since = now
                if now - self.good_since >= START_DELAY:
                    self.state = "PLANK"
                    self.start_time = self.good_since
                    self.bad_since = None
            else:
                self.good_since = None

        elif self.state == "PLANK":
            if is_good:
                self.bad_since = None
            else:
                if self.bad_since is None:
                    self.bad_since = now
                if now - self.bad_since >= LOST_TOLERANCE:
                    self.best = max(self.best, self.elapsed(self.bad_since))
                    self.state = "Đứng"
                    self.good_since = None
                    self.start_time = None

        return self.elapsed(now)

    def elapsed(self, now):
        if self.state != "PLANK":
            return 0.0
        return now - self.start_time