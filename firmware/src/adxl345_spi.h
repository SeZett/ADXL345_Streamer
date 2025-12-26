#pragma once
#include <stdint.h>

struct AdxlSample {
    int16_t x;
    int16_t y;
    int16_t z;
};

void adxl_init(uint8_t bw_rate);
void adxl_read(AdxlSample &out);
