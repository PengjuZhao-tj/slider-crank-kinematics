# -*- coding: utf-8 -*-
"""
Slider-crank mechanism: position analysis
曲柄滑块机构位置分析
"""

import numpy as np
import matplotlib.pyplot as plt


# 1. Mechanism parameters
r = 0.04       # Crank radius, m
l = 0.12       # Connecting rod length, m

# The connecting rod must be longer than the crank
if l <= r:
    raise ValueError("Connecting rod length must be greater than crank radius.")


# 2. Crank angle
theta_deg = np.linspace(0, 360, 721)
theta = np.deg2rad(theta_deg)


# 3. Slider position
x = (
    r * np.cos(theta)
    + np.sqrt(l**2 - (r * np.sin(theta))**2)
)

# Displacement measured from the right dead center
s = (r + l) - x


# 4. Print calculation results
print("Crank radius: %.1f mm" % (r * 1000))
print("Connecting rod length: %.1f mm" % (l * 1000))
print("Slider stroke: %.1f mm" % ((np.max(x) - np.min(x)) * 1000))
print("Maximum displacement: %.1f mm" % (np.max(s) * 1000))


# 5. Plot displacement curve
plt.figure(figsize=(9, 5))
plt.plot(theta_deg, s * 1000, color="blue", linewidth=2)

plt.title("Slider Displacement vs. Crank Angle")
plt.xlabel("Crank Angle (degree)")
plt.ylabel("Slider Displacement (mm)")
plt.xlim(0, 360)
plt.xticks(np.arange(0, 361, 45))
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("position_curve.png", dpi=300)
plt.show()