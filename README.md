# InteractAI: Real-Time Gesture-Based Human-Computer Interaction System 🤖✋

Welcome to **InteractAI**, a real-time gesture recognition system that lets you control your computer using hand gestures! Built with Python, OpenCV, and MediaPipe, this project enables seamless device interaction through intuitive gestures—think clicking, scrolling, or zooming with just a wave of your hand. Whether you’re enhancing accessibility or exploring the future of human-computer interaction, InteractAI is a step toward making technology more natural and inclusive.

I developed this project as part of my B.Tech in Computer Science and Engineering at Karunya Institute of Technology and Sciences, and I’m excited to share it with the community! Check out the details below to get started.

---

## 📖 Project Overview

InteractAI uses computer vision to detect and interpret hand gestures in real-time, mapping them to actions like mouse control, scrolling, zooming, and window management. It’s designed to enhance accessibility and provide an intuitive way to interact with devices, with potential applications in gaming, virtual reality, and assistive technology.

### Key Features
- **Gesture-Based Control**: Perform actions like left/right clicks, scrolling, volume adjustment, and window management using hand gestures.
- **Real-Time Performance**: Optimized for low latency using MediaPipe’s hand tracking.
- **Dual-Hand Support**: Right hand for mouse and volume control, left hand for window management and zooming.
- **Accessibility Focus**: Makes technology more accessible for users with limited mobility.
- **Presented at Karunya Innovation Event**: Received positive feedback for its innovative approach.

---

## 🚀 Getting Started

Follow the steps below to set up and run InteractAI on your machine.

### Prerequisites

#### Hardware Requirements
- **Webcam**: A working webcam is required for real-time hand tracking.
- **System**: Windows, macOS, or Linux (tested on Windows 10/11).

#### Software Requirements
- **Python**: Version 3.8 or higher (MediaPipe has specific compatibility requirements).
- **Libraries**:
  - `opencv-python` (for image processing and webcam access)
  - `mediapipe` (for hand tracking)
  - `numpy` (for numerical operations)
  - `pyautogui` (for system control like mouse and keyboard actions)

#### Python Environment Setup
To ensure compatibility with MediaPipe, follow these steps to set up your Python environment:

1. **Install Python**:
   - Download and install Python 3.8 or 3.9 from [python.org](https://www.python.org/downloads/). Avoid using Python 3.10+ as MediaPipe may have compatibility issues with newer versions.
   - Verify the installation:
     ```bash
     python --version
     ```

2. **Create a Virtual Environment** (recommended):
   - Create a virtual environment to isolate dependencies:
     ```bash
     python -m venv interactai_env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       interactai_env\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source interactai_env/bin/activate
       ```

3. **Install Required Libraries**:
   - With the virtual environment activated, install the necessary packages:
     ```bash
     pip install opencv-python mediapipe numpy pyautogui
     ```
   - Verify the installations:
     ```bash
     pip list
     ```
     You should see `opencv-python`, `mediapipe`, `numpy`, and `pyautogui` listed.

4. **MediaPipe-Specific Notes**:
   - MediaPipe requires a compatible Python version (3.8–3.9 recommended). If you encounter issues, ensure your Python version aligns with MediaPipe’s requirements.
   - On some systems, you may need to install additional dependencies for OpenCV (e.g., `libGL` on Linux):
     ```bash
     sudo apt-get install libgl1-mesa-glx
     ```

---

## 🛠️ Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jinto-joseph/interactai.git
   cd interactai
