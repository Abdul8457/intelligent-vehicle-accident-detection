/*
 * Portfolio reference firmware skeleton.
 * Replace demo values with readings from the selected IMU.
 */

const float ACCELERATION_THRESHOLD_G = 3.0;
const float GYRO_THRESHOLD_DPS = 180.0;
const int CONFIRMATION_SAMPLES = 3;

int abnormalSamples = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  float accelerationG = 0.0;
  float gyroDps = 0.0;

  bool abnormal =
      abs(accelerationG) >= ACCELERATION_THRESHOLD_G ||
      abs(gyroDps) >= GYRO_THRESHOLD_DPS;

  if (abnormal) {
    abnormalSamples++;
    if (abnormalSamples >= CONFIRMATION_SAMPLES) {
      Serial.println("ACCIDENT EVENT CONFIRMED");
      abnormalSamples = 0;
    }
  } else {
    abnormalSamples = 0;
  }

  delay(20);
}
