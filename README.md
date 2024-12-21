# ai_to_old_car

---

## 1. Installation

---

### Flash Jetson

- Install Jeston nano developer Kit -> [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- Download, install, and launch Etcher -> [Etcher](https://www.balena.io/etcher/)
- Click “Select image” and choose the zipped image file downloaded earlier.
- Insert your microSD card. If you have no other external drives attached, Etcher will automatically select the microSD card as target device. Otherwise, click “Change” and choose the correct device.
- Click “Flash!” Your OS may prompt for your username and password before it allows Etcher to proceed.


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