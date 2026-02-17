import cv2


def draw_header(img, mode):
    """Draws the top bar with the current mode."""
    h, w, _ = img.shape

    # Draw dark header background
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (40, 40, 40), -1)
    alpha = 0.7
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # Draw Mode Text
    color = (0, 255, 0) if mode == "MOUSE" else (0, 255, 255)
    cv2.putText(img, f"MODE: {mode}", (30, 55), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

    # Instructions
    cv2.putText(
        img,
        "Press 'M' to Switch",
        (w - 350, 55),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (200, 200, 200),
        2,
    )


def draw_translation_box(img, text):
    """Draws the bottom text box for sign language."""
    h, w, _ = img.shape

    # White background box
    cv2.rectangle(img, (50, h - 120), (w - 50, h - 30), (255, 255, 255), -1)
    cv2.rectangle(img, (50, h - 120), (w - 50, h - 30), (0, 0, 0), 2)

    # The Text
    cv2.putText(
        img, f"Sign: {text}", (70, h - 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
    )


def draw_mouse_box(img, frameR):
    """Draws the purple boundary box for mouse movement."""
    h, w, _ = img.shape
    cv2.rectangle(img, (frameR, frameR), (w - frameR, h - frameR), (255, 0, 255), 2)
