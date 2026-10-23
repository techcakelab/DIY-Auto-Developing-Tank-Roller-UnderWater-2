import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray, QSize

svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1600" height="960" viewBox="0 0 1600 960" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1" opacity="0.6"/>
      <circle cx="0" cy="0" r="1.5" fill="#334155"/>
    </pattern>

    <!-- Component Shadows & Glows -->
    <filter id="drop-shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
    <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ef4444" flood-opacity="0.7"/>
    </filter>
    <filter id="glow-green" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#22c55e" flood-opacity="0.7"/>
    </filter>
    <filter id="glow-yellow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#eab308" flood-opacity="0.7"/>
    </filter>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#06b6d4" flood-opacity="0.7"/>
    </filter>

    <!-- Gradients -->
    <linearGradient id="esp-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1e24"/>
      <stop offset="100%" stop-color="#0d0d11"/>
    </linearGradient>
    <linearGradient id="drv-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="tm-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e3a8a"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
    <linearGradient id="knob-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748b"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <linearGradient id="silver-metal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="50%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
    <linearGradient id="copper-trace" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="1600" height="960" fill="#0b1120"/>
  <rect width="1600" height="960" fill="url(#grid)"/>

  <!-- ==================== TOP TITLE BAR ==================== -->
  <g transform="translate(60, 30)">
    <rect x="0" y="0" width="1480" height="72" rx="12" fill="#1e293b" fill-opacity="0.85" stroke="#334155" stroke-width="1.5" filter="url(#drop-shadow)"/>
    <text x="25" y="34" fill="#f8fafc" font-size="23" font-weight="700" letter-spacing="0.5">ESP32-C3 Super Mini — Film Tank Rotator</text>
    <text x="25" y="55" fill="#94a3b8" font-size="13" font-weight="400">Complete Hardware Wiring Diagram &amp; Pinout (Single-Knob Agitation Machine)</text>

    <!-- Color Legend -->
    <g transform="translate(770, 20)">
      <!-- 5V -->
      <circle cx="10" cy="18" r="6" fill="#ef4444"/>
      <text x="22" y="22" fill="#cbd5e1" font-size="12" font-weight="600">5V Power</text>

      <!-- 3.3V -->
      <circle cx="115" cy="18" r="6" fill="#f97316"/>
      <text x="127" y="22" fill="#cbd5e1" font-size="12" font-weight="600">3.3V Logic</text>

      <!-- GND -->
      <circle cx="220" cy="18" r="6" fill="#64748b"/>
      <text x="232" y="22" fill="#cbd5e1" font-size="12" font-weight="600">GND</text>

      <!-- Motor PWM -->
      <circle cx="295" cy="18" r="6" fill="#38bdf8"/>
      <text x="307" y="22" fill="#cbd5e1" font-size="12" font-weight="600">Motor PWM</text>

      <!-- Display -->
      <circle cx="410" cy="18" r="6" fill="#22c55e"/>
      <text x="422" y="22" fill="#cbd5e1" font-size="12" font-weight="600">Display</text>

      <!-- Encoder -->
      <circle cx="500" cy="18" r="6" fill="#facc15"/>
      <text x="512" y="22" fill="#cbd5e1" font-size="12" font-weight="600">KY-040 Encoder</text>
    </g>
  </g>

  <!-- ==================== WIRES / ROUTING LAYER ==================== -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">

    <!-- === 5V POWER BUS (RED) === -->
    <!-- ESP32 5V (X: 660, Y: 270) -->
    <!-- Branch 1 to DRV8833 VCC (X: 410, Y: 290) -->
    <path d="M 660 270 L 530 270 L 530 290 L 410 290" stroke="#ef4444" stroke-width="4.5" opacity="0.95"/>
    <!-- Branch 2 to TM1637 VCC (X: 1180, Y: 290) -->
    <path d="M 660 270 L 610 270 L 610 140 L 1090 140 L 1090 290 L 1180 290" stroke="#ef4444" stroke-width="4.5" opacity="0.95"/>

    <!-- === GND COMMON BUS (SLATE GREY) === -->
    <!-- ESP32 GND (X: 660, Y: 315) -->
    <!-- Branch to DRV8833 GND (X: 410, Y: 335) -->
    <path d="M 660 315 L 505 315 L 505 335 L 410 335" stroke="#64748b" stroke-width="4.5" opacity="0.95"/>
    <!-- Branch to TM1637 GND (X: 1180, Y: 335) -->
    <path d="M 660 315 L 590 315 L 590 160 L 1070 160 L 1070 335 L 1180 335" stroke="#64748b" stroke-width="4.5" opacity="0.95"/>
    <!-- Branch to KY-040 GND (X: 1160, Y: 785) -->
    <path d="M 505 335 L 505 890 L 1110 890 L 1110 785 L 1160 785" stroke="#64748b" stroke-width="4.5" opacity="0.95"/>

    <!-- === 3.3V POWER (ORANGE) === -->
    <!-- ESP32 3V3 (X: 660, Y: 360) to KY-040 [+] (X: 1160, Y: 740) -->
    <path d="M 660 360 L 545 360 L 545 865 L 1090 865 L 1090 740 L 1160 740" stroke="#f97316" stroke-width="4" opacity="0.95"/>

    <!-- === MOTOR CONTROL SIGNALS (CYAN & BLUE) === -->
    <!-- GPIO 0 (IN1) [660, 405] to DRV8833 IN1 [410, 380] -->
    <path d="M 660 405 L 480 405 L 480 380 L 410 380" stroke="#38bdf8" stroke-width="3.5" filter="url(#glow-cyan)"/>
    <!-- GPIO 1 (IN2) [660, 450] to DRV8833 IN2 [410, 425] -->
    <path d="M 660 450 L 460 450 L 460 425 L 410 425" stroke="#0284c7" stroke-width="3.5"/>

    <!-- === TM1637 DISPLAY SIGNALS (GREEN & LIME) === -->
    <!-- GPIO 4 (DIO) [660, 585] to TM1637 DIO [1180, 245] -->
    <path d="M 660 585 L 565 585 L 565 180 L 1050 180 L 1050 245 L 1180 245" stroke="#22c55e" stroke-width="3.5" filter="url(#glow-green)"/>
    <!-- GPIO 5 (CLK) [940, 270] to TM1637 CLK [1180, 200] -->
    <path d="M 940 270 L 1030 270 L 1030 200 L 1180 200" stroke="#84cc16" stroke-width="3.5"/>

    <!-- === KY-040 ROTARY ENCODER SIGNALS (YELLOW, GOLD, AMBER) === -->
    <!-- CLK -> GPIO 6 [940, 315] to KY-040 CLK [1160, 605] -->
    <path d="M 940 315 L 1060 315 L 1060 605 L 1160 605" stroke="#eab308" stroke-width="4" filter="url(#glow-yellow)"/>
    <!-- DT  -> GPIO 7 [940, 360] to KY-040 DT  [1160, 650] -->
    <path d="M 940 360 L 1040 360 L 1040 650 L 1160 650" stroke="#ca8a04" stroke-width="4"/>
    <!-- SW  -> GPIO 10 [940, 495] to KY-040 SW  [1160, 695] -->
    <path d="M 940 495 L 1020 495 L 1020 695 L 1160 695" stroke="#f59e0b" stroke-width="4"/>

    <!-- === MOTOR OUTPUT TERMINALS === -->
    <!-- DRV8833 OUT1 [200, 380] to Motor Terminal 1 [160, 680] -->
    <path d="M 200 380 L 110 380 L 110 680 L 155 680" stroke="#f43f5e" stroke-width="4"/>
    <!-- DRV8833 OUT2 [200, 425] to Motor Terminal 2 [160, 715] -->
    <path d="M 200 425 L 85 425 L 85 715 L 155 715" stroke="#0ea5e9" stroke-width="4"/>
  </g>

  <!-- ==================== CENTER: ESP32-C3 SUPER MINI ==================== -->
  <g id="esp32c3-board" transform="translate(660, 180)" filter="url(#drop-shadow)">
    <!-- Board PCB -->
    <rect x="0" y="0" width="280" height="495" rx="16" fill="url(#esp-grad)" stroke="#3f3f46" stroke-width="2"/>

    <!-- Silkscreen Accent Frame -->
    <rect x="14" y="14" width="252" height="467" rx="10" fill="none" stroke="#27272a" stroke-width="1.5"/>

    <!-- USB Type-C Connector (Top) -->
    <g transform="translate(95, -16)">
      <rect x="0" y="0" width="90" height="42" rx="6" fill="url(#silver-metal)" stroke="#475569" stroke-width="1.5"/>
      <rect x="15" y="6" width="60" height="18" rx="4" fill="#0f172a"/>
      <text x="45" y="32" fill="#475569" font-size="9" font-weight="700" text-anchor="middle">USB-C</text>
    </g>

    <!-- BOOT & RESET Buttons -->
    <g transform="translate(45, 45)">
      <circle cx="12" cy="12" r="10" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
      <circle cx="12" cy="12" r="5" fill="#f8fafc"/>
      <text x="12" y="34" fill="#94a3b8" font-size="9" text-anchor="middle" font-weight="600">BOOT</text>
    </g>
    <g transform="translate(205, 45)">
      <circle cx="12" cy="12" r="10" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
      <circle cx="12" cy="12" r="5" fill="#f8fafc"/>
      <text x="12" y="34" fill="#94a3b8" font-size="9" text-anchor="middle" font-weight="600">RST</text>
    </g>

    <!-- Status LED (GPIO 8) -->
    <g transform="translate(130, 52)">
      <rect x="0" y="0" width="20" height="12" rx="2" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
      <rect x="4" y="3" width="12" height="6" fill="#60a5fa"/>
      <text x="10" y="24" fill="#38bdf8" font-size="8" text-anchor="middle">LED (IO8)</text>
    </g>

    <!-- ESP32-C3 RF Shielding Can (Center IC) -->
    <g transform="translate(65, 120)">
      <rect x="0" y="0" width="150" height="150" rx="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
      <text x="75" y="55" fill="#e4e4e7" font-size="15" font-weight="800" text-anchor="middle" letter-spacing="1">ESPRESSIF</text>
      <text x="75" y="80" fill="#f43f5e" font-size="13" font-weight="700" text-anchor="middle">ESP32-C3</text>
      <text x="75" y="105" fill="#a1a1aa" font-size="10" text-anchor="middle">RISC-V Super Mini</text>
      <circle cx="18" cy="18" r="3" fill="#d4d4d8"/>
    </g>

    <!-- Onboard Ceramic Antenna (Bottom) -->
    <g transform="translate(70, 405)">
      <rect x="0" y="0" width="140" height="65" rx="6" fill="url(#copper-trace)" stroke="#78350f" stroke-width="1.5"/>
      <path d="M 20 15 H 120 M 20 28 H 120 M 20 41 H 120 M 20 54 H 120" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
      <text x="70" y="38" fill="#451a03" font-size="10" font-weight="800" text-anchor="middle" letter-spacing="1">2.4GHz Wi-Fi / BLE</text>
    </g>

    <!-- ================= LEFT PIN HEADER (8 PINS) ================= -->

    <!-- Pin 1: 5V -->
    <g transform="translate(0, 90)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#ef4444" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#fca5a5" font-size="12" font-weight="800">5V</text>
    </g>

    <!-- Pin 2: GND -->
    <g transform="translate(0, 135)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#475569" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#cbd5e1" font-size="12" font-weight="800">GND</text>
    </g>

    <!-- Pin 3: 3V3 -->
    <g transform="translate(0, 180)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#f97316" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#fdba74" font-size="12" font-weight="800">3V3</text>
    </g>

    <!-- Pin 4: GPIO 0 -->
    <g transform="translate(0, 225)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#0284c7" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#7dd3fc" font-size="11" font-weight="800">0 (IN1)</text>
    </g>

    <!-- Pin 5: GPIO 1 -->
    <g transform="translate(0, 270)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#0284c7" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#7dd3fc" font-size="11" font-weight="800">1 (IN2)</text>
    </g>

    <!-- Pin 6: GPIO 2 -->
    <g transform="translate(0, 315)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#27272a"/>
      <circle cx="12" cy="0" r="6" fill="#71717a" stroke="#52525b" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#52525b" font-size="11">2</text>
    </g>

    <!-- Pin 7: GPIO 3 -->
    <g transform="translate(0, 360)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#27272a"/>
      <circle cx="12" cy="0" r="6" fill="#71717a" stroke="#52525b" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#52525b" font-size="11">3</text>
    </g>

    <!-- Pin 8: GPIO 4 -->
    <g transform="translate(0, 405)">
      <rect x="0" y="-12" width="24" height="24" rx="4" fill="#16a34a" opacity="0.9"/>
      <circle cx="12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="28" y="4" fill="#86efac" font-size="11" font-weight="800">4 (DIO)</text>
    </g>

    <!-- ================= RIGHT PIN HEADER (8 PINS) ================= -->

    <!-- Pin 1 (Right): GPIO 5 -->
    <g transform="translate(280, 90)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#65a30d" opacity="0.9"/>
      <circle cx="-12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#bef264" font-size="11" font-weight="800" text-anchor="end">(CLK) 5</text>
    </g>

    <!-- Pin 2 (Right): GPIO 6 -->
    <g transform="translate(280, 135)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#ca8a04" opacity="0.9"/>
      <circle cx="-12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#fde047" font-size="11" font-weight="800" text-anchor="end">(CLK) 6</text>
    </g>

    <!-- Pin 3 (Right): GPIO 7 -->
    <g transform="translate(280, 180)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#ca8a04" opacity="0.9"/>
      <circle cx="-12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#fde047" font-size="11" font-weight="800" text-anchor="end">(DT) 7</text>
    </g>

    <!-- Pin 4 (Right): GPIO 8 -->
    <g transform="translate(280, 225)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#1e293b"/>
      <circle cx="-12" cy="0" r="6" fill="#475569" stroke="#334155" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#64748b" font-size="10" text-anchor="end">8 (LED)</text>
    </g>

    <!-- Pin 5 (Right): GPIO 9 -->
    <g transform="translate(280, 270)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#1e293b"/>
      <circle cx="-12" cy="0" r="6" fill="#475569" stroke="#334155" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#64748b" font-size="10" text-anchor="end">9 (BOOT)</text>
    </g>

    <!-- Pin 6 (Right): GPIO 10 -->
    <g transform="translate(280, 315)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#d97706" opacity="0.9"/>
      <circle cx="-12" cy="0" r="6" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#fde68a" font-size="11" font-weight="800" text-anchor="end">(SW) 10</text>
    </g>

    <!-- Pin 7 (Right): GPIO 20 -->
    <g transform="translate(280, 360)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#27272a"/>
      <circle cx="-12" cy="0" r="6" fill="#71717a" stroke="#52525b" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#52525b" font-size="10" text-anchor="end">20</text>
    </g>

    <!-- Pin 8 (Right): GPIO 21 -->
    <g transform="translate(280, 405)">
      <rect x="-24" y="-12" width="24" height="24" rx="4" fill="#27272a"/>
      <circle cx="-12" cy="0" r="6" fill="#71717a" stroke="#52525b" stroke-width="1.5"/>
      <circle cx="-12" cy="0" r="2.5" fill="#0f172a"/>
      <text x="-28" y="4" fill="#52525b" font-size="10" text-anchor="end">21</text>
    </g>
  </g>

  <!-- ==================== LEFT MODULE: DRV8833 MOTOR DRIVER ==================== -->
  <g id="drv8833-board" transform="translate(190, 240)" filter="url(#drop-shadow)">
    <!-- Board PCB -->
    <rect x="0" y="0" width="220" height="240" rx="12" fill="url(#drv-grad)" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="110" y="30" fill="#93c5fd" font-size="15" font-weight="800" text-anchor="middle" letter-spacing="1">DRV8833</text>
    <text x="110" y="45" fill="#64748b" font-size="9.5" text-anchor="middle">Dual H-Bridge Driver</text>

    <!-- IC Chip -->
    <rect x="80" y="85" width="60" height="70" rx="4" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>
    <circle cx="90" cy="95" r="2.5" fill="#64748b"/>
    <text x="110" y="125" fill="#cbd5e1" font-size="10" font-weight="700" text-anchor="middle">DRV8833</text>

    <!-- Right Header (Inputs from ESP32) -->
    <!-- VCC (Pin 1) -->
    <g transform="translate(220, 50)">
      <circle cx="-14" cy="0" r="6" fill="#ef4444"/>
      <circle cx="-14" cy="0" r="2.5" fill="#facc15"/>
      <text x="-28" y="4" fill="#fca5a5" font-size="11" font-weight="700" text-anchor="end">VCC / VM</text>
    </g>
    <!-- GND (Pin 2) -->
    <g transform="translate(220, 95)">
      <circle cx="-14" cy="0" r="6" fill="#475569"/>
      <circle cx="-14" cy="0" r="2.5" fill="#facc15"/>
      <text x="-28" y="4" fill="#cbd5e1" font-size="11" font-weight="700" text-anchor="end">GND</text>
    </g>
    <!-- IN1 (Pin 3) -->
    <g transform="translate(220, 140)">
      <circle cx="-14" cy="0" r="6" fill="#0284c7"/>
      <circle cx="-14" cy="0" r="2.5" fill="#facc15"/>
      <text x="-28" y="4" fill="#7dd3fc" font-size="11" font-weight="700" text-anchor="end">IN1</text>
    </g>
    <!-- IN2 (Pin 4) -->
    <g transform="translate(220, 185)">
      <circle cx="-14" cy="0" r="6" fill="#0284c7"/>
      <circle cx="-14" cy="0" r="2.5" fill="#facc15"/>
      <text x="-28" y="4" fill="#7dd3fc" font-size="11" font-weight="700" text-anchor="end">IN2</text>
    </g>

    <!-- Left Header (Outputs to Motor) -->
    <!-- OUT1 -->
    <g transform="translate(0, 140)">
      <circle cx="14" cy="0" r="6" fill="#f43f5e"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fda4af" font-size="11" font-weight="700">OUT1</text>
    </g>
    <!-- OUT2 -->
    <g transform="translate(0, 185)">
      <circle cx="14" cy="0" r="6" fill="#0ea5e9"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#7dd3fc" font-size="11" font-weight="700">OUT2</text>
    </g>

    <text x="110" y="222" fill="#64748b" font-size="9" text-anchor="middle">EEP/SLP pulled HIGH</text>
  </g>

  <!-- ==================== BOTTOM LEFT: N20 GEARED MOTOR ==================== -->
  <g id="n20-motor" transform="translate(155, 600)" filter="url(#drop-shadow)">
    <!-- Motor Body (Metal Cylinder) -->
    <rect x="0" y="55" width="130" height="85" rx="10" fill="url(#silver-metal)" stroke="#475569" stroke-width="2"/>
    <text x="65" y="98" fill="#1e293b" font-size="12" font-weight="800" text-anchor="middle">N20 MOTOR</text>
    <text x="65" y="115" fill="#475569" font-size="10" text-anchor="middle">150 RPM (5V/6V)</text>

    <!-- Metal Gearbox -->
    <rect x="130" y="65" width="60" height="65" rx="4" fill="#d97706" stroke="#92400e" stroke-width="2"/>
    <text x="160" y="103" fill="#fef3c7" font-size="10" font-weight="700" text-anchor="middle">GEAR</text>

    <!-- Output Shaft -->
    <rect x="190" y="92" width="25" height="12" fill="url(#silver-metal)" stroke="#475569"/>

    <!-- Rubber Drive Wheel -->
    <g transform="translate(215, 45)">
      <rect x="0" y="0" width="35" height="105" rx="10" fill="#18181b" stroke="#3f3f46" stroke-width="2"/>
      <line x1="5" y1="20" x2="30" y2="20" stroke="#52525b" stroke-width="2"/>
      <line x1="5" y1="35" x2="30" y2="35" stroke="#52525b" stroke-width="2"/>
      <line x1="5" y1="50" x2="30" y2="50" stroke="#52525b" stroke-width="2"/>
      <line x1="5" y1="65" x2="30" y2="65" stroke="#52525b" stroke-width="2"/>
      <line x1="5" y1="80" x2="30" y2="80" stroke="#52525b" stroke-width="2"/>
      <text x="17" y="130" fill="#94a3b8" font-size="11" font-weight="600" text-anchor="middle">Rubber Wheel</text>
      <text x="17" y="145" fill="#64748b" font-size="9" text-anchor="middle">(Friction Drive)</text>
    </g>

    <!-- Motor Terminals -->
    <circle cx="0" cy="80" r="7" fill="#f43f5e" stroke="#fda4af" stroke-width="1.5"/>
    <circle cx="0" cy="115" r="7" fill="#0ea5e9" stroke="#7dd3fc" stroke-width="1.5"/>
  </g>

  <!-- ==================== TOP RIGHT: TM1637 4-DIGIT DISPLAY ==================== -->
  <g id="tm1637-board" transform="translate(1180, 150)" filter="url(#drop-shadow)">
    <!-- Board PCB -->
    <rect x="0" y="0" width="350" height="215" rx="12" fill="url(#tm-grad)" stroke="#2563eb" stroke-width="2"/>
    <text x="175" y="30" fill="#93c5fd" font-size="15" font-weight="800" text-anchor="middle" letter-spacing="1">TM1637 DISPLAY</text>

    <!-- LED 7-Segment Screen Glass -->
    <rect x="65" y="45" width="265" height="90" rx="8" fill="#0a0a0f" stroke="#1e293b" stroke-width="2"/>
    <!-- Red 7-Segment Digits: 03:30 -->
    <g transform="translate(85, 110)">
      <text x="0" y="0" fill="#ef4444" font-size="52" font-family="'Courier New', Courier, monospace" font-weight="900" filter="url(#glow-red)" letter-spacing="6">03:30</text>
    </g>

    <!-- Left Header (Inputs from ESP32) -->
    <!-- CLK (Pin 1) -->
    <g transform="translate(0, 50)">
      <circle cx="14" cy="0" r="6" fill="#84cc16"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#d9f99d" font-size="12" font-weight="700">CLK</text>
      <text x="65" y="4" fill="#94a3b8" font-size="10">➔ GPIO 5</text>
    </g>
    <!-- DIO (Pin 2) -->
    <g transform="translate(0, 95)">
      <circle cx="14" cy="0" r="6" fill="#22c55e"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#86efac" font-size="12" font-weight="700">DIO</text>
      <text x="65" y="4" fill="#94a3b8" font-size="10">➔ GPIO 4</text>
    </g>
    <!-- VCC (Pin 3) -->
    <g transform="translate(0, 140)">
      <circle cx="14" cy="0" r="6" fill="#ef4444"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fca5a5" font-size="12" font-weight="700">VCC</text>
      <text x="65" y="4" fill="#94a3b8" font-size="10">➔ 5V</text>
    </g>
    <!-- GND (Pin 4) -->
    <g transform="translate(0, 185)">
      <circle cx="14" cy="0" r="6" fill="#475569"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#cbd5e1" font-size="12" font-weight="700">GND</text>
      <text x="65" y="4" fill="#94a3b8" font-size="10">➔ GND</text>
    </g>

    <text x="165" y="165" fill="#60a5fa" font-size="10" text-anchor="middle">Countdown Timer &amp; Speed Overlay</text>
  </g>

  <!-- ==================== BOTTOM RIGHT: KY-040 ROTARY ENCODER ==================== -->
  <g id="ky040-board" transform="translate(1160, 560)" filter="url(#drop-shadow)">
    <!-- Board PCB -->
    <rect x="0" y="0" width="350" height="260" rx="12" fill="#18181b" stroke="#eab308" stroke-width="2"/>
    <text x="230" y="32" fill="#fef08a" font-size="15" font-weight="800" text-anchor="middle" letter-spacing="1">KY-040 ENCODER</text>
    <text x="230" y="48" fill="#a1a1aa" font-size="10" text-anchor="middle">Single-Knob Controller</text>

    <!-- Metal Rotary Encoder Knob (Shifted to right) -->
    <g transform="translate(240, 150)">
      <circle cx="0" cy="0" r="60" fill="#09090b" stroke="#3f3f46" stroke-width="2"/>
      <circle cx="0" cy="0" r="50" fill="url(#knob-grad)" stroke="#64748b" stroke-width="2"/>
      <circle cx="0" cy="0" r="38" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="24" fill="url(#silver-metal)" stroke="#94a3b8" stroke-width="1.5"/>
      <rect x="-3" y="-36" width="6" height="15" rx="2" fill="#38bdf8"/>
    </g>

    <!-- Exact 5 Pin Headers on Left Edge -->
    <!-- Pin 1: CLK (to GPIO 6) -->
    <g transform="translate(0, 45)">
      <circle cx="14" cy="0" r="6" fill="#eab308"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fef08a" font-size="12" font-weight="800">CLK</text>
      <text x="65" y="4" fill="#fde047" font-size="11" font-weight="600">➔ GPIO 6</text>
    </g>

    <!-- Pin 2: DT (to GPIO 7) -->
    <g transform="translate(0, 90)">
      <circle cx="14" cy="0" r="6" fill="#ca8a04"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fef08a" font-size="12" font-weight="800">DT</text>
      <text x="65" y="4" fill="#fde047" font-size="11" font-weight="600">➔ GPIO 7</text>
    </g>

    <!-- Pin 3: SW (to GPIO 10) -->
    <g transform="translate(0, 135)">
      <circle cx="14" cy="0" r="6" fill="#f59e0b"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fde68a" font-size="12" font-weight="800">SW</text>
      <text x="65" y="4" fill="#fde68a" font-size="11" font-weight="600">➔ GPIO 10</text>
    </g>

    <!-- Pin 4: + (VCC to 3.3V) -->
    <g transform="translate(0, 180)">
      <circle cx="14" cy="0" r="6" fill="#f97316"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#fdba74" font-size="12" font-weight="800">+</text>
      <text x="65" y="4" fill="#fdba74" font-size="11" font-weight="600">➔ 3.3V (3V3)</text>
    </g>

    <!-- Pin 5: GND -->
    <g transform="translate(0, 225)">
      <circle cx="14" cy="0" r="6" fill="#475569"/>
      <circle cx="14" cy="0" r="2.5" fill="#facc15"/>
      <text x="28" y="4" fill="#cbd5e1" font-size="12" font-weight="800">GND</text>
      <text x="65" y="4" fill="#cbd5e1" font-size="11" font-weight="600">➔ GND</text>
    </g>

    <text x="240" y="240" fill="#71717a" font-size="9" text-anchor="middle">Push Button uses INPUT_PULLUP</text>
  </g>

  <!-- ==================== HELPFUL HARDWARE ANNOTATION BOXES ==================== -->
  <g transform="translate(480, 750)">
    <rect x="0" y="0" width="620" height="90" rx="8" fill="#1e293b" fill-opacity="0.95" stroke="#334155" stroke-width="1.5"/>
    <text x="20" y="28" fill="#38bdf8" font-size="13" font-weight="700">💡 Hardware Pinout Architecture:</text>
    <text x="20" y="50" fill="#cbd5e1" font-size="12">• Left Header: 5V &amp; GND bus, 3V3 for encoder, GPIO 0 &amp; 1 (PWM motor), GPIO 4 (TM1637 DIO).</text>
    <text x="20" y="70" fill="#cbd5e1" font-size="12">• Right Header: GPIO 5 (TM1637 CLK), GPIO 6 (Encoder CLK), GPIO 7 (Encoder DT), GPIO 10 (Encoder SW).</text>
    <text x="20" y="85" fill="#94a3b8" font-size="11" font-style="italic">• Unused System Pins: GPIO 8 (Onboard blue LED) and GPIO 9 (BOOT strapping button) are safely unassigned.</text>
  </g>

