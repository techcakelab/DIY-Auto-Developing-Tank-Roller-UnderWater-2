#include "TM1637Display.h"
#include "config.h"

// --- TM1637 Display ---
TM1637Display display(PIN_TM1637_CLK, PIN_TM1637_DIO);
bool showColon = true;

// --- State Machine ---
enum State { IDLE, RUNNING, PAUSED, DONE };
State currentState = IDLE;

enum AgitPhase { CW, PAUSE_1, CCW, PAUSE_2 };
AgitPhase currentAgitPhase = CW;

// --- Global Variables ---
uint32_t totalTimeSec = DEFAULT_DEVELOP_SEC;
uint32_t remainTimeSec = DEFAULT_DEVELOP_SEC;
uint8_t speedPct = DEFAULT_SPEED_PCT;

unsigned long lastTickMs = 0;
unsigned long agitPhaseStartMs = 0;
unsigned long blinkTickMs = 0;
bool isBlinkOff = false;

// Speed display overlay timeout
unsigned long speedShowUntilMs = 0;

// --- Encoder Logic ---
int lastEncStateCLK;
unsigned long lastEncDebounceTime = 0;

// --- Button Logic ---
bool btnState = HIGH;
bool lastBtnState = HIGH;
unsigned long lastBtnDebounceTime = 0;
unsigned long btnPressedTime = 0;
bool btnLongPressFired = false;

// ----------------------------------------------------------------
// Motor Control (Compatible with both ESP32 Arduino Core 2.x and 3.x)
// ----------------------------------------------------------------
void initMotor() {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttach(PIN_MOTOR_IN1, MOTOR_PWM_FREQ, MOTOR_PWM_RES);
  ledcAttach(PIN_MOTOR_IN2, MOTOR_PWM_FREQ, MOTOR_PWM_RES);
#else
  ledcSetup(MOTOR_PWM_CH1, MOTOR_PWM_FREQ, MOTOR_PWM_RES);
  ledcSetup(MOTOR_PWM_CH2, MOTOR_PWM_FREQ, MOTOR_PWM_RES);
  ledcAttachPin(PIN_MOTOR_IN1, MOTOR_PWM_CH1);
  ledcAttachPin(PIN_MOTOR_IN2, MOTOR_PWM_CH2);
#endif
  stopMotor();
}

void setMotorSpeed(uint8_t pct, bool cw) {
  uint32_t duty = map(pct, 0, 100, 0, 255);
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  if (pct == 0) {
    ledcWrite(PIN_MOTOR_IN1, 0);
    ledcWrite(PIN_MOTOR_IN2, 0);
  } else if (cw) {
    ledcWrite(PIN_MOTOR_IN1, duty);
    ledcWrite(PIN_MOTOR_IN2, 0);
  } else {
    ledcWrite(PIN_MOTOR_IN1, 0);
    ledcWrite(PIN_MOTOR_IN2, duty);
  }
#else
  if (pct == 0) {
    ledcWrite(MOTOR_PWM_CH1, 0);
    ledcWrite(MOTOR_PWM_CH2, 0);
  } else if (cw) {
    ledcWrite(MOTOR_PWM_CH1, duty);
    ledcWrite(MOTOR_PWM_CH2, 0);
  } else {
    ledcWrite(MOTOR_PWM_CH1, 0);
    ledcWrite(MOTOR_PWM_CH2, duty);
  }
#endif
}

void stopMotor() {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(PIN_MOTOR_IN1, 0);
  ledcWrite(PIN_MOTOR_IN2, 0);
#else
  ledcWrite(MOTOR_PWM_CH1, 0);
  ledcWrite(MOTOR_PWM_CH2, 0);
#endif
}

