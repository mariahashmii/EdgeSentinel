
# EdgeSentinel
### Hybrid TinyML–Generative AI Environmental Anomaly Monitoring System

**Detect locally. Explain remotely.**

EdgeSentinel is an IoT-based environmental monitoring prototype that combines local anomaly detection using a lightweight decision-tree classifier with Generative AI-powered explanations.

The system collects temperature and soil moisture readings through an ESP8266, extracts statistical features, detects environmental anomalies locally, and sends the results to a Python backend.

Google Gemini generates contextual explanations, while a Streamlit dashboard displays sensor readings, system status, and recommendations. Voice alerts are delivered through the laptop.

## Key Features

- Real-time environmental monitoring using ESP8266.
- Temperature sensing using DS18B20.
- Soil moisture monitoring.
- Lightweight decision-tree-based anomaly classification.
- Gemini-powered anomaly explanations.
- Voice alerts using Python text-to-speech.
- Live Streamlit dashboard.
- Demo mode for repeatable NORMAL, WARNING, and CRITICAL scenarios.
- Local sensor processing and classification.

## System Architecture

```text
DS18B20 + Soil Moisture Sensor
              |
              v
           ESP8266
              |
              v
     Feature Extraction
              |
              v
      Local TinyML Classifier
              |
              v
        USB Serial Output
              |
              v
        Python Backend
          /         \
         v           v
      Gemini       Voice Alert
         |
         v
   Streamlit Dashboard
```

## Hardware Requirements

| Component | Purpose |
|---|---|
| ESP8266 NodeMCU | Microcontroller |
| DS18B20 | Temperature measurement |
| Soil Moisture Sensor v1.2 | Soil moisture measurement |
| 4.7kΩ resistor | DS18B20 pull-up |
| USB cable | Power and serial communication |

## Hardware Connections

### DS18B20

| Sensor Wire | ESP8266 |
|---|---|
| Red | 3.3V |
| Black | GND |
| Yellow (Data) | D2 / GPIO4 |

Connect a 4.7kΩ pull-up resistor between the data line and 3.3V.

### Soil Moisture Sensor

| Sensor Pin | ESP8266 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| AOUT | A0 |

## Software Stack

- **Microcontroller:** ESP8266
- **Embedded programming:** Arduino IDE / C++
- **Backend:** Python
- **Machine Learning:** Scikit-learn
- **AI explanations:** Google Gemini API
- **Dashboard:** Streamlit
- **Voice alerts:** pyttsx3
- **Communication:** USB Serial

## Project Structure

```text
EdgeSentinel/
|
|-- arduino/
|   |-- EdgeSentinel.ino
|
|-- scripts/
|   |-- create_dataset.py
|   |-- train_model.py
|   |-- train_tiny_model.py
|   |-- test_model.py
|   |-- esp_reader.py
|   |-- dashboard.py
|   |-- gemini_test.py
|
|-- data/
|   |-- normal.csv
|   |-- tinyml_dataset.csv
|
|-- models/
|   |-- edgesentinel_model.pkl
|   |-- edgesentinel_tiny_model.pkl
|
|-- requirements.txt
|-- .gitignore
|-- README.md
```

## How It Works

### 1. Sensor Data Collection

The ESP8266 collects temperature and soil moisture readings from the connected sensors.

### 2. Feature Extraction

Statistical features are calculated from sensor readings, including:

- Temperature mean
- Temperature variance
- Temperature rate of change
- Moisture mean
- Moisture minimum and maximum
- Moisture rate of change

### 3. Local Anomaly Detection

The current embedded classifier uses a lightweight decision-tree rule based primarily on temperature rate and temperature variance.

It identifies three environmental states:

- NORMAL
- WARNING
- CRITICAL

**Note:** Moisture readings are monitored and passed to the backend, but they are not currently used by the embedded classification rule.

### 4. Generative AI Explanation

The Python backend sends the detected status to Google Gemini to generate an explanation and recommended action.

The AI explanation supplements the local classifier; it does not replace or override its prediction.

### 5. Voice Alerts

The backend uses pyttsx3 to announce the detected environmental status through the laptop speakers.

### 6. Live Dashboard

The Streamlit dashboard displays:

- Temperature readings
- Soil moisture readings
- Environmental status
- Sensor rates of change
- Gemini-generated explanation
- Latest alert

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Arduino IDE
- ESP8266 board support installed in Arduino IDE
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/mariahashmii/EdgeSentinel.git
cd EdgeSentinel
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Arduino Libraries

Install the following libraries through Arduino IDE Library Manager:

- OneWire
- DallasTemperature

### 4. Configure Gemini API Key

Set your API key in PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Do not commit your API key to GitHub.

### 5. Upload Firmware

1. Open `arduino/EdgeSentinel.ino`.
2. Select the appropriate ESP8266 board.
3. Select the correct COM port.
4. Upload the firmware.

### 6. Start the Python Backend

Open a terminal:

```powershell
cd scripts
python esp_reader.py
```

The backend reads ESP8266 serial data, processes predictions, requests Gemini explanations, and generates voice alerts.

### 7. Start the Dashboard

Open a second terminal:

```powershell
cd scripts
streamlit run dashboard.py
```

Open:

http://localhost:8501

**Important:** Close Arduino Serial Monitor before starting the Python backend. Only one application can access the serial port at a time.

If your ESP8266 uses a different COM port, update the port configuration in `esp_reader.py`.

## Demonstration Modes

EdgeSentinel supports two operating modes:

- **REAL MODE:** Processes readings from the connected sensors.
- **DEMO MODE:** Uses predefined sensor patterns to demonstrate NORMAL, WARNING, and CRITICAL conditions.

Demo mode is useful for repeatable demonstrations without manually creating environmental anomalies.

## Limitations

- The current classifier primarily uses temperature-derived features.
- Moisture features are monitored but do not yet influence the classifier.
- Demo-mode sensor patterns are synthetic.
- Synthetic training and testing results do not establish real-world classification accuracy.
- Gemini explanations require an internet connection and a valid API key.
- The current prototype uses laptop speakers for voice alerts.

## Future Improvements

- Integrate moisture features into the anomaly classifier.
- Collect larger real-world sensor datasets.
- Improve model validation under different environmental conditions.
- Deploy a more comprehensive TinyML model.
- Add long-term sensor data logging.
- Explore edge-based AI explanation alternatives.

## Project Status

Developed as an academic IoT and TinyML prototype.

## Author

**Maria Hashmi**

B.Tech Computer Science and Engineering

---

**Detect locally. Explain remotely.**
