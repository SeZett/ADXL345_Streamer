#include "adxl345_spi.h"
#include <Arduino.h>
#include <SPI.h>
#include "mbed.h"

/* ADXL345 registers */
#define REG_BW_RATE     0x2C
#define REG_POWER_CTL   0x2D
#define REG_DATA_FORMAT 0x31
#define REG_DATAX0      0x32

/* Pins (can be overridden in platformio.ini) */
#ifndef CS_PIN
#define CS_PIN 9
#endif
#ifndef SCK_PIN
#define SCK_PIN 10
#endif
#ifndef MOSI_PIN
#define MOSI_PIN 11
#endif
#ifndef MISO_PIN
#define MISO_PIN 12
#endif

constexpr uint32_t SPI_SPEED = 2'000'000;

static mbed::SPI spiPort(
    digitalPinToPinName(MOSI_PIN),
    digitalPinToPinName(MISO_PIN),
    digitalPinToPinName(SCK_PIN));

inline void csLow()  { digitalWrite(CS_PIN, LOW); }
inline void csHigh() { digitalWrite(CS_PIN, HIGH); }

static void adxlWrite(uint8_t reg, uint8_t val) {
    csLow();
    spiPort.write(reg);
    spiPort.write(val);
    csHigh();
}

static void adxlReadBurst(uint8_t startReg, uint8_t *buf, size_t len) {
    csLow();
    spiPort.write(0x80 | 0x40 | startReg);
    for (size_t i = 0; i < len; ++i) {
        buf[i] = spiPort.write(0);
    }
    csHigh();
}

void adxl_init(uint8_t bw_rate_code) {
    pinMode(CS_PIN, OUTPUT);
    csHigh();

    spiPort.frequency(SPI_SPEED);
    spiPort.format(8, 3);   // SPI mode 3

    adxlWrite(REG_DATA_FORMAT, 0x0B); // full-res ±16g
    adxlWrite(REG_BW_RATE, bw_rate_code);
    adxlWrite(REG_POWER_CTL, 0x08);   // measurement mode
}

void adxl_read(AdxlSample &out) {
    uint8_t raw[6];
    adxlReadBurst(REG_DATAX0, raw, 6);

    out.x = (raw[1] << 8) | raw[0];
    out.y = (raw[3] << 8) | raw[2];
    out.z = (raw[5] << 8) | raw[4];
}
