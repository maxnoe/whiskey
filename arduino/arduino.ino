#include <Adafruit_NeoPixel.h>

const int PIN = 6;

const int N_PIXELS_RING = 7;
const int N_RINGS = 2;
const int N_PIXELS = N_PIXELS_RING * N_RINGS;

Adafruit_NeoPixel pixels(N_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

const auto OFF = pixels.Color(0, 0, 0);
const auto MAX = pixels.Color(255, 255, 255);

const auto RED = pixels.Color(64, 0, 0);
const auto GREEN = pixels.Color(0, 64, 0);
const auto BLUE = pixels.Color(0, 0, 64);

uint32_t colors[N_PIXELS];


enum class Command : uint8_t {
    OFF = 0,
    ON = 1,
    GET = 2,
    SET_PIX = 3,
    SET_ALL = 4,
};

struct RGB {
    uint8_t r;
    uint8_t g;
    uint8_t b;

    RGB() = default;
    RGB(uint32_t color) {
        r = (color & (0xfful << 16)) >> 16;
        g = (color & (0xfful << 8)) >> 8;
        b = color & 0xfful;
    }
};

bool on = true;


uint32_t white(float intensity) {
    auto value = static_cast<uint8_t>(255 * intensity);
    return pixels.Color(value, value, value);
}


void all_off() {
    for (int i=0; i < N_PIXELS; i++) {
        pixels.setPixelColor(i, OFF);
    }
    pixels.show();
}

void set_color() {
    for (int i=0; i < N_PIXELS; i++) {
        pixels.setPixelColor(i, colors[i]);
    }
    pixels.show();
}

void setup() {
    pixels.begin();

    for (int pixel=0; pixel < N_PIXELS; pixel++) {
        colors[pixel] = RED;
    }

    set_color();

    Serial.begin(115200);
    while (!Serial) delay(10);
}

void serialEvent() {
    auto val = Serial.read();
    auto command = static_cast<Command>(val);

    int n = 0;
    uint8_t pix = 0;
    uint8_t color[3] = {0, 0, 0};
    RGB rgb;

    switch (command) {
        case Command::OFF:
            all_off();
            on = false;
            Serial.println("ok: OFF");
            break;
        case Command::ON:
            set_color();
            on = true;
            Serial.println("ok: ON");
            break;
        case Command::GET:
            Serial.print("ok: {\"on\":");
            Serial.print(on ? "true" : "false");
            Serial.print(",\"colors\":[");
            for (int i=0; i < N_PIXELS; i++) {
                rgb = RGB{colors[i]};
                Serial.print("[");
                Serial.print(rgb.r);
                Serial.print(",");
                Serial.print(rgb.g);
                Serial.print(",");
                Serial.print(rgb.g);
                Serial.print("]");
                if ((i + 1) < N_PIXELS) {
                    Serial.print(",");
                }
            }
            Serial.println("]}");
            break;
        case Command::SET_PIX:
            n = Serial.readBytes(reinterpret_cast<char*>(&pix), sizeof(pix));
            // timeout
            if (n == 0) {
                Serial.println("error: timeout getting pixel");
                break;
            }
            n = Serial.readBytes(reinterpret_cast<char*>(&color), sizeof(color));
            // timeout
            if (n != sizeof(color)) {
                Serial.println("error: timeout getting color");
                break;
            }
            if (pix >= N_PIXELS) {
                Serial.println("error: out of bounds");
                break;
            }
            colors[pix] = pixels.Color(color[0], color[1], color[2]);
            Serial.println("ok: SET_PIX");
            set_color();
            break;
        case Command::SET_ALL:
            for (int pix=0; pix < N_PIXELS; pix++) {
                n = Serial.readBytes(reinterpret_cast<char*>(&color), sizeof(color));
                // timeout
                if (n != sizeof(color)) {
                    Serial.println("error: timeout getting color");
                    break;
                }
                colors[pix] = pixels.Color(color[0], color[1], color[2]);
            }
            set_color();
            Serial.println("ok: SET_ALL");
            break;
        default:
            Serial.println("error: unknown command");
            while (Serial.available() > 0) {
                Serial.read();
            }
            break;
    }
}

void loop() {
}
