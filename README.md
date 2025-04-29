
# 🌱 LandLord: The Path of Least Resistance

**I’m not lazy; I just like to work smart, not hard.**  
I whipped up this little Python script in the comfort of my AC to avoid a summer-yard-rewiring marathon. It’s not perfect (the wire has dead spots and the mower sometimes needs a nudge), but hey—until I muster the courage (or get a base tan lol), this works well enough.

---

## 🚀 What It Does

- **Watches** your Worx Landroid boundary wire for "wire missing" errors.
- **Automatically** sends the mower home when it loses signal on the wire.
- **Restarts** the mower when the wire comes back.
- Handles **battery-temp errors** by rebooting the baseboard.

---

## 🛠️ Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/LandLord.git
   cd LandLord
   ```
2. Install dependencies:
   ```bash
   pip install pyworxcloud
   ```
3. Update `LandLord2.py` with your **EMAIL**, **PASSWORD**, and **SERIAL**.

---

## 🎉 Usage

```bash
chmod +x LandLord2.py
./LandLord2.py
```

The script will poll every 30 s. Ctrl‑C to stop.  
Slack integration? Maybe later—your app already yells when things break.

---

## 📋 TODO

- Automate zone nudges (if only the mower accepted more commands…)  
- Slack / email notifications  
- Real perimeter rewire (someday…)

---

*Made with ☕ by someone who loves efficiency more than yard work.*
