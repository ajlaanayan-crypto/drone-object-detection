from ultralytics import YOLO
import cv2
import sys
import os
import platform

def open_camera():
    """Try to open camera with macOS AVFoundation backend first, then fallback."""
    is_mac = platform.system() == "Darwin"

    # On macOS, try AVFoundation backend explicitly for better compatibility
    if is_mac:
        backends = [
            (0, cv2.CAP_AVFOUNDATION),
            (0, cv2.CAP_ANY),
            (1, cv2.CAP_AVFOUNDATION),
        ]
    else:
        backends = [
            (0, cv2.CAP_ANY),
            (1, cv2.CAP_ANY),
        ]

    for idx, backend in backends:
        cap = cv2.VideoCapture(idx, backend)
        if cap.isOpened():
            # Warm up: try reading a frame to confirm it actually works
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            ret, _ = cap.read()
            if ret:
                backend_name = "AVFoundation" if backend == cv2.CAP_AVFOUNDATION else "default"
                print(f"Camera opened: index={idx}, backend={backend_name}")
                return cap
            cap.release()

    return None


def main():
    """Real-time object detection using YOLOv8 — macOS compatible."""

    # Resolve model path relative to this file's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    model_path = os.path.join(project_root, "models", "yolov8s.pt")
    model_path = os.path.normpath(model_path)

    # Load YOLOv8 model (auto-downloads if missing)
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # Open camera with macOS-compatible approach
    print("Opening camera...")
    cap = open_camera()

    if cap is None:
        print("Error: Cannot access camera.")
        if platform.system() == "Darwin":
            print("\nmacOS Troubleshooting:")
            print("  1. Go to System Settings → Privacy & Security → Camera")
            print("  2. Enable camera access for Terminal / iTerm2")
            print("  3. Restart your terminal and try again")
        sys.exit(1)

    print("Starting real-time object detection. Press 'q' to quit.")

    window_title = "YOLOv8 Object Detection"

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame — camera may have disconnected.")
                break

            # Run YOLO inference
            results = model(frame, verbose=False)

            # Draw bounding boxes + labels on frame
            annotated_frame = results[0].plot()

            # Show the annotated frame
            cv2.imshow(window_title, annotated_frame)

            # Quit on 'q' key
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                print("Quitting...")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
