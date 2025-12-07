#include <Arduino.h>

#define MQ7_PIN 14  // Analog input pin for MQ-7 (A0 connected to GPIO14)

// Calibration parameters (you can adjust based on your sensor)
float R0 = 10.0;  // Initial guess for clean air resistance

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("MQ-7 CO Sensor Reading Starting...");
}

void loop() {
  // 1️⃣ Read raw ADC value (12-bit ADC → 0–4095)
  int adcValue = analogRead(MQ7_PIN);

  // 2️⃣ Convert ADC to voltage (ESP32 ADC reference = 3.3V)
  float voltage = (adcValue / 4095.0) * 3.3;

  // 3️⃣ MQ-7 Sensor Basic Ratio (Rs/R0)
  // Sensor output in clean air ~1.5V → Rs/R0 approx 1
  float Rs = (3.3 - voltage) / voltage;  
  float ratio = Rs / R0;

  // 4️⃣ Rough CO ppm estimation (Simplified curve)
  // MQ-7 ppm curve approximation: ppm = 100 * (ratio)^-1.5
  float ppm = 100 * pow(ratio, -1.5);

  Serial.print("ADC Value: ");
  Serial.print(adcValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage);
  Serial.print(" V | CO: ");
  Serial.print(ppm);
  Serial.println(" ppm");

  delay(1000);
}
