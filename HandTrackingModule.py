import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, detectionCon=0.7, trackCon=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=detectionCon, min_tracking_confidence=trackCon
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """Processes the image and finds hands."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def find_position(self, img):
        """Returns a list of landmarks [[id, x, y], ...]"""
        lm_list = []
        if self.results.multi_hand_landmarks:
            # We assume 1 hand for simplicity
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def get_fingers_up(self, lm_list):
        """Returns which fingers are up [1, 0, 1, 1, 0]"""
        fingers = []
        if len(lm_list) == 0:
            return fingers

        # 1. Thumb (Improved Logic)
        # We check if the thumb tip (4) is to the left/right of the knuckle (3)
        # This assumes Right Hand. If you use Left Hand, this needs flipping.
        if lm_list[4][1] < lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2. Other 4 Fingers (Index, Middle, Ring, Pinky)
        # We check if the Tip (y) is higher than the PIP joint (y)
        # Remember: In screen coordinates, "Up" means a Lower Y value.
        tip_ids = [8, 12, 16, 20]
        for id in tip_ids:
            if lm_list[id][2] < lm_list[id - 2][2]:  # Tip < Pip
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
