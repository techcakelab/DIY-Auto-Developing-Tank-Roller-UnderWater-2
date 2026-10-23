#ifndef CONFIG_H
#define CONFIG_H

// ================================================================
// ESP32-C3 Super Mini Film Tank Rotator — Parameter Configuration
// Hardware: ESP32-C3 Super Mini, TM1637 LED Display, KY-040 Encoder, DRV8833
// ================================================================

// ----------------------------------------------------------------
// MOTOR DRIVER — DRV8833 (PWM Control)
// ----------------------------------------------------------------
// Safe pin assignment on ESP32-C3 Super Mini (Left header)
#define PIN_MOTOR_IN1       0
#define PIN_MOTOR_IN2       1
#define MOTOR_PWM_FREQ      5000
#define MOTOR_PWM_RES       8      // 8-bit resolution (0-255)
#define MOTOR_PWM_CH1       0
#define MOTOR_PWM_CH2       1

// ----------------------------------------------------------------
// TM1637 4-DIGIT LED DISPLAY
// ----------------------------------------------------------------
// Left header
#define PIN_TM1637_DIO      4
#define PIN_TM1637_CLK      5

// ----------------------------------------------------------------
// KY-040 ROTARY ENCODER
// ----------------------------------------------------------------
// Right header (Avoids built-in LED GPIO 8 and BOOT button GPIO 9)
#define PIN_ENC_CLK         6
#define PIN_ENC_DT          7
#define PIN_ENC_SW          10     // Push button (Active LOW)

#define BTN_DEBOUNCE_MS     50
#define BTN_LONG_PRESS_MS   800

// ----------------------------------------------------------------
// TIMING DEFAULTS
// ----------------------------------------------------------------
#define DEFAULT_DEVELOP_SEC 210    // 3:30 (C-41 developer)
#define TIMER_STEP_SEC      15     // 15 seconds per click
#define TIMER_MIN_SEC       15
#define TIMER_MAX_SEC       3600

// Agitation Cycle
#define AGIT_ON_SEC         10     // Run 10s
#define AGIT_PAUSE_SEC      1      // Pause 1s between directions

// Speed
#define DEFAULT_SPEED_PCT   70     // 70% duty cycle
#define SPEED_STEP_PCT      5      // 5% per click
#define SPEED_MIN_PCT       30
#define SPEED_MAX_PCT       100

#endif // CONFIG_H
