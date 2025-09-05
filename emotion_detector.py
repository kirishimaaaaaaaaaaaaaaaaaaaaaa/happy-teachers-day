import cv2
from deepface import DeepFace
import random

cap = cv2.VideoCapture(0)


ret, frame_test = cap.read()
frame_width = frame_test.shape[1]
frame_height = frame_test.shape[0]

pastel_colors = [
    (203, 192, 255),  # Pink
    (255, 192, 203),  # Peach
    (255, 218, 185),  # Light Peach
    (208, 224, 64),   # Teal-ish
    (150, 111, 51),   # Brown
    (230, 230, 250),  # Lavender
    (152, 255, 152),  # Mint
    (255, 255, 153),  # Light Yellow
    (0, 0, 255)       # Red
]


LEFT_ZONE = (50, frame_width//2 - 100)
RIGHT_ZONE = (frame_width//2 + 100, frame_width - 50)
num_balloons_per_side = 5

def create_side_balloons(zone_start, zone_end, count, existing_balloons):
    balloons = []
    attempts = 0
    while len(balloons) < count and attempts < 200:
        x_pos = random.randint(zone_start, zone_end)
        y_pos = random.randint(400, 700)
        color = random.choice(pastel_colors)
        overlap = False
        for b in existing_balloons + balloons:
            if abs(x_pos - b["x"]) < 60 and abs(y_pos - b["y"]) < 60:
                overlap = True
                break
        if not overlap:
            balloons.append({"x": x_pos, "y": y_pos, "color": color})
        attempts += 1
    return balloons

balloons = []
balloons += create_side_balloons(*LEFT_ZONE, num_balloons_per_side, balloons)
balloons += create_side_balloons(*RIGHT_ZONE, num_balloons_per_side, balloons)


def draw_realistic_balloon(frame, balloon):
    
    cv2.ellipse(frame,
                (balloon["x"], balloon["y"]),
                (20, 30), 0, 0, 360,
                balloon["color"], -1)
  
    highlight_x = balloon["x"] - 7
    highlight_y = balloon["y"] - 10
    cv2.circle(frame, (highlight_x, highlight_y), 5, (255, 255, 255), -1)
  
    cv2.line(frame,
             (balloon["x"], balloon["y"] + 30),
             (balloon["x"], balloon["y"] + 60),
             (0, 0, 0), 2)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Emotion detection
    try:
        response = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        for face_data in response:
            x = face_data["region"]["x"]
            y = face_data["region"]["y"]
            w = face_data["region"]["w"]
            h = face_data["region"]["h"]

            if w > 0 and h > 0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame,
                            text=face_data["dominant_emotion"],
                            org=(x, y - 10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(0, 0, 255),
                            thickness=2)
    except:
        pass

    # Teacher's Day message
    cv2.putText(frame,
                text="HAPPY TEACHER'S DAY 💐",
                org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=1.2,
                color=(0, 0, 139),
                thickness=2)

    # Confetti
    for _ in range(20):
        x_conf = random.randint(0, frame.shape[1] - 1)
        y_conf = random.randint(0, frame.shape[0] - 1)
        cv2.circle(frame,
                   (x_conf, y_conf),
                   3,
                   random.choice(pastel_colors),
                   -1)

    # Draw & move balloons
    for i, balloon in enumerate(balloons):
        draw_realistic_balloon(frame, balloon)

        # Move upward
        balloon["y"] -= 5

        
        if balloon["y"] < -50:
            side_zone = LEFT_ZONE if balloon["x"] < frame_width//2 else RIGHT_ZONE
            new_balloons = create_side_balloons(*side_zone, 1, balloons)
            if new_balloons:
                balloons[i] = new_balloons[0]

    # Instructions
    cv2.putText(frame,
                text="Press Q to exit",
                org=(10, frame.shape[0] - 20),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=(0, 0, 255),
                thickness=2)

    # Display full screen
    cv2.namedWindow("Teacher Celebration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Teacher Celebration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Teacher Celebration", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from PIL import Image, ImageSequence
import urllib.request
import io

#load GIF
url = "https://media.tenor.com/WMM8Yjt8BUsAAAAC/happy-teachers-day-teachers-day.gif"
with urllib.request.urlopen(url) as response:
    gif_bytes = io.BytesIO(response.read())

gif = Image.open(gif_bytes)
gif_frames = []

for frame in ImageSequence.Iterator(gif):
    frame = frame.convert("RGB")
    frame = frame.resize((400, 200))  
    cv_frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    gif_frames.append(cv_frame)


height, width = 700, 1000
affirmation_frame = np.zeros((height, width, 3), dtype=np.uint8)
affirmation_frame[:] = (255, 228, 225)  # Misty pink

# Teacher's Day Text 
cv2.putText(affirmation_frame,
            "HAPPY TEACHER'S DAY ",
            org=(50, 100),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1.5,  # reduced from 2
            color=(0, 0, 255),
            thickness=3)


message_lines = [
    "Dear Hibhayasmine l,",
    "Happy Teacher's Day, Hibhayasmine! ",
    "I just want to say thank you for being such an amazing teacher.",
    "You make coding fun and you inspire me to keep learning every day.",
    "I really appreciate your patience, guidance,",
    "and the way you encourage me , it truly means a lot!"
]

y_pos = 180
for line in message_lines:
    cv2.putText(affirmation_frame,
                line,
                org=(50, y_pos),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,  # reduced from 1
                color=(75, 0, 130),  # Indigo
                thickness=2)
    y_pos += 45  


frame_idx = 0
num_gif_frames = len(gif_frames)

cv2.namedWindow("A Special Message", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("A Special Message", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    display_frame = affirmation_frame.copy()


    gif_frame = gif_frames[frame_idx]
    gh, gw, _ = gif_frame.shape
    x_offset = (width - gw) // 2
    y_offset = height - gh - 20 

    display_frame[y_offset:y_offset+gh, x_offset:x_offset+gw] = gif_frame

    cv2.imshow("A Special Message", display_frame)

    frame_idx = (frame_idx + 1) % num_gif_frames  

    if cv2.waitKey(100) & 0xFF == ord("q"):  

cv2.destroyAllWindows()

