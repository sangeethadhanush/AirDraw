# ✋ AirDraw – AI-Based Air Drawing System

## 📌 Project Overview

**AirDraw** is an AI-based touchless drawing system that allows users to draw on a virtual canvas using their hand gestures.

The system uses a webcam to capture the user's hand movements and **MediaPipe Hand Landmarker** to detect and track hand landmarks in real time. When only the index finger is raised, the system enters drawing mode and follows the movement of the fingertip to create a virtual drawing on the screen.

This project demonstrates how **Computer Vision, Hand Gesture Recognition, and Human-Computer Interaction** can be combined to create a touchless drawing experience.

---

## ✨ Features

- ✋ Real-time hand tracking
- ☝️ Index-finger gesture-based drawing
- 🖥️ Touchless interaction using a webcam
- 🎨 Virtual drawing canvas
- 🎯 Smooth finger movement tracking
- 🚫 Jitter reduction for stable drawing
- 🧹 Clear the canvas using the `C` key
- ❌ Exit the application using the `Q` key

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **Computer Vision**
- **Hand Gesture Recognition**

---

## ⚙️ How It Works

The system follows these steps:

```text
Webcam
   ↓
Capture Video
   ↓
Hand Detection
   ↓
Hand Landmark Tracking
   ↓
Finger Gesture Recognition
   ↓
Index Finger Position Detection
   ↓
Virtual Canvas
   ↓
Air Drawing
