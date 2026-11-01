#include <OneWire.h>
#include <DallasTemperature.h>

// =====================================================
//                 MODE SWITCH
// =====================================================

// true  = DEMO MODE
// false = REAL SENSOR MODE

#define DEMO_MODE false


// =====================================================
//                 PIN CONFIGURATION
// =====================================================

#define ONE_WIRE_BUS 4      // DS18B20 DATA -> GPIO4 (D2)
#define MOISTURE_PIN A0     // Soil moisture -> A0


// =====================================================
//                 DS18B20 SETUP
// =====================================================

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


// =====================================================
//                 MOISTURE CALIBRATION
// =====================================================

int dryValue = 13;
int wetValue = 73;


// =====================================================
//                 TINYML SETTINGS
// =====================================================

const int WINDOW_SIZE = 10;

float tempData[WINDOW_SIZE];
float moistureData[WINDOW_SIZE];

int indexCount = 0;


// =====================================================
//              TINYML DECISION TREE
// =====================================================
//
// 0 = NORMAL
// 1 = WARNING
// 2 = CRITICAL
//
// Learned rules from your trained model:
//
// temp_rate <= 0.51              -> NORMAL
//
// temp_rate > 0.51 AND
// temp_variance <= 0.64          -> WARNING
//
// temp_rate > 0.51 AND
// temp_variance > 0.64           -> CRITICAL
//
// =====================================================

int predictTinyML(float tempRate, float tempVariance) {

  if (tempRate <= 0.51) {
    return 0;   // NORMAL
  }

  if (tempVariance <= 0.64) {
    return 1;   // WARNING
  }

  return 2;     // CRITICAL
}


// =====================================================
//                 PRINT RESULT
// =====================================================

void printPrediction(int prediction) {

  Serial.println();
  Serial.println("================================");
  Serial.println("          TINYML RESULT");
  Serial.println("================================");

  Serial.print("Prediction: ");

  if (prediction == 0) {
    Serial.println("NORMAL");
  }

  else if (prediction == 1) {
    Serial.println("WARNING");
  }

  else {
    Serial.println("CRITICAL");
  }

  Serial.println("================================");
  Serial.println();
}


// =====================================================
//             PROCESS TINYML WINDOW
// =====================================================
//
// This is the same processing used for both
// REAL mode and DEMO mode.
//
// =====================================================

void processWindow() {

  // ---------------------------------------------------
  // Temperature features
  // ---------------------------------------------------

  float tempRate = tempData[WINDOW_SIZE - 1]
                 - tempData[0];


  float tempMean = 0;

  for (int i = 0; i < WINDOW_SIZE; i++) {
    tempMean += tempData[i];
  }

  tempMean = tempMean / WINDOW_SIZE;


  float tempVariance = 0;

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float difference = tempData[i] - tempMean;

    tempVariance += difference * difference;
  }

  tempVariance = tempVariance / WINDOW_SIZE;


  // ---------------------------------------------------
  // Moisture features
  // ---------------------------------------------------

  float moistureMean = 0;

  float moistureMin = moistureData[0];

  float moistureMax = moistureData[0];


  for (int i = 0; i < WINDOW_SIZE; i++) {

    moistureMean += moistureData[i];

    if (moistureData[i] < moistureMin) {
      moistureMin = moistureData[i];
    }

    if (moistureData[i] > moistureMax) {
      moistureMax = moistureData[i];
    }
  }

  moistureMean = moistureMean / WINDOW_SIZE;


  float moistureRate =
      moistureData[WINDOW_SIZE - 1]
      - moistureData[0];


  // ---------------------------------------------------
  // TinyML prediction
  // ---------------------------------------------------

  int prediction =
      predictTinyML(tempRate, tempVariance);


  // ---------------------------------------------------
  // Print features
  // ---------------------------------------------------

  Serial.println();
  Serial.println("================================");
  Serial.println("          FEATURE VALUES");
  Serial.println("================================");

  Serial.print("Temperature mean     : ");
  Serial.println(tempMean, 3);

  Serial.print("Temperature variance : ");
  Serial.println(tempVariance, 3);

  Serial.print("Temperature rate     : ");
  Serial.println(tempRate, 3);

  Serial.print("Moisture mean        : ");
  Serial.println(moistureMean, 3);

  Serial.print("Moisture minimum     : ");
  Serial.println(moistureMin, 3);

  Serial.print("Moisture maximum     : ");
  Serial.println(moistureMax, 3);

  Serial.print("Moisture rate        : ");
  Serial.println(moistureRate, 3);


  // ---------------------------------------------------
  // Print prediction
  // ---------------------------------------------------

  printPrediction(prediction);
}


