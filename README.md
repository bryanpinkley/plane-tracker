# plane-tracker
A small project that will tell you where the plane flying above you is going.

## Intro
Have you ever looked at a plane in the sky and wonderered, where is that plane going? Or have you ever heard a loud plane and wondered, is that a frickin 747? Well I have, and I wanted to create a little Raspberry Pi project to tell me what those planes are. 

This project is inspired by Sozora's Flight Radar [project](https://sozorablog.com/flightradar/), which can be found on their blog. Note that the blog is in Japanese. I have developed on their code and instructions for my project.

## Setup
Most commercial airplanes broadcast ADS-B data, which provides plane IDs, flight number, location, altitude, and speed, amongst other things. To capture this data, we will use a Raspberry Pi with a ADS-B receiver.

Before we begin, you will need this equipment:
- Raspberry Pi. In my case, I am using a Raspberry Pi 4.
- An ADS-B receiver. This is the one I got on [Amazon](https://a.co/d/b94NCPA).

### Settting up the Raspberry Pi
You can follow [FlightAware's](https://www.flightaware.com/adsb/piaware/install) instructions directly to set up the device. 

Note that it seems like the link for Step 7, claiming your PiAware device, does not work. Instead, you can follow their instructions to [manually claim PiAware](https://support.flightaware.com/hc/en-us/articles/31093377447831-Manually-Claim-PiAware).