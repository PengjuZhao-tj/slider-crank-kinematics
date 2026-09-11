# -*- coding: utf-8 -*-
"""
Slider-crank mechanism: kinematic analysis
曲柄滑块机构运动学分析
"""

import numpy as np
import matplotlib.pyplot as plt


# 1. Mechanism parameters
r = 0.04       # Crank radius, m
l = 0.12       # Connecting rod length, m
rpm = 600      # Crank rotational speed, r/min

if l <= r:
    raise ValueError(
        "Connecting rod length must be greater than crank radius."
    )


# 2. Crank angle and time
theta_deg = np.linspace(0, 360, 1441)
theta = np.deg2rad(theta_deg)

omega = 2 * np.pi * rpm / 60
time = theta / omega


# 3. Slider position
x = (
    r * np.cos(theta)
    + np.sqrt(l**2 - (r * np.sin(theta))**2)
)

# Displacement measured from the right dead center
s = (r + l) - x


# 4. Numerical velocity and acceleration
velocity = np.gradient(s, time, edge_order=2)
acceleration = np.gradient(velocity, time, edge_order=2)


# 5. Print calculation results
print("Crank radius: %.1f mm" % (r * 1000))
print("Connecting rod length: %.1f mm" % (l * 1000))
print("Rotational speed: %.1f r/min" % rpm)
print("Angular velocity: %.2f rad/s" % omega)
print("Slider stroke: %.1f mm" % (
    (np.max(x) - np.min(x)) * 1000
))
print("Maximum velocity: %.3f m/s" % np.max(np.abs(velocity)))
print("Maximum acceleration: %.3f m/s^2" % (
    np.max(np.abs(acceleration))
))


# 6. Plot kinematic curves
fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True)

axes[0].plot(
    theta_deg,
    s * 1000,
    color="blue",
    linewidth=2
)
axes[0].set_ylabel("Displacement (mm)")
axes[0].set_title("Slider-Crank Mechanism Kinematic Analysis")

axes[1].plot(
    theta_deg,
    velocity,
    color="green",
    linewidth=2
)
axes[1].set_ylabel("Velocity (m/s)")

axes[2].plot(
    theta_deg,
    acceleration,
    color="red",
    linewidth=2
)
axes[2].set_xlabel("Crank Angle (degree)")
axes[2].set_ylabel("Acceleration (m/s^2)")

for ax in axes:
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xlim(0, 360)
    ax.set_xticks(np.arange(0, 361, 45))

plt.tight_layout()
plt.savefig("kinematic_curves.png", dpi=300)
plt.show()