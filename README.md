# whiskey

Project to build an illuminated bar using neopixels 
where you can highlight bottles given some filters,
e.g. origin, flavour profile, age, ...

## Technology

Hardware will consist of several Neopixel Jewell 7 LED rings,
one for each bottle and a raspberry pi 0.

See this link for how to connect pixels to the pi, it needs
a level shifter to shift the 3.3 V logic signal of the pi to
the 5 V signal needed by the pixels:
https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring#raspberry-pi-wiring-with-level-shifting-chip-3006459

As currently, pi 0 are not really easy to get and we don't have one yet,
development is for now done on a raspberry pi 4.

Unfortunately, the GPIO pin that can talk to the pixels (D21),
requires root permissions to be used.
This is why we have a long running python service that runs as root
that receives commands (set colors, set patterns, etc.) via a redis queue.

Software side is django for the backend using sqlite, svelte for the frontend.

Project setup for the django/svelte combination taken from:
https://dev.to/besil/my-django-svelte-setup-for-fullstack-development-3an8
