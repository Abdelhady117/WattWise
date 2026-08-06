<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/46f13c0e-c43a-4f0f-a585-fb1f60a65a8d" /># ⚡ WattWise

<h3 align="center">An IoT-Based Home Energy Management System</h3>

<p align="center">
Monitor • Analyze • Optimize
</p>

![NTI](https://img.shields.io/badge/NTI-IoT%20Training-blue)
![ESP32](https://img.shields.io/badge/ESP32-IoT-blue?logo=espressif&logoColor=red)
![MicroPython](https://img.shields.io/badge/MicroPython-1.28-2B2728?logo=micropython&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Protocol-660066?logo=eclipsemosquitto&logoColor=white)
![Node-RED](https://img.shields.io/badge/Node--RED-Dashboard-8F0000?logo=nodered&logoColor=white)
![Wokwi](https://img.shields.io/badge/Wokwi-Simulation-0096FF?logo=wokwi&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-success?logo=opensourceinitiative&logoColor=green)

---

## 📖 Overview

**WattWise** is an IoT-based Home Energy Management System developed as part of the **National Telecommunication Institute (NTI) IoT Training Program**.

The system continuously monitors household electrical parameters using ESP32-based Smart Monitoring Nodes. It collects voltage, current, power, and energy consumption data, transmits them through MQTT, and visualizes them on an interactive Node-RED dashboard.

Beyond monitoring, WattWise aims to help users make smarter energy decisions by providing notifications, warnings, and energy-saving recommendations while considering the Egyptian prepaid electricity tariff system.

---

## ✨ Features

### ⚡ Real-Time Monitoring

* Live voltage monitoring
* Live current monitoring
* Real-time power calculation
* Power factor calculation
* Peak power monitoring
* OLED live display

### 📊 Energy Analytics

* Energy consumption (kWh)
* Estimated electricity cost
* Estimated CO₂ emissions
* Historical monitoring
* Peak power tracking

### 🚨 Smart Notifications

* Overload detection
* Relay protection
* High current alerts
* System status monitoring

### 💡 Energy Advisor

* Energy-saving recommendations
* Electricity tariff awareness
* Consumption insights
* Usage warnings

### 🌐 IoT Connectivity

* ESP32
* MQTT Communication
* Node-RED Dashboard
* Wokwi Simulation

---

## 🏗 System Architecture

<p align="center">
  <img src="assets/images/system-architecture.png" alt="System Architecture" width="900">
</p>

The system consists of:

* **ESP32** as the main controller.
* **Voltage and current sensors** for electrical measurements.
* **MQTT** for real-time communication.
* **Node-RED Dashboard** for visualization.
* **OLED displays** for local monitoring.
* **Relay and buzzer** for protection and alerts.

---

## 🔌 Hardware Components

* ESP32 Development Board
* Voltage Sensor
* Current Sensor
* Relay Module
* OLED Display
* Buzzer
* Status LEDs
* Potentiometers (simulation inputs)

---

## 💻 Software Stack

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| MicroPython  | ESP32 Firmware            |
| MQTT         | IoT Communication         |
| Node-RED     | Dashboard & Visualization |
| Wokwi        | Hardware Simulation       |
| Git & GitHub | Version Control           |

---

## 📂 Repository Structure

```text
WattWise/
│
├── README.md
├── AUTHORS.md
│
├── dashboard/
│   ├── dashboard1.
│   └── WattWise_Presentation.pptx
│
├── docs/
│   ├── WattWise_Report.pdf
│   └── WattWise_Presentation.pptx
│
├── wokwi/
│   ├── main.py
│   ├── diagram.json
│   ├── ssd1306.py
│   └── wokwi.jpeg
│
├── dashboard/
│   ├── node-red-flow.json
│   └── screenshots/
│
└── assets/
    ├── logo/
    ├── images/
    └── demo/
```

---

## 🖥 Dashboard

The Node-RED dashboard provides:

* Live electrical measurements
* Voltage, current and power visualization
* Energy consumption monitoring
* Estimated electricity cost
* System status
* Notifications
* Energy Advisor recommendations

<p align="center">
  <img src="assets/images/dashboard-home.png" alt="Dashboard" width="900">
</p>

---

## 🔬 Wokwi Simulation

The complete ESP32 simulation is available in the repository.

**Simulation Link**

> *(Insert your Wokwi project link here.)*

<p align="center">
  <img src="assets/images/wokwi-simulation.png" alt="Wokwi Simulation" width="900">
</p>

---

## 📄 Documentation

Complete project documentation can be found in the **docs** folder.

Included documents:

* Project Report
* Project Presentation

---

## 🚀 Future Improvements

Planned enhancements include:

* Mobile application
* AI-based energy recommendations
* Appliance-level anomaly detection
* Smart meter integration
* Renewable energy monitoring
* Cloud connectivity
* Multi-home management
* Predictive energy analytics

---

## 👥 Team

The complete list of contributors is available in **AUTHORS.md**.

---

## 📜 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

## 🙏 Acknowledgements

This project was developed as part of the **National Telecommunication Institute (NTI) IoT Training Program**.

Special thanks to the NTI instructors and mentors for their continuous guidance and support throughout the Training Program.

<div align="center">
<img src="https://www.nti.sci.eg/images/logo.png" height="70">
</div>
