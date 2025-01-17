import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Define GPIO pins
TRIG = 17
ECHO = 27
led = 22
m11 = 16
m12 = 12
m21 = 21
m22 = 20

# Setup GPIO pins
GPIO.setup(TRIG, GPIO.OUT)  # Set TRIG as output
GPIO.setup(ECHO, GPIO.IN)  # Set ECHO as input
GPIO.setup(led, GPIO.OUT)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

# Initialize LED
GPIO.output(led, 1)
time.sleep(5)

# Motor control functions
def stop():
    print('Stop')
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Forward')

def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print('Back')

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Left')

def right():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print('Right')

# Main loop
count = 0

try:
    while True:
        avgDistance = 0

        # Measure distance 5 times and calculate average
        for _ in range(5):
            GPIO.output(TRIG, False)  # Set TRIG as LOW
            time.sleep(0.1)  # Delay
            GPIO.output(TRIG, True)  # Set TRIG as HIGH
            time.sleep(0.00001)  # Delay of 10 microseconds
            GPIO.output(TRIG, False)  # Set TRIG as LOW

            # Wait for ECHO to go HIGH
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            # Wait for ECHO to go LOW
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            # Calculate distance
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150  # Distance in cm
            avgDistance += distance

        avgDistance = avgDistance / 5
        avgDistance = round(avgDistance, 2)
        print(f"Average Distance: {avgDistance} cm")

        # Obstacle detection and action
        if avgDistance < 25:  # If obstacle is within 25 cm
            count += 1
            stop()
            time.sleep(1)
            back()
            time.sleep(1.5)

            if (count % 3 == 1):
                right()
            else:
                left()
            
            time.sleep(1.5)
            stop()
            time.sleep(1)
        else:
            forward()

except KeyboardInterrupt:
    print("Exiting program")
    stop()
    GPIO.cleanup()
