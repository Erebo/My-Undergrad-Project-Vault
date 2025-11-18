<!-- PROJECT BANNER -->
<h1 align="center">🔥 Carbon Monoxide Monitoring & 7-Day Data Recording System 🔥</h1>

<p align="center">
  ESP32 • MQ-7 Sensor • Real-time CO Monitoring • Environmental Data Logging
</p>

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Platform-ESP32-blue" />
  <img src="https://img.shields.io/badge/Sensor-MQ--7-red" />
  <img src="https://img.shields.io/badge/Language-Arduino%20C%2B%2B-green" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---

## 📌 Overview
This project is a Carbon Monoxide (CO) monitoring system built using an MQ-7 gas sensor and an ESP32 microcontroller.  
It measures CO concentration in ppm and prepares for a continuous 7-day environmental data-logging session.

The system reads analog output from the MQ-7 sensor using the ESP32 ADC, converts it to ppm, and provides stable readings when powered at 5V.

---

## 🛠️ Features
- Real-time CO measurement (ppm)
- ESP32 + MQ-7 analog sensing
- Stable and accurate readings at 5V
- Ready for 7-day long-term CO data logging

---

## 🔌 Hardware Requirements
- ESP32
- MQ-7 CO Gas Sensor Module
- Breadboard
- Jumper wires
- (Optional) LED indicators

---

## 🔧 Hardware Setup
Connections:

- MQ-7 VCC → ESP32 5V  
- MQ-7 GND → ESP32 GND  
- MQ-7 AO  → ESP32 GPIO34 (ADC input)

⚠️ Important: The MQ-7 must be powered at **5V** for correct ppm output.

---

## 📜 Code
Upload your ESP32 program that:
- Reads ADC values from MQ-7  
- Converts ADC reading to ppm  
- Prints ppm values using Serial Monitor  

(Place your code in a folder called **/firmware**)

---

## ▶️ How to Run
1. Connect ESP32 to your computer  
2. Upload code using Arduino IDE or PlatformIO  
3. Open Serial Monitor  
4. View CO concentration in ppm  

---

## 📂 Recommended Repository Structure
README.md
/firmware
(ESP32 source code)
/hardware
circuit_diagram.png
/docs
Project Progress Report.pdf
/data
(7-day CO recordings)

---

## 📄 Documentation
The full academic progress report is included in the **/docs** folder:  
**Project Progress Report (Group 01, 68_A1).pdf**

---

## 📌 Project Status
- Hardware tested and fully functional  
- CO readings stable between **4–6 ppm**  
- Ready for the 7-day continuous CO monitoring phase  

---

## 🏁 License
MIT License.

---