// ----------------------------------------------------------------
// Display Updates
// ----------------------------------------------------------------
void updateDisplay() {
  unsigned long now = millis();
  static unsigned long lastDisplayRefreshMs = 0;
  if (now - lastDisplayRefreshMs < 50) return; // Cap at 20 FPS for TM1637 refresh rate
  lastDisplayRefreshMs = now;

  // If showing speed temporarily
  if (now < speedShowUntilMs) {
    // Show 'SPxx'
    uint8_t data[] = {
      SEG_A | SEG_C | SEG_D | SEG_F | SEG_G, // S
      SEG_A | SEG_B | SEG_E | SEG_F | SEG_G, // P
      display.encodeDigit(speedPct / 10),
      display.encodeDigit(speedPct % 10)
    };
    if (speedPct == 100) {
      data[1] = display.encodeDigit(1);
      data[2] = display.encodeDigit(0);
      data[3] = display.encodeDigit(0);
    }
    display.setSegments(data);
    return;
  }

  // Handle blinking for Paused/Done state
  if (currentState == PAUSED || currentState == DONE) {
    if (now - blinkTickMs > 500) {
      blinkTickMs = now;
      isBlinkOff = !isBlinkOff;
    }
  } else {
    isBlinkOff = false;
  }

  // Show DONE text or Timer
  if (currentState == DONE) {
    if (isBlinkOff) {
      display.clear();
    } else {
      uint8_t doneMsg[] = {
        SEG_B | SEG_C | SEG_D | SEG_E | SEG_G,         // d
        SEG_C | SEG_D | SEG_E | SEG_G,                 // o
        SEG_C | SEG_E | SEG_G,                         // n
        SEG_A | SEG_D | SEG_E | SEG_F | SEG_G          // E
      };
      display.setSegments(doneMsg);
    }
  } else {
    // Show Timer MM:SS
    if (isBlinkOff) {
      display.clear();
    } else {
      int m = remainTimeSec / 60;
      int s = remainTimeSec % 60;
      int displayValue = (m * 100) + s;
      
      // Toggle colon every second when running
      if (currentState == RUNNING) {
        showColon = (now % 1000) < 500;
      } else {
        showColon = true;
      }
      
      uint8_t dots = showColon ? 0x40 : 0x00; // 0x40 is the center colon on most TM1637
      display.showNumberDecEx(displayValue, dots, true);
    }
  }
}

// ----------------------------------------------------------------
// Hardware Interrupts / Polling for Encoder
// ----------------------------------------------------------------
void IRAM_ATTR isrEncoder() {
  unsigned long now = millis();
  if (now - lastEncDebounceTime < 5) return; // 5ms debounce
  lastEncDebounceTime = now;

  int dtState = digitalRead(PIN_ENC_DT);
  int clkState = digitalRead(PIN_ENC_CLK);

  if (clkState != lastEncStateCLK && clkState == 1) {
    if (dtState != clkState) {
      // Clockwise
      if (currentState == IDLE) {
        totalTimeSec += TIMER_STEP_SEC;
        if (totalTimeSec > TIMER_MAX_SEC) totalTimeSec = TIMER_MAX_SEC;
        remainTimeSec = totalTimeSec;
      } else {
        speedPct += SPEED_STEP_PCT;
        if (speedPct > SPEED_MAX_PCT) speedPct = SPEED_MAX_PCT;
        speedShowUntilMs = millis() + 1500; // Show speed for 1.5s
      }
    } else {
      // Counter-Clockwise
      if (currentState == IDLE) {
        if (totalTimeSec > TIMER_MIN_SEC + TIMER_STEP_SEC) totalTimeSec -= TIMER_STEP_SEC;
        remainTimeSec = totalTimeSec;
      } else {
        if (speedPct > SPEED_MIN_PCT + SPEED_STEP_PCT) speedPct -= SPEED_STEP_PCT;
        speedShowUntilMs = millis() + 1500;
      }
    }
  }
  lastEncStateCLK = clkState;
}

