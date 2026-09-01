# Intelligent Vehicle Accident Detection & Emergency Alert System

A software-based version of my 2021 undergraduate academic project for detecting potential vehicle accidents using acceleration and gyroscope data, obtaining GPS location information, and generating emergency-alert messages.

> **Project status:** Completed academic project  
> **Note:** This repository presents a cleaned and testable software version of my 2021 undergraduate academic project. The current implementation uses synthetic sensor data to demonstrate and test the accident-detection logic without requiring the original hardware.

## Objectives

- Detect abnormal vehicle motion from acceleration and gyroscope data.
- Confirm potential accident events using consecutive abnormal samples.
- Reduce false triggers from short abnormal sensor readings.
- Process GPS position information.
- Generate emergency-alert messages.
- Analyze sensor data using Python.
- Provide automated software tests.
- Maintain a modular project structure.

## Architecture

```text
Sensor / Simulated Data
          |
          v
     Data Loading
          |
          v
   Accident Detector
          |
          v
  Event Confirmation
       /       \
   Reject     Confirm
                 |
                 v
                GPS
                 |
                 v
          Alert Manager
                 |
                 v
          Alert Message
                 |
                 v
        Python Analysis
