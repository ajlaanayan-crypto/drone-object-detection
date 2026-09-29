# Drone Object Detection System

Real-time object detection for autonomous drones using YOLOv8, optimized for Raspberry Pi 4B deployment.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a real-time object detection system designed for autonomous drone applications. Using the lightweight YOLOv8 nano model and OpenCV, it can detect and track 80 different object classes in real-time on resource-constrained devices like the Raspberry Pi 4B.

**Key Use Cases:**
- Autonomous drone navigation
- Object tracking and surveillance
- Search and rescue operations
- Agricultural monitoring
- Wildlife detection

## ✨ Features

- ⚡ Real-time object detection using YOLOv8n (nano model)
- 🎯 80 pre-trained object classes (COCO dataset)
- 🚁 Optimized for Raspberry Pi 4B (4GB RAM)
- 📹 Support for webcam and Raspberry Pi Camera Module
- 🔧 Fast dependency management with `uv` package manager
- 📦 Clean, modular package structure
- 🐧 Linux-optimized (tested on Fedora)

## 📦 Prerequisites

### Hardware Requirements
- **Development**: Laptop/PC with webcam
- **Deployment**: Raspberry Pi 4B (4GB RAM) with Camera Module
- **Camera**: USB webcam or Pi Camera Module v2/v3

### Software Requirements
- **OS**: Fedora Linux (or other Linux distributions)
- **Python**: 3.8 or higher
- **uv**: Fast Python package manager

## 🚀 Installation

### Step 1: Install uv Package Manager

**On Fedora:**
```

sudo dnf install -y uv

```

**Alternative (standalone installer):**
```

curl -LsSf https://astral.sh/uv/install.sh | sh

```

**Verify installation:**
```

uv --version

```

### Step 2: Install System Dependencies (Fedora)

Install OpenCV system libraries:
```

sudo dnf install -y python3-devel gcc gcc-c++ cmake
sudo dnf install -y gtk3-devel libpng-devel libjpeg-devel libtiff-devel
sudo dnf install -y ffmpeg-free-devel mesa-libGL mesa-libGL-devel

```

### Step 3: Clone Repository

```

cd ~/Documents/Projects
git clone <your-repository-url> Object-Detection
cd Object-Detection

```

### Step 4: Install Python Dependencies

```

uv sync

```

This command will:
- Create a virtual environment in `.venv/`
- Install all project dependencies
- Generate a lockfile (`uv.lock`) for reproducibility

## 📁 Project Structure

```

Object-Detection/
├── .python-version          \# Python version specification
├── .gitignore              \# Git ignore file
├── README.md              \# This documentation
├── pyproject.toml        \# Project configuration \& dependencies
├── uv.lock              \# Dependency lockfile
├── .venv/              \# Virtual environment (auto-generated)
│
├── src/
│   └── detector/
│       ├── __init__.py
│       └── detect.py   \# Main detection script
│
├── models/            \# Model weights (auto-downloaded)
│   └── yolov8n.pt    \# YOLOv8 nano model
│
└── data/             \# Test images and videos
├── images/
└── videos/

```

## 💻 Usage

### Testing on Laptop

Run the detection script with your laptop's webcam:

```

uv run python -m detector.detect

```

**Alternative method (activate virtual environment first):**
```

source .venv/bin/activate
python -m detector.detect

```

### Deploying on Raspberry Pi

1. **Transfer project to Raspberry Pi:**
```

scp -r Object-Detection/ pi@raspberrypi.local:~/

```

2. **SSH into Raspberry Pi:**
```

ssh pi@raspberrypi.local

```

3. **Install dependencies:**
```

cd Object-Detection
uv sync

```

4. **Run detection:**
```

uv run python -m detector.detect

```

### Controls

- Press **'q'** to quit the detection window
- The YOLOv8n model (~6MB) will auto-download on first run

## ⚙️ Configuration

### pyproject.toml

Main configuration file defining:

```

[project]
name = "drone-object-detection"
version = "0.1.0"
description = "Real-time object detection for autonomous drones"
requires-python = ">=3.8"
dependencies = [
"ultralytics>=8.0.0",
"opencv-python>=4.8.0",
"numpy>=1.24.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/detector"]

```

### Camera Settings

