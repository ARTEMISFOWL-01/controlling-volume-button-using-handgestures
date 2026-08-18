# 🎙️ Hand Gesture Volume Control

Control your computer's volume using **hand gestures** detected via **OpenCV** and **MediaPipe**. Point your thumb and index finger, and the distance between them controls the volume level in real-time.

## 📋 Project Overview

This project uses computer vision to detect hand landmarks and convert hand gestures into volume control commands. By measuring the distance between your thumb and index finger, you can adjust system volume intuitively without touching your keyboard or mouse.

### How It Works
```
Hand Detection (MediaPipe)
        ↓
Detect Landmarks (Thumb & Index)
        ↓
Calculate Distance
        ↓
Map to Volume Level
        ↓
Set System Volume (pycaw)
```

## ✨ Key Features

- 🤚 **Hand Gesture Recognition**: Detect hand position and landmarks in real-time
- 📏 **Distance Measurement**: Calculate distance between thumb and index finger
- 🔊 **Volume Control**: Map gesture distance to volume levels (0-100%)
- 📹 **Live Video Feed**: Real-time camera capture and processing
- 📊 **Visual Feedback**: Volume bar display on screen
- ⚡ **Low Latency**: Real-time response to hand movements
- 💻 **Cross-Platform**: Works on Windows with pycaw
- 🎯 **Accurate Detection**: MediaPipe's robust hand detection

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Hand Detection** | MediaPipe |
| **Computer Vision** | OpenCV |
| **Volume Control** | pycaw, comtypes |
| **Math** | NumPy, math |
| **Language** | Python 3.8+ |

## 📦 Dependencies

```
opencv-python>=4.5.0
mediapipe>=0.8.9
pycaw>=20211226
comtypes>=1.1.10
numpy>=1.20.0
```

## ⚙️ Installation

### Windows Installation

```bash
# Clone the repository
git clone https://github.com/ARTEMISFOWL-01/controlling-volume-button-using-handgestures.git
cd controlling-volume-button-using-handgestures

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install opencv-python mediapipe pycaw comtypes numpy

# Run the application
python volumecontrol.py
```

**Note**: pycaw works on Windows. For macOS/Linux, you may need alternative libraries like `pyaudio` or `alsaaudio`.

## 🎮 Usage

1. **Start the Application**
   ```bash
   python volumecontrol.py
   ```

2. **Position Your Hand**
   - Face your camera
   - Show your hand in the frame
   - MediaPipe will detect your hand landmarks

3. **Control Volume**
   - **Close Hand**: Bring thumb and index finger together → **Minimum Volume**
   - **Open Hand**: Separate thumb and index finger → **Maximum Volume**
   - The distance controls the volume level smoothly

4. **Visual Feedback**
   - Volume percentage displayed on screen (0-100%)
   - Volume bar shown on the left side
   - FPS counter for performance monitoring

5. **Exit**
   - Press `Esc` or close the window

## 🧠 How It Works

### Hand Detection
```python
detector = hm.handDetector(detectionCon=0.7)
# detectionCon: Confidence threshold (0.7 = 70%)
```

### Hand Landmarks
MediaPipe detects 21 key points on the hand:
```
Landmark Map:
- 0: Wrist
- 4: Thumb tip
- 8: Index finger tip
- 12: Middle finger tip
- 16: Ring finger tip
- 20: Pinky finger tip
(and others)
```

### Distance Calculation
```python
# Get thumb (landmark 4) and index (landmark 8) positions
x1, y1 = lmlist[4][1], lmlist[4][2]  # Thumb
x2, y2 = lmlist[8][1], lmlist[8][2]  # Index

# Calculate Euclidean distance
distance = math.hypot((x2 - x1), (y2 - y1))

# Map distance to volume (-65.25 to 0 dB)
volume = np.interp(distance, [20, 350], [-65.25, 0])

# Map distance to volume bar height (400 to 150 pixels)
volbar = np.interp(distance, [20, 350], [400, 150])

# Map distance to percentage (0 to 100%)
percentage = np.interp(distance, [20, 350], [0, 100])
```

### Volume Mapping
- **Distance 0-20 pixels**: Minimum volume (-65.25 dB)
- **Distance 20-350 pixels**: Progressive volume increase
- **Distance 350+ pixels**: Maximum volume (0 dB)

### System Volume Control
```python
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Get speaker device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Set master volume level
volume.SetMasterVolumeLevel(volume_level, None)
```

## 📊 Key Variables

| Variable | Purpose | Range |
|----------|---------|-------|
| `distance` | Thumb-to-index distance | 0-500 pixels |
| `vol` | Volume in dB | -65.25 to 0 |
| `volbar` | Volume bar position | 150-400 pixels |
| `volp` | Volume percentage | 0-100% |
| `fps` | Frames per second | Varies |