</svg>
"""

svg_path = os.path.join(os.path.dirname(__file__), "wiring_diagram.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"Saved SVG to: {svg_path}")

app = QApplication(sys.argv)
renderer = QSvgRenderer(QByteArray(svg_content.encode("utf-8")))

target_width = 2400
target_height = 1440
image = QImage(QSize(target_width, target_height), QImage.Format_ARGB32)
image.fill(QColor(11, 17, 32))

painter = QPainter(image)
painter.setRenderHint(QPainter.Antialiasing, True)
painter.setRenderHint(QPainter.TextAntialiasing, True)
painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
renderer.render(painter)
painter.end()

png_path = os.path.join(os.path.dirname(__file__), "wiring_diagram.png")
image.save(png_path, "PNG")
print(f"Saved PNG to: {png_path}")

jpg_path = os.path.join(os.path.dirname(__file__), "wiring_diagram.jpg")
image.save(jpg_path, "JPEG", 95)
print(f"Saved JPG to: {jpg_path}")

artifact_dir = r"C:\Users\LENOVO\.gemini\antigravity-ide\brain\e225de69-8d66-487c-8e14-6f7160e803b9"
if os.path.exists(artifact_dir):
    artifact_jpg = os.path.join(artifact_dir, "wiring_diagram.jpg")
    image.save(artifact_jpg, "JPEG", 95)
    print(f"Saved artifact copy to: {artifact_jpg}")