// =====================================================
//                 REAL SENSOR MODE
// =====================================================

void runRealMode() {

  sensors.requestTemperatures();

  float temperature =
      sensors.getTempCByIndex(0);


  // Read moisture sensor

  int rawMoisture =
      analogRead(MOISTURE_PIN);


  int moisturePercent =
      map(
        rawMoisture,
        dryValue,
        wetValue,
        0,
        100
      );


  moisturePercent =
      constrain(
        moisturePercent,
        0,
        100
      );


  // Store reading

  tempData[indexCount] =
      temperature;

  moistureData[indexCount] =
      moisturePercent;


  indexCount++;


  // ---------------------------------------------------
  // Display reading
  // ---------------------------------------------------

  Serial.print("Reading ");

  Serial.print(indexCount);

  Serial.print("/");

  Serial.print(WINDOW_SIZE);

  Serial.print(" | Temp: ");

  Serial.print(
      temperature,
      2
  );

  Serial.print(" C");

  Serial.print(" | Moisture: ");

  Serial.print(
      moisturePercent
  );

  Serial.print(" %");

  Serial.print(" | Raw: ");

  Serial.println(
      rawMoisture
  );


  // ---------------------------------------------------
  // Process after 10 readings
  // ---------------------------------------------------

  if (indexCount == WINDOW_SIZE) {

    processWindow();

    indexCount = 0;
  }


  delay(1000);
}


// =====================================================
//                 DEMO MODE
// =====================================================
//
// DEMO MODE creates three artificial patterns:
//
// NORMAL
// WARNING
// CRITICAL
//
// This is ONLY for demonstrating the TinyML pipeline.
// It is not real sensor data.
//
// =====================================================

void runDemoMode() {

  // ---------------------------------------------------
  // NORMAL
  // ---------------------------------------------------

  Serial.println();
  Serial.println();
  Serial.println("################################");
  Serial.println("       DEMO: NORMAL");
  Serial.println("################################");

  Serial.println(
      "Simulating stable environment..."
  );


  for (int i = 0; i < WINDOW_SIZE; i++) {

    tempData[i] =
        27.0 + (i * 0.01);

    moistureData[i] =
        20.0;
  }


  processWindow();


  delay(3000);


  // ---------------------------------------------------
  // WARNING
  // ---------------------------------------------------

  Serial.println();
  Serial.println();
  Serial.println("################################");
  Serial.println("       DEMO: WARNING");
  Serial.println("################################");

  Serial.println(
      "Simulating gradual temperature rise..."
  );


  for (int i = 0; i < WINDOW_SIZE; i++) {

    tempData[i] =
        27.0 + (i * 0.15);

    moistureData[i] =
        20.0 - (i * 0.5);
  }


  processWindow();


  delay(3000);


  // ---------------------------------------------------
  // CRITICAL
  // ---------------------------------------------------

  Serial.println();
  Serial.println();
  Serial.println("################################");
  Serial.println("       DEMO: CRITICAL");
  Serial.println("################################");

  Serial.println(
      "Simulating rapid temperature rise..."
  );


  for (int i = 0; i < WINDOW_SIZE; i++) {

    tempData[i] =
        27.0 + (i * 0.6);

    moistureData[i] =
        20.0 - (i * 2.0);
  }


  processWindow();


  delay(5000);
}


// =====================================================
//                       SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  sensors.begin();

  delay(1000);


  Serial.println();
  Serial.println();
  Serial.println("======================================");
  Serial.println("          EDGESENTINEL");
  Serial.println("       TinyML Anomaly System");
  Serial.println("======================================");


  if (DEMO_MODE) {

    Serial.println("MODE: DEMO");

    Serial.println(
        "Showing NORMAL / WARNING / CRITICAL"
    );
  }

  else {

    Serial.println("MODE: REAL SENSOR");

    Serial.println(
        "Reading DS18B20 + Soil Moisture"
    );
  }


  Serial.println();
}


// =====================================================
//                       LOOP
// =====================================================

void loop() {

  if (DEMO_MODE) {

    runDemoMode();

  }

  else {

    runRealMode();

  }
}