// ----------------------------------------------------------------
// Setup
// ----------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("\n--- ESP32-C3 Film Rotator Starting ---");
  Serial.printf("TM1637: CLK = GPIO %d, DIO = GPIO %d\n", PIN_TM1637_CLK, PIN_TM1637_DIO);

  // Encoder
  pinMode(PIN_ENC_CLK, INPUT_PULLUP);
  pinMode(PIN_ENC_DT, INPUT_PULLUP);
  pinMode(PIN_ENC_SW, INPUT_PULLUP);
  lastEncStateCLK = digitalRead(PIN_ENC_CLK);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_CLK), isrEncoder, CHANGE);

  initMotor();

  // Display Test
  display.setBrightness(7, true); // Maximum brightness (0-7)
  
  // Turn on all 4 digits (88:88) for 1 second as a display self-test
  uint8_t allOn[] = { 0xff, 0xff, 0xff, 0xff };
  display.setSegments(allOn);
  delay(1000);

  Serial.println("Ready in IDLE state (03:30)");
}

// ----------------------------------------------------------------
// Button Actions
// ----------------------------------------------------------------
void onButtonShortPress() {
  if (currentState == IDLE || currentState == PAUSED || currentState == DONE) {
    if (currentState == DONE) {
      remainTimeSec = totalTimeSec;
    }
    currentState = RUNNING;
    currentAgitPhase = CW;
    agitPhaseStartMs = millis();
    lastTickMs = millis();
  } else if (currentState == RUNNING) {
    currentState = PAUSED;
    stopMotor();
  }
}

void onButtonLongPress() {
  currentState = IDLE;
  remainTimeSec = totalTimeSec;
  stopMotor();
  speedShowUntilMs = 0; // Clear speed overlay
}

void pollButton() {
  int reading = digitalRead(PIN_ENC_SW);

  if (reading != lastBtnState) {
    lastBtnDebounceTime = millis();
  }

  if ((millis() - lastBtnDebounceTime) > BTN_DEBOUNCE_MS) {
    if (reading != btnState) {
      btnState = reading;

      if (btnState == LOW) {
        // Pressed
        btnPressedTime = millis();
        btnLongPressFired = false;
      } else {
        // Released
        if (!btnLongPressFired) {
          onButtonShortPress();
        }
      }
    } else if (btnState == LOW && !btnLongPressFired) {
      if (millis() - btnPressedTime > BTN_LONG_PRESS_MS) {
        btnLongPressFired = true;
        onButtonLongPress();
      }
    }
  }
  lastBtnState = reading;
}

// ----------------------------------------------------------------
// Loop
// ----------------------------------------------------------------
void loop() {
  pollButton();

  // Timer Tick
  if (currentState == RUNNING) {
    unsigned long now = millis();
    
    // Countdown
    if (now - lastTickMs >= 1000) {
      lastTickMs = now;
      if (remainTimeSec > 0) {
        remainTimeSec--;
      } else {
        currentState = DONE;
        stopMotor();
      }
    }

    // Agitation Cycle
    if (currentState == RUNNING) {
      unsigned long phaseElapsed = now - agitPhaseStartMs;
      
      switch(currentAgitPhase) {
        case CW:
          setMotorSpeed(speedPct, true);
          if (phaseElapsed >= AGIT_ON_SEC * 1000) {
            currentAgitPhase = PAUSE_1;
            agitPhaseStartMs = now;
            stopMotor();
          }
          break;
        case PAUSE_1:
          if (phaseElapsed >= AGIT_PAUSE_SEC * 1000) {
            currentAgitPhase = CCW;
            agitPhaseStartMs = now;
          }
          break;
        case CCW:
          setMotorSpeed(speedPct, false);
          if (phaseElapsed >= AGIT_ON_SEC * 1000) {
            currentAgitPhase = PAUSE_2;
            agitPhaseStartMs = now;
            stopMotor();
          }
          break;
        case PAUSE_2:
          if (phaseElapsed >= AGIT_PAUSE_SEC * 1000) {
            currentAgitPhase = CW;
            agitPhaseStartMs = now;
          }
          break;
      }
    }
  }

  // Refresh screen efficiently
  updateDisplay();
}