Edit `src/detector/detect.py` to adjust camera settings:

```


# Change camera index (0 for default, 1 for external)

cap = cv2.VideoCapture(0)

# Adjust confidence threshold

results = model(frame, conf=0.5)  \# Default is 0.25

# Change input resolution

model = YOLO('yolov8n.pt', imgsz=416)  \# Default is 640

```

## 📊 Performance

### Model Specifications

| Parameter | Value |
|-----------|-------|
| Model | YOLOv8 Nano |
| Size | ~6 MB |
| Parameters | 3.2M |
| FPS (Laptop) | 30-60 FPS |
| FPS (RPi 4B) | 8-10 FPS |
| Accuracy (mAP) | ~37% (COCO) |
| Classes | 80 objects |

### Detected Object Classes

person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

## 🛠️ Troubleshooting

### Camera Permission Issues (Fedora)

```


# Add user to video group

sudo usermod -a -G video \$USER

# Log out and log back in

```

### OpenCV Display Problems

```


# Install additional libraries

sudo dnf install -y libxcb libXext libSM libICE

```

### Camera Not Detected

```


# List available cameras

ls -l /dev/video*

# Test camera

ffplay /dev/video0

```

### Build Errors

Ensure `pyproject.toml` contains:
```

[tool.hatch.build.targets.wheel]
packages = ["src/detector"]

```

### Slow Performance on Raspberry Pi

- Lower input resolution: `imgsz=320`
- Increase confidence threshold: `conf=0.6`
- Use quantized model (INT8)
- Disable verbose output: `verbose=False`

## 🔧 Development

### Adding Dependencies

```

uv add package-name

```

### Removing Dependencies

```

uv remove package-name

```

### Updating Dependencies

```

uv lock --upgrade
uv sync

```

### Adding Development Tools

```

uv add --dev pytest black ruff mypy

```

### Running Tests

```

uv run pytest

```

### Code Formatting

```

uv run black src/
uv run ruff check src/

```

## 🚀 Future Enhancements

- [ ] Custom model training for specific objects
- [ ] Integration with drone flight controller (MAVLink)
- [ ] GPS tagging of detected objects
- [ ] Multi-camera support
- [ ] Real-time video streaming to ground station
- [ ] Automatic target tracking and following
- [ ] Object counting and analytics
- [ ] Night vision/infrared camera support
- [ ] Edge TPU acceleration
- [ ] Web dashboard for monitoring

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📚 References

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [OpenCV Python](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [Raspberry Pi Camera](https://www.raspberrypi.com/documentation/accessories/camera.html)

## 📄 License

[Specify your license - e.g., MIT, Apache 2.0]

## 👨‍💻 Authors

[Your name/team]

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8
- **Astral** for the uv package manager
- **OpenCV** community
- **Raspberry Pi Foundation**

## 📞 Contact

For questions or support, please open an issue or contact [your-email@example.com]

---

**Note**: This project is optimized for educational and research purposes. For production drone deployments, ensure compliance with local regulations and safety standards.
```

This comprehensive README includes all necessary information for setting up and using your drone object detection project with the package structure (Option 2), includes Fedora-specific instructions, troubleshooting guides, performance metrics, and follows best practices for technical documentation.[^1][^3]
<span style="display:none">[^2][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.com/nia194/Object-Detection

[^2]: https://www.studocu.com/row/document/jomo-kenyatta-university-of-agriculture-and-technology/computer-technology/object-detection-from-drone-for-surveillance-readmemd-at-main-andyokuba-object-detection-from-drone-for-surveillance/84728663

[^3]: https://github.com/VijayRajIITP/Drone-Detection-and-Tracking

[^4]: https://universe.roboflow.com/muhammad-ahmad-rpdsk/drone-detection-vh4ix

[^5]: https://discuss.ardupilot.org/t/quadcopter-object-tracking-on-a-budget/18147

[^6]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11821834/

[^7]: https://www.kaggle.com/datasets/redzapdos123/vsai-dataset-yolo11-obb-format

[^8]: https://huggingface.co/StephanST/WALDO30/blame/a79e852017256ec64d543360be2b03837640b1b8/README.md

[^9]: https://gitlab.utu.fi/drone-warehouse/beam_defect_detection
