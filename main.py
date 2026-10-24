import cv2
from pose_tracker import PoseTracker 
from plank_logic import is_plank, plank_timer

tracker = PoseTracker()
cap = cv2.VideoCapture(0)
timer = plank_timer()

while True:
    ok, frame = cap.read()

    if not ok:
        break

    tracker.process(frame)
    tracker.draw(frame)

    points = tracker.get_side_points(frame)

    good = False
    if points:
        good = is_plank(points["shoulder"], points["hip"], points["ankle"])
    seconds = timer.update(good)
    color = (0, 255, 0) if good else (0, 0, 255)
    cv2.putText(frame, f"Time: {seconds:.1f}s", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"Best: {timer.best:.1f}s", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
    cv2.imshow("Plank Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()