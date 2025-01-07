# ai_to_old_car

---

## 1. Installation

---

### Install micropython on pico

- Download the UF2 file from the official website -> [MicroPython](https://micropython.org/download/rp2-pico/)
- Connect the Pico to your computer using a USB cable while holding down the BOOTSEL button.
- Drag and drop the UF2 file to the Pico drive that appears on your computer.

### Flash Jetson

- Install Jeston nano developer
  Kit -> [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- Download, install, and launch Etcher -> [Etcher](https://www.balena.io/etcher/)
- Click “Select image” and choose the zipped image file downloaded earlier.
- Insert your microSD card. If you have no other external drives attached, Etcher will automatically select the microSD
  card as target device. Otherwise, click “Change” and choose the correct device.
- Click “Flash!” Your OS may prompt for your username and password before it allows Etcher to proceed.

### Install Jetson

```bash
sudo apt-get update
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
````

### Configure Pin on Pico

- In `src/pico_script.const.py` add good pin for the motor

```python
BOTTOM_ARM_MOTOR_PIN = 16
TOP_ARM_MOTOR_PIN = 17
BRAKE_MOTOR_PIN = 18
ACCELERATOR_MOTOR_PIN = 19
...
```

## 2. Run

### Main

---

```bash
export PYTHONPATH=$(pwd)/src:$(pwd)
python3 main.py
```

### Test on video

---

```bash
export PYTHONPATH=$(pwd)/src:$(pwd)
python3 test/test_road_detection.py
```

### With docker

```bash
docker compose up -d
```

or 

```bash
docker compose -f docker-compose-prod.yml up -d
```

### Test pico script

```bash
cp ./RPI_PICO-20241129-v1.24.1.uf2 /media/user/RPI-RP2/
ampy --port /dev/ttyACM0 put src/pico_script/servo.py
ampy --port /dev/ttyACM0 put src/pico_script/const.py
ampy --port /dev/ttyACM0 run src/pico_script/*.py
```

## 3. Linter

---

```
black .
```