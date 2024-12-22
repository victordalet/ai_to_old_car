# ai_to_old_car

---

## 1. Installation

---

### Install micropython on pico

- Download the UF2 file from the official website -> [MicroPython](https://micropython.org/download/rp2-pico/)
- Connect the Pico to your computer using a USB cable while holding down the BOOTSEL button.
- Drag and drop the UF2 file to the Pico drive that appears on your computer.

### Flash Jetson

- Install Jeston nano developer Kit -> [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- Download, install, and launch Etcher -> [Etcher](https://www.balena.io/etcher/)
- Click “Select image” and choose the zipped image file downloaded earlier.
- Insert your microSD card. If you have no other external drives attached, Etcher will automatically select the microSD card as target device. Otherwise, click “Change” and choose the correct device.
- Click “Flash!” Your OS may prompt for your username and password before it allows Etcher to proceed.


### Install Jetson
```bash
sudo apt-get update
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
````
## 2. Run

---

```bash
python3 main.py
```


## 3. Linter

---

```
black .
```