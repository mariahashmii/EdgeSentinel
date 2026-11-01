import json
import serial
import time
import pyttsx3
from pathlib import Path
from google import genai


# =====================================================
#                  ESP8266 CONFIGURATION
# =====================================================

PORT = "COM3"
BAUD = 115200


# =====================================================
#                  DASHBOARD CONFIGURATION
# =====================================================

# Always save dashboard_state.json in the same folder
# as this Python file.

BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_FILE = BASE_DIR / "dashboard_state.json"


# =====================================================
#                  GEMINI CONFIGURATION
# =====================================================

MODEL = "gemini-3.5-flash-lite"


# =====================================================
#                  TTS CONFIGURATION
# =====================================================

tts = pyttsx3.init()

tts.setProperty("rate", 165)
tts.setProperty("volume", 1.0)


# =====================================================
#                  CONNECT TO ESP8266
# =====================================================

print("================================")
print("       EDGESENTINEL BACKEND")
print("================================")
print()

print("Connecting to ESP8266...")

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)

time.sleep(2)

# Remove ESP8266 startup garbage
ser.reset_input_buffer()

print("ESP8266 connected on", PORT)
print("Waiting for TinyML events...")
print()


# =====================================================
#                  CONNECT TO GEMINI
# =====================================================

client = genai.Client()


# =====================================================
#                  SENSOR VALUES
# =====================================================

temperature_mean = None
temperature_variance = None
temperature_rate = None

moisture_mean = None
moisture_minimum = None
moisture_maximum = None
moisture_rate = None


# =====================================================
#                  DASHBOARD STATE
# =====================================================

def write_dashboard_state(
    temperature,
    moisture,
    status,
    gemini_text,
    alert,
    temp_rate,
    moisture_rate
):

    data = {
        "temperature": temperature if temperature is not None else 0,
        "moisture": moisture if moisture is not None else 0,
        "status": status,
        "gemini": gemini_text,
        "alert": alert,
        "temp_rate": temp_rate if temp_rate is not None else 0,
        "moisture_rate": moisture_rate if moisture_rate is not None else 0
    }

    try:

        with open(DASHBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as e:

        print("Dashboard update error:", e)


# =====================================================
#                  ALERT MESSAGE
# =====================================================

def get_alert_message(prediction):

    if prediction == "NORMAL":

        return (
            "Edge Sentinel reports normal conditions. "
            "Temperature and moisture are stable. "
            "Continue standard monitoring."
        )

    elif prediction == "WARNING":

        return (
            "Edge Sentinel warning. "
            "Temperature is increasing while moisture is decreasing. "
            "Please inspect the monitored environment."
        )

    elif prediction == "CRITICAL":

        return (
            "Edge Sentinel critical alert. "
            "Temperature is rising rapidly while moisture is "
            "falling sharply. "
            "Immediately inspect the monitored environment."
        )

    else:

        return (
            "Edge Sentinel has detected an unknown condition."
        )


# =====================================================
#                  VOICE ALERT
# =====================================================

def speak_alert(prediction):

    message = get_alert_message(prediction)

    print()
    print("================================")
    print("          VOICE ALERT")
    print("================================")

    print(message)

    print("================================")
    print()

    # Speak through laptop speakers
    try:

        tts.say(message)
        tts.runAndWait()

    except Exception as e:

        print("TTS error:", e)

    return message


# =====================================================
#                  GEMINI FUNCTION
# =====================================================

def ask_gemini(prediction):

    prompt = f"""
You are the contextual explanation system for EdgeSentinel.

IMPORTANT:
The TinyML model running locally on the ESP8266 is the
anomaly detector.

You are NOT the anomaly detector.

The TinyML model has already classified the condition as:

{prediction}

Your job is ONLY to explain what the detected condition
means using the measured sensor data.

--------------------------------
SENSOR DATA
--------------------------------

Temperature mean:
{temperature_mean} °C

Temperature variance:
{temperature_variance}

Temperature rate:
{temperature_rate} °C over the observation window

Moisture mean:
{moisture_mean} %

Moisture minimum:
{moisture_minimum} %

Moisture maximum:
{moisture_maximum} %

Moisture rate:
{moisture_rate} %

--------------------------------
IMPORTANT RULES
--------------------------------

1. Do NOT change the TinyML classification.

2. Do NOT claim that you detected the anomaly yourself.

3. Do NOT invent specific causes such as fire,
   equipment failure, drought, or overheating.

4. Base the explanation only on the observed
   temperature and moisture measurements.

5. Clearly distinguish measured behavior from
   possible interpretation.

6. Keep the explanation concise.

--------------------------------
RESPONSE FORMAT
--------------------------------

Give exactly three sections:

1. What is happening:
Describe the observed temperature and moisture pattern.

2. Environmental interpretation:
Give a cautious interpretation based only on
the measurements.

3. Recommended action:
Give one simple practical action.

Remember:
TinyML detects the condition.
Gemini explains the condition.
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        gemini_text = response.text

        print()
        print("================================")
        print("        GEMINI EXPLANATION")
        print("================================")

        print(gemini_text)

        print("================================")
        print()

        return gemini_text

    except Exception as e:

        print()
        print("================================")
        print("        GEMINI ERROR")
        print("================================")

        print(e)

        print("================================")
        print()

        return "Gemini explanation unavailable."


# =====================================================
#                  READ ESP8266
# =====================================================

while True:

    try:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

    except Exception as e:

        print("Serial read error:", e)
        continue


    if not line:
        continue


    print(line)


    # =================================================
    #       TEMPERATURE FEATURES
    # =================================================

    if line.startswith("Temperature mean"):

        try:

            temperature_mean = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    elif line.startswith("Temperature variance"):

        try:

            temperature_variance = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    elif line.startswith("Temperature rate"):

        try:

            temperature_rate = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    # =================================================
    #       MOISTURE FEATURES
    # =================================================

    elif line.startswith("Moisture mean"):

        try:

            moisture_mean = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    elif line.startswith("Moisture minimum"):

        try:

            moisture_minimum = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    elif line.startswith("Moisture maximum"):

        try:

            moisture_maximum = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    elif line.startswith("Moisture rate"):

        try:

            moisture_rate = float(
                line.split(":", 1)[1].strip()
            )

        except ValueError:

            pass


    # =================================================
    #       TINYML CLASSIFICATION
    # =================================================

    elif line.startswith("Prediction:"):

        prediction = line.split(
            ":",
            1
        )[1].strip()


        print()
        print("================================")
        print("       TINYML EVENT")
        print("================================")

        print(
            "TinyML classification:",
            prediction
        )

        print("================================")


        # ---------------------------------------------
        # Create initial dashboard state immediately
        # ---------------------------------------------

        initial_alert = get_alert_message(prediction)

        write_dashboard_state(
            temperature_mean,
            moisture_mean,
            prediction,
            "Generating Gemini explanation...",
            initial_alert,
            temperature_rate,
            moisture_rate
        )


        # ---------------------------------------------
        # Gemini explanation
        # ---------------------------------------------

        gemini_explanation = ask_gemini(prediction)


        # ---------------------------------------------
        # Voice alert
        # ---------------------------------------------

        alert_message = speak_alert(prediction)


        # ---------------------------------------------
        # Final dashboard update
        # ---------------------------------------------

        write_dashboard_state(
            temperature_mean,
            moisture_mean,
            prediction,
            gemini_explanation,
            alert_message,
            temperature_rate,
            moisture_rate
        )