import cv2 # type: ignore
import mediapipe as mp # type: ignore
import math
import time

def draw_hud(frame):
    h, w, _ = frame.shape

    # Slightly darken the displayed camera feed
    # This affects the HUD appearance, not hand tracking.
    frame = cv2.convertScaleAbs(
        frame,
        alpha=0.78,
        beta=-8
    )

    # Holographic glow layer
    glow = frame.copy()
    # Animated holographic scan line
    scan_y = int((time.time() * 120) % h)

    cv2.line(
        frame,
        (15, scan_y),
        (w - 15, scan_y),
        (255, 255, 255),
        1
    )

    # HUD border
    margin = 15

    # HUD border on glow layer
    cv2.rectangle(
        glow,
        (margin, margin),
        (w - margin, h - margin),
        (255, 255, 255),
        3
    )
    # Soft glow
    glow = cv2.GaussianBlur(
        glow,
        (0, 0),
        8
    )

    # Blend glow with camera
    frame = cv2.addWeighted(
        frame,
        1.0,
        glow,
        0.25,
        0
    )

    # Sharp HUD border
    cv2.rectangle(
        frame,
        (margin, margin),
        (w - margin, h - margin),
        (255, 255, 255),
        1
    )

    # Corner brackets
    corner = 28
    thickness = 2

    # Small technical markers
    marker = 8

    cv2.line(
        frame,
        (margin + corner + 8, margin),
        (margin + corner + 8 + marker, margin),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (margin, margin + corner + 8),
        (margin, margin + corner + 8 + marker),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (w - margin - corner - 8, h - margin),
        (w - margin - corner - 8 - marker, h - margin),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (w - margin, h - margin - corner - 8),
        (w - margin, h - margin - corner - 8 - marker),
        (255, 255, 255),
        1
    )

    # Top-left
    cv2.line(frame, (margin, margin), (margin + corner, margin), (255, 255, 255), thickness)
    cv2.line(frame, (margin, margin), (margin, margin + corner), (255, 255, 255), thickness)

    # Top-right
    cv2.line(frame, (w - margin, margin), (w - margin - corner, margin), (255, 255, 255), thickness)
    cv2.line(frame, (w - margin, margin), (w - margin, margin + corner), (255, 255, 255), thickness)

    # Bottom-left
    cv2.line(frame, (margin, h - margin), (margin + corner, h - margin), (255, 255, 255), thickness)
    cv2.line(frame, (margin, h - margin), (margin, h - margin - corner), (255, 255, 255), thickness)

    # Bottom-right
    cv2.line(frame, (w - margin, h - margin), (w - margin - corner, h - margin), (255, 255, 255), thickness)
    cv2.line(frame, (w - margin, h - margin), (w - margin, h - margin - corner), (255, 255, 255), thickness)

    # Title

    cv2.putText(
            frame,
            "HOLOGRAPHIC INTERFACE",
            (50, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    # Live tracking indicator
    status_text = "[ TRACKING ]"
    cv2.putText(
        frame,
        status_text,
        (w - 170, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    # Center holographic reticle
    cx = w // 2
    cy = h // 2

    reticle_size = 18
    gap = 7

    cv2.circle(
        frame,
        (cx, cy),
        reticle_size,
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (cx - reticle_size - gap, cy),
        (cx - gap, cy),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (cx + gap, cy),
        (cx + reticle_size + gap, cy),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (cx, cy - reticle_size - gap),
        (cx, cy - gap),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (cx, cy + gap),
        (cx, cy + reticle_size + gap),
        (255, 255, 255),
        1
    )
    
    # Subtle HUD grid

    grid = frame.copy()
    grid_spacing = 80

    for gx in range(margin + grid_spacing, w - margin, grid_spacing):
        cv2.line(
            grid,
            (gx, margin),
            (gx, h - margin),
            (255, 255, 255),
            1
        )

    for gy in range(margin + grid_spacing, h - margin, grid_spacing):
        cv2.line(
            grid,
            (margin, gy),
            (w - margin, gy),
            (255, 255, 255),
            1
        )

    frame = cv2.addWeighted(
        frame,
        1.0,
        grid,
        0.08,
        0
    )
    
    # Version
    cv2.putText(
        frame,
        "V1.4.3",
        (w - 110, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    return frame
def draw_reticle(frame, x, y, active=False, hand_label="Right"):
    if active:
        radius = 24
        thickness = 3
    else:
        radius = 16
        thickness = 2

    # Main circle
    cv2.circle(
        frame,
        (x, y),
        radius,
        (255, 255, 255),
        thickness
    )

    # Hand label
    cv2.putText(
        frame,
        hand_label,
        (x + radius + 8, y - radius - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1
    )
    # Center point
    cv2.circle(
        frame,
        (x, y),
        4,
        (255, 255, 255),
        -1
    )

    # Four targeting lines
    gap = radius + 5
    length = 12

    # Top
    cv2.line(
        frame,
        (x, y - gap),
        (x, y - gap - length),
        (255, 255, 255),
        2
    )

    # Bottom
    cv2.line(
        frame,
        (x, y + gap),
        (x, y + gap + length),
        (255, 255, 255),
        2
    )

    # Left
    cv2.line(
        frame,
        (x - gap, y),
        (x - gap - length, y),
        (255, 255, 255),
        2
    )

    # Right
    cv2.line(
        frame,
        (x + gap, y),
        (x + gap + length, y),
        (255, 255, 255),
        2
    )

def draw_test_object(frame, cx, cy, size):
    # Holographic test object
    half = size // 2

    cv2.rectangle(
        frame,
        (cx - half, cy - half),
        (cx + half, cy + half),
        (255, 255, 255),
        2
    )

    # Center cross
    cv2.line(
        frame,
        (cx - 10, cy),
        (cx + 10, cy),
        (255, 255, 255),
        1
    )

    cv2.line(
        frame,
        (cx, cy - 10),
        (cx, cy + 10),
        (255, 255, 255),
        1
    )

def draw_panel(frame, x, y, width, height, title, lines):
    # Panel outline
    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (255, 255, 255),
        1
    )

    # Title line
    cv2.line(
        frame,
        (x, y + 38),
        (x + width, y + 38),
        (255, 255, 255),
        1
    )

    # Title
    cv2.putText(
        frame,
        title,
        (x + 15, y + 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Panel information
    for i, line in enumerate(lines):
        cv2.putText(
            frame,
            line,
            (x + 15, y + 70 + i * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "HOLOGRAPHIC INTERFACE - V1.4.3"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        window_name,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    # Independent smoothing for each hand
    smooth_positions = {
        "Left": [0, 0],
        "Right": [0, 0]
    }

    # Stable wrist positions for two-hand tracking
    previous_wrist_positions = {
        "Left": None,
        "Right": None
    }

    smoothing = 0.35

    # Independent pinch states
    pinch_frames = {
        "Left": 0,
        "Right": 0
    }

    required_frames = 4

    # Virtual button
    button_width = 150
    button_height = 55

    # Two-hand holographic test object
    object_x = 640
    object_y = 360
    object_size = 120

   # --------------------------------
    # Object interaction state
    # --------------------------------

    current_hand_points = {}
    current_pinch_states = {}

    object_grabbed = False
    grab_hand = None
    grab_offset_x = 0
    grab_offset_y = 0

    scale_active = False
    scale_start_distance = None
    scale_start_size = None

    interaction_mode = "IDLE"

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:

        while True:

            success, frame = cap.read()

            if not success:
                print("ERROR: Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)

            h, w, _ = frame.shape
            # Responsive button position
            button_x1 = w - button_width - 35
            button_y1 = (h - button_height) // 2

            button_x2 = button_x1 + button_width
            button_y2 = button_y1 + button_height

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = hands.process(rgb_frame)

            # Start each frame with fresh hand data
            current_hand_points.clear()
            current_pinch_states.clear()

            if results.multi_hand_landmarks:

                for hand_index, hand_landmarks in enumerate(
                    results.multi_hand_landmarks
                ):

                    hand_label = (
                        results.multi_handedness[
                            hand_index
                        ].classification[0].label
                    )

                    # Track wrist position for hand identity stability
                    wrist = hand_landmarks.landmark[0]

                    wrist_x = int(wrist.x * w)
                    wrist_y = int(wrist.y * h)

                    previous_wrist_positions[hand_label] = [
                        wrist_x,
                        wrist_y
                    ]

                    # Keep only valid hand labels
                    if hand_label not in smooth_positions:
                        continue
                    # Draw hand skeleton
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    # Index fingertip
                    index_tip = hand_landmarks.landmark[8]

                    current_hand_points[hand_label] = (
                        smooth_x,
                        smooth_y
                    )

                    x = int(index_tip.x * w)
                    y = int(index_tip.y * h)

                    # Smooth pointer
                    previous_x, previous_y = (
                        smooth_positions[hand_label]
                    )

                    if previous_x == 0 and previous_y == 0:
                        smooth_x = x
                        smooth_y = y
                    else:
                        dx = x - previous_x
                        dy = y - previous_y

                        smooth_x = int(
                            previous_x + dx * smoothing
                        )

                        smooth_y = int(
                            previous_y + dy * smoothing
                        )

                    smooth_positions[hand_label] = [
                        smooth_x,
                        smooth_y
                    ]

                    current_hand_points[hand_label] = (
                        smooth_x,
                        smooth_y
                    )

                    x = smooth_x
                    y = smooth_y

                    # Keep pointer inside the camera frame
                    x = max(0, min(w - 1, x))
                    y = max(0, min(h - 1, y))

                    # --------------------------------
                    # Adaptive pinch detection
                    # --------------------------------

                    thumb_tip = hand_landmarks.landmark[4]
                    wrist = hand_landmarks.landmark[0]
                    middle_mcp = hand_landmarks.landmark[9]

                    pinch_distance = distance(
                        thumb_tip,
                        index_tip
                    )


                    hand_size = distance(
                        wrist,
                        middle_mcp
                    )

                    hand_size = max(
                        hand_size,
                        0.001
                    )

                    normalized_pinch = (
                        pinch_distance / hand_size
                    )

                    PINCH_START = 0.55
                    PINCH_RELEASE = 0.70

                    if pinch_frames[hand_label] > 0:

                        if normalized_pinch < PINCH_RELEASE:
                            pinch_frames[hand_label] += 1
                        else:
                            pinch_frames[hand_label] = 0

                    else:

                        if normalized_pinch < PINCH_START:
                            pinch_frames[hand_label] = 1

                    is_pinching = (
                        pinch_frames[hand_label]
                        >= required_frames
                    )

                    current_pinch_states[hand_label] = is_pinching

                    # --------------------------------
                    # Pointer
                    # --------------------------------

                    draw_reticle(
                        frame,
                        x,
                        y,
                        is_pinching,
                        hand_label
                    )

                    # --------------------------------
                    # Button interaction
                    # --------------------------------

                    inside_button = (
                        button_x1 <= x <= button_x2
                        and
                        button_y1 <= y <= button_y2
                    )

                    if inside_button and is_pinching:
                        button_selected = True

                    # Status
                    if is_pinching:

                        cv2.putText(
                            frame,
                            "PINCH",
                            (x + 20, y + 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 255),
                            2
                        )

                    else:

                        cv2.putText(
                            frame,
                            hand_label,
                            (x + 20, y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (255, 255, 255),
                            2
                        )

            # --------------------------------
            # OBJECT INTERACTION ENGINE
            # --------------------------------

            hand_count = len(current_hand_points)

            # ========================================
            # NO HANDS
            # ========================================

            if hand_count == 0:

                interaction_mode = "IDLE"

                object_grabbed = False
                grab_hand = None

                scale_active = False
                scale_start_distance = None
                scale_start_size = None


            # ========================================
            # ONE HAND
            # ========================================

            elif hand_count == 1:

                hand_label = next(iter(current_hand_points))

                hand_x, hand_y = current_hand_points[hand_label]

                is_pinching = current_pinch_states.get(
                    hand_label,
                    False
                )

                # --------------------------------
                # Pinch starts / continues
                # --------------------------------

                if is_pinching:

                    # If this is a NEW grab
                    if not object_grabbed:

                        object_grabbed = True
                        grab_hand = hand_label

                        grab_offset_x = object_x - hand_x
                        grab_offset_y = object_y - hand_y

                    # Move while holding pinch
                    if object_grabbed and grab_hand == hand_label:

                        interaction_mode = "MOVE"

                        object_x = int(
                            hand_x + grab_offset_x
                        )

                        object_y = int(
                            hand_y + grab_offset_y
                        )

                # --------------------------------
                # Pinch released
                # --------------------------------

                else:

                    interaction_mode = "IDLE"

                    object_grabbed = False
                    grab_hand = None


            # ========================================
            # TWO HANDS
            # ========================================

            elif hand_count == 2:

                left_x, left_y = current_hand_points["Left"]
                right_x, right_y = current_hand_points["Right"]

                left_pinching = current_pinch_states.get(
                    "Left",
                    False
                )

                right_pinching = current_pinch_states.get(
                    "Right",
                    False
                )

                # --------------------------------
                # Both hands pinching = SCALE
                # --------------------------------

                if left_pinching and right_pinching:

                    interaction_mode = "SCALE"

                    # Stop single-hand grab
                    object_grabbed = False
                    grab_hand = None

                    current_distance = math.sqrt(
                        (right_x - left_x) ** 2 +
                        (right_y - left_y) ** 2
                    )

                    # Start a NEW scale gesture
                    if not scale_active:

                        scale_active = True

                        scale_start_distance = max(
                            current_distance,
                            1
                        )

                        scale_start_size = object_size

                    # Calculate scale relative to gesture start
                    scale_ratio = (
                        current_distance /
                        scale_start_distance
                    )

                    new_size = int(
                        scale_start_size *
                        scale_ratio
                    )

                    object_size = max(
                        60,
                        min(400, new_size)
                    )

                # --------------------------------
                # Two hands visible but not both
                # pinching
                # --------------------------------

                else:

                    interaction_mode = "IDLE"

                    scale_active = False
                    scale_start_distance = None
                    scale_start_size = None

                    object_grabbed = False
                    grab_hand = None

           
            draw_test_object(
                frame,
                object_x,
                object_y,
                object_size
            )

            frame = draw_hud(frame)

            draw_panel(
                frame,
                30,
                80,
                280,
                180,
                "SYSTEM STATUS",
                [
                    "HAND TRACKING    ONLINE",
                    "GESTURE          ACTIVE",
                    "POINTER          ONLINE",
                    "INTERFACE        V1.4.3"
                ]
            )

            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

# GitHub auto-push test