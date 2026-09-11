# -*- coding: utf-8 -*-
"""
Slider-crank mechanism parameter comparison
曲柄滑块机构参数对比分析
"""

import csv
import numpy as np
import matplotlib.pyplot as plt


def calculate_displacement(theta, crank_radius, rod_length):
    """Calculate slider displacement from right dead center."""

    if rod_length <= crank_radius:
        raise ValueError(
            "Connecting rod length must be greater than crank radius."
        )

    slider_position = (
        crank_radius * np.cos(theta)
        + np.sqrt(
            rod_length**2
            - (crank_radius * np.sin(theta))**2
        )
    )

    displacement = (
        crank_radius
        + rod_length
        - slider_position
    )

    return displacement


# Crank angle
theta_deg = np.linspace(0, 360, 1441)
theta = np.deg2rad(theta_deg)


# 1. Effect of crank radius
crank_radius_values = [0.03, 0.04, 0.05]
fixed_rod_length = 0.12


# 2. Effect of connecting rod length
rod_length_values = [0.08, 0.12, 0.16]
fixed_crank_radius = 0.04


# 3. Effect of rotational speed
rpm_values = np.array([300, 600, 900])
base_displacement = calculate_displacement(
    theta,
    fixed_crank_radius,
    fixed_rod_length
)

maximum_velocity = []
maximum_acceleration = []

for rpm in rpm_values:
    omega = 2 * np.pi * rpm / 60
    time = theta / omega

    velocity = np.gradient(
        base_displacement,
        time,
        edge_order=2
    )

    acceleration = np.gradient(
        velocity,
        time,
        edge_order=2
    )

    maximum_velocity.append(
        np.max(np.abs(velocity))
    )

    maximum_acceleration.append(
        np.max(np.abs(acceleration))
    )


# 4. Export speed comparison data
with open(
    "speed_parameter_summary.csv",
    "w",
    newline=""
) as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([
        "Rotational Speed (rpm)",
        "Maximum Velocity (m/s)",
        "Maximum Acceleration (m/s^2)"
    ])

    for rpm, velocity, acceleration in zip(
        rpm_values,
        maximum_velocity,
        maximum_acceleration
    ):
        writer.writerow([
            rpm,
            "%.4f" % velocity,
            "%.4f" % acceleration
        ])


# 5. Plot parameter comparison
fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)

# Crank radius comparison
for radius in crank_radius_values:
    displacement = calculate_displacement(
        theta,
        radius,
        fixed_rod_length
    )

    axes[0, 0].plot(
        theta_deg,
        displacement * 1000,
        linewidth=2,
        label="r = %.0f mm" % (radius * 1000)
    )

axes[0, 0].set_title("Effect of Crank Radius")
axes[0, 0].set_xlabel("Crank Angle (degree)")
axes[0, 0].set_ylabel("Displacement (mm)")
axes[0, 0].legend()


# Connecting rod length comparison
for rod_length in rod_length_values:
    displacement = calculate_displacement(
        theta,
        fixed_crank_radius,
        rod_length
    )

    axes[0, 1].plot(
        theta_deg,
        displacement * 1000,
        linewidth=2,
        label="l = %.0f mm" % (rod_length * 1000)
    )

axes[0, 1].set_title("Effect of Connecting Rod Length")
axes[0, 1].set_xlabel("Crank Angle (degree)")
axes[0, 1].set_ylabel("Displacement (mm)")
axes[0, 1].legend()


# Rotational speed and maximum velocity
axes[1, 0].plot(
    rpm_values,
    maximum_velocity,
    "o-",
    color="green",
    linewidth=2
)

axes[1, 0].set_title("Speed vs. Maximum Slider Velocity")
axes[1, 0].set_xlabel("Rotational Speed (r/min)")
axes[1, 0].set_ylabel("Maximum Velocity (m/s)")


# Rotational speed and maximum acceleration
axes[1, 1].plot(
    rpm_values,
    maximum_acceleration,
    "o-",
    color="red",
    linewidth=2
)

axes[1, 1].set_title("Speed vs. Maximum Slider Acceleration")
axes[1, 1].set_xlabel("Rotational Speed (r/min)")
axes[1, 1].set_ylabel("Maximum Acceleration (m/s^2)")


for ax in axes.flat:
    ax.grid(True, linestyle="--", alpha=0.6)

fig.suptitle(
    "Slider-Crank Mechanism Parameter Comparison",
    fontsize=15
)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("parameter_comparison.png", dpi=300)
plt.show()


# 6. Print engineering conclusions
print("Parameter comparison completed.")
print("Conclusion 1: Increasing crank radius increases slider stroke.")
print("Conclusion 2: Rod length changes the displacement curve shape.")
print("Conclusion 3: Speed increases velocity and acceleration.")
print("Data saved: speed_parameter_summary.csv")


