#include <Arduino.h>
#include "adxl345_spi.h"

struct __attribute__((packed)) Frame {
    uint32_t timestamp_us;
    int16_t x;
    int16_t y;
    int16_t z;
};

static uint32_t sample_interval_us = 4000; // 250 Hz
static uint32_t t0_us = 0;

void setup() {
    Serial.begin(2'000'000);
    while (!Serial) {}       // warten bis USB bereit ist

    adxl_init(0x0A);        // ADXL345 initialisieren
    t0_us = micros();       // Startzeit
}

void loop() {
    static uint32_t next_us = micros();
    uint32_t now = micros();

    if ((int32_t)(now - next_us) >= 0) {
        next_us += sample_interval_us;

        AdxlSample s;
        adxl_read(s);

        Frame f;
        f.timestamp_us = now - t0_us;
        f.x = s.x;
        f.y = s.y;
        f.z = s.z;

        Serial.write((uint8_t *)&f, sizeof(f));
    }
}