## 🎨 Visual Elements

- **Green Circle**: Indicates hand closure (distance < 20)
- **Purple Circles**: Thumb and index finger positions
- **Volume Bar**: Left-side rectangle showing current volume level
- **Filled Bar**: Displays volume percentage visually
- **FPS Counter**: Top-left corner shows real-time performance

## 🔧 Customization

### Adjust Detection Confidence
```python
detector = hm.handDetector(detectionCon=0.7)
# Increase to be more strict (0.9), decrease to be lenient (0.5)
```

### Modify Distance Range
```python
# Change the mapping range (currently [20, 350])
vol = np.interp(dis, [min_dist, max_dist], [-65.25, 0])
```

### Change Volume Range (dB)
```python
# Windows volume range: -65.25 to 0 dB
# Adjust these values for different systems
vol = np.interp(dis, [20, 350], [your_min, your_max])
```

### Adjust Camera Resolution
```python
cap.set(3, 1000)  # Width: 1000 pixels
cap.set(4, 1000)  # Height: 1000 pixels
```

## 📁 Project Files

- **volumecontrol.py** - Main application with volume control logic
- **hNDMODULE.py** - Hand detection module (custom MediaPipe wrapper)
- **README.md** - This file

## 🎓 Learning Concepts

This project demonstrates:
- **Hand Pose Estimation**: MediaPipe hand detection
- **Real-time Video Processing**: OpenCV streaming
- **Landmark Detection**: Extracting hand keypoints
- **Distance Calculation**: Euclidean distance formula
- **Data Mapping**: Interpolation for smooth control
- **System Integration**: Controlling OS-level audio
- **Computer Vision Pipeline**: From capture to control

## 💡 Potential Improvements

- [ ] Add gesture recognition for different commands (mute, pause, etc.)
- [ ] Support for both hands
- [ ] Add brightness control using palm orientation
- [ ] Implement smoothing for jitter reduction
- [ ] Add on-screen menu for settings
- [ ] Multi-gesture support (pinch, open palm, etc.)
- [ ] Save gesture profiles/presets
- [ ] Add voice feedback
- [ ] Cross-platform support (macOS, Linux)
- [ ] Calibration UI for different users

## 🚀 Advanced Features

### Add Mute Gesture
```python
# Close fist (all fingers together) = Mute
if distance < 30:
    volume.Mute(True)
```

### Add Pause Gesture
```python
# Palm facing camera = Pause music
# Requires additional pose detection
```

### Smoothing Filter
```python
from collections import deque

# Apply exponential moving average
history = deque(maxlen=5)
smooth_distance = sum(history) / len(history)
```

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Hand not detected | Ensure good lighting, stable hand position |
| Jerky volume changes | Add smoothing filter or increase detection confidence |
| Low FPS | Reduce camera resolution or optimize processing |
| pycaw errors | Ensure running on Windows, check audio device |
| Delayed response | Reduce image size or increase detection confidence |

## 🔒 Performance Optimization

- **Resolution**: 1000×1000 (can be reduced for faster processing)
- **Frame Rate**: Depends on hardware (30-60 FPS typical)
- **Detection Confidence**: 0.7 (balance between accuracy and speed)
- **Landmark Count**: 21 (MediaPipe hand model)

## 📞 Common Issues

**Issue**: "No module named 'pycaw'"
```bash
# Solution: Install pycaw
pip install pycaw
```

**Issue**: Hand detection is slow
```python
# Solution: Reduce resolution
cap.set(3, 640)  # Lower from 1000
cap.set(4, 480)
```

**Issue**: Volume doesn't change
```python
# Solution: Check volume device and range
print(volume.GetVolumeRange())  # See available range
```

## 🎮 Use Cases

- 🎵 **Music Control**: Adjust volume without touching device
- 🎮 **Gaming**: Hands-free audio adjustment
- 🎙️ **Presentations**: Control audio during presentations
- 👨‍💻 **Accessibility**: Hand gesture-based control for accessibility needs
- 📺 **Home Automation**: Gesture control for smart home systems

## 📊 System Requirements

- **OS**: Windows 10/11 (primary), macOS/Linux (with modifications)
- **Python**: 3.8+
- **Webcam**: USB camera or built-in
- **RAM**: 2GB minimum
- **CPU**: Modern processor recommended
- **GPU**: Optional (CPU processing is fast enough)

## 🎓 Educational Value

Great for learning:
- Computer vision fundamentals
- Real-time hand pose estimation
- Gesture recognition basics
- System API integration
- Video processing pipelines

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

**ARTEMISFOWL-01**

---

**Pro Tip**: For best results, use in well-lit environments with a neutral background!
