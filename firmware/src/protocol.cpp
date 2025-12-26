#include "protocol.h"
#include <Arduino.h>
#include <string.h>

bool protocol_parse_line(const char *line, ParsedCommand &out) {
    out.type = Command::NONE;
    out.value = 0;

    if (strcmp(line, "START") == 0) {
        out.type = Command::START;
        return true;
    }

    if (strcmp(line, "STOP") == 0) {
        out.type = Command::STOP;
        return true;
    }

    if (strncmp(line, "SET_RATE ", 9) == 0) {
        uint32_t rate = atoi(line + 9);
        if (rate >= 1 && rate <= 3200) {
            out.type = Command::SET_RATE;
            out.value = rate;
            return true;
        }
    }

    return false;
}