#pragma once
#include <stdint.h>

enum class Command {
    NONE,
    START,
    STOP,
    SET_RATE
};

struct ParsedCommand {
    Command type;
    uint32_t value;
};

bool protocol_parse_line(const char *line, ParsedCommand &out);
