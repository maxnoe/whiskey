import board
import neopixel
import time
import math

PIN = board.D21

OFF = (0, 0, 0)
RED = (0xff, 0, 0)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0xff)

N_JEWELL = 2
N_PIX_JEWELL = 7
N = N_JEWELL * N_PIX_JEWELL
PIXELS = neopixel.NeoPixel(PIN, N, auto_write=False, brightness=1.0)


def all_off(pixels=PIXELS):
    pixels.fill(OFF)
    pixels.show()


def sine_wave(pixels, period, basecolor=(0xff, 0xff, 0xff)):
    t = time.time()
    intensity = 0.5 * (1 + math.sin(2 * math.pi * t / period))
    color = tuple(int(intensity * c) for c in basecolor)
    pixels.fill(color)


def clock(pixels, period):
    t = (time.time() % period) / period
    idx = 1 + int((N_PIX_JEWELL - 1) * t)
    pixels.fill(OFF)

    for jewell in range(N_JEWELL):
        pixels[jewell * N_PIX_JEWELL + idx] = (0, 0, 0x10)


def main(pause=0.001):
    while True:
        clock(PIXELS, period=1)
        PIXELS.show()
        time.sleep(pause)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        all_off()
        print()
