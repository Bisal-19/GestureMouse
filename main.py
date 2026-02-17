import cv2
import pyautogui
import numpy as np
import math
import HandTrackingModule as htm
import UI
import Signs

# --- SAFETY SETTING ---
pyautogui.FAILSAFE = False

# --- GLOBAL VARIABLES ---
cap = None
detector = None
W_CAM, H_CAM = 640, 480
frameR = 100
bottom_margin = 220
smoothening = 7
CLICK_DIST = 30
RIGHT_CLICK_DIST = 45


def initialize_camera():
    global cap, detector
    cap = cv2.VideoCapture(0)
    cap.set(3, W_CAM)
    cap.set(4, H_CAM)
    detector = htm.HandDetector(detectionCon=0.7)
    return True


def start_app(start_mode="MOUSE"):
    global cap, detector

    if cap is None or detector is None:
        initialize_camera()

    screen_w, screen_h = pyautogui.size()
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # State Variables
    dragging = False
    right_clicked = False
    show_camera = True  # Toggle for Hiding Camera
    mode = start_mode

    # --- FIX: LOCK WINDOW SIZE ---
    # This prevents the user from resizing/maximizing and freezing the app
    cv2.namedWindow("AI Mouse Controller", cv2.WINDOW_AUTOSIZE)

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)

        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        # Only draw UI if camera is shown
        if show_camera:
            UI.draw_header(img, mode)

        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]
            x_thumb, y_thumb = lm_list[4][1:]

            fingers = detector.get_fingers_up(lm_list)

            if mode == "MOUSE":
                if show_camera:
                    cv2.rectangle(
                        img,
                        (frameR, frameR),
                        (W_CAM - frameR, H_CAM - bottom_margin),
                        (255, 0, 255),
                        2,
                    )

                # --- A. Moving ---
                if fingers[1] == 1 and fingers[2] == 0:
                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                    x3 = np.interp(x1, (frameR, W_CAM - frameR), (0, screen_w))
                    y3 = np.interp(y1, (frameR, H_CAM - bottom_margin), (0, screen_h))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY
                    if show_camera:
                        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

                # --- B. Left Click / Drag ---
                if fingers[1] == 1 and fingers[2] == 1:
                    length = math.hypot(x2 - x1, y2 - y1)
                    if show_camera:
                        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    if length < CLICK_DIST:
                        if show_camera:
                            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

                        if not dragging:
                            pyautogui.mouseDown()
                            dragging = True

                        x3 = np.interp(x1, (frameR, W_CAM - frameR), (0, screen_w))
                        y3 = np.interp(
                            y1, (frameR, H_CAM - bottom_margin), (0, screen_h)
                        )

                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        pyautogui.moveTo(clocX, clocY)
                        plocX, plocY = clocX, clocY

                    else:
                        if dragging:
                            pyautogui.mouseUp()
                            dragging = False

                # --- C. Right Click ---
                if fingers[2] == 0:
                    dist_thumb = math.hypot(x1 - x_thumb, y1 - y_thumb)
                    if show_camera and dist_thumb < 100:
                        cv2.line(img, (x1, y1), (x_thumb, y_thumb), (0, 255, 255), 2)

                    if dist_thumb < RIGHT_CLICK_DIST:
                        if show_camera:
                            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                        if not right_clicked:
                            pyautogui.rightClick()
                            right_clicked = True
                            if show_camera:
                                cv2.putText(
                                    img,
                                    "RIGHT CLICK",
                                    (50, 50),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2,
                                    (0, 0, 255),
                                    2,
                                )
                    else:
                        right_clicked = False

                # --- D. Scrolling ---
                if fingers[4] == 1:
                    if y1 < H_CAM // 2:
                        if show_camera:
                            cv2.putText(
                                img,
                                "SCROLL UP",
                                (20, 100),
                                cv2.FONT_HERSHEY_PLAIN,
                                2,
                                (0, 0, 255),
                                2,
                            )
                        pyautogui.scroll(300)
                    else:
                        if show_camera:
                            cv2.putText(
                                img,
                                "SCROLL DOWN",
                                (20, 100),
                                cv2.FONT_HERSHEY_PLAIN,
                                2,
                                (0, 0, 255),
                                2,
                            )
                        pyautogui.scroll(-300)

            elif mode == "TRANSLATE":
                meaning = Signs.get_meaning(fingers)
                if show_camera:
                    UI.draw_translation_box(img, meaning)

        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # --- DRAWING LOGIC ---
        if show_camera:
            cv2.imshow("AI Mouse Controller", img)
        else:
            # If hidden, we show a tiny 1x1 pixel window to keep the loop running
            # This prevents the "Minimize Freeze"
            cv2.imshow("AI Mouse Controller", np.zeros((1, 1, 3), dtype=np.uint8))

        key = cv2.waitKey(1)
        if key == ord("q"):
            if dragging:
                pyautogui.mouseUp()
            break
        if key == ord("m"):
            mode = "TRANSLATE" if mode == "MOUSE" else "MOUSE"
        if key == ord("h"):  # Toggle Hide/Show
            show_camera = not show_camera
            if show_camera:
                # Restore window size when showing again
                cv2.resizeWindow("AI Mouse Controller", W_CAM, H_CAM)

    cap.release()
    cv2.destroyAllWindows()
