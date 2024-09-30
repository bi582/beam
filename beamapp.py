import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# Title of the application
st.title("Beam Support Reaction Solver with Simulation")

# Step 3: Input Section
st.header("Input Parameters")

# Beam length
beam_length = st.number_input("Enter the length of the beam (m):", min_value=0.0, step=0.1)

# Support positions
st.subheader("Support Positions")

# Hinge support position
hinge_position = st.number_input("Enter the position of the hinge support (m) from the left end:", min_value=0.0, max_value=beam_length, step=0.1)

# Roller support position
roller_position = st.number_input("Enter the position of the roller support (m) from the left end:", min_value=0.0, max_value=beam_length, step=0.1)

# Number of point loads
num_point_loads = st.number_input("Enter the number of point loads:", min_value=0, step=1)

# Number of UDLs (Uniformly Distributed Loads)
num_udls = st.number_input("Enter the number of UDLs:", min_value=0, step=1)

point_loads = []
point_positions = []

# For each point load, get the magnitude and position
if num_point_loads > 0:
    st.subheader("Point Loads and their positions")

for i in range(num_point_loads):
    point_load = st.number_input(f"Point Load {i+1} magnitude (N):", step=1.0)
    point_position = st.number_input(f"Point Load {i+1} position (m) from the left end:", min_value=0.0, max_value=beam_length, step=0.1)
    point_loads.append(point_load)
    point_positions.append(point_position)

udls = []
udl_start_positions = []
udl_end_positions = []

# For each UDL, get the magnitude and positions
if num_udls > 0:
    st.subheader("UDLs (Uniformly Distributed Loads) and their positions")

for i in range(num_udls):
    udl_magnitude = st.number_input(f"UDL {i+1} magnitude (N/m):", step=1.0)
    udl_start = st.number_input(f"UDL {i+1} start position (m) from the left end:", min_value=0.0, max_value=beam_length, step=0.1)
    udl_end = st.number_input(f"UDL {i+1} end position (m) from the left end:", min_value=udl_start, max_value=beam_length, step=0.1)
    udls.append(udl_magnitude)
    udl_start_positions.append(udl_start)
    udl_end_positions.append(udl_end)

# Step 4: Solver Logic for Support Reactions
if st.button("Calculate Reactions"):

    # Initialize total force and total moment
    total_force = 0
    total_moment_about_hinge = 0

    # Calculate contributions from point loads
    for i in range(len(point_loads)):
        total_force += point_loads[i]
        total_moment_about_hinge += point_loads[i] * (point_positions[i] - hinge_position)

    # Calculate contributions from UDLs
    for i in range(len(udls)):
        udl_length = udl_end_positions[i] - udl_start_positions[i]
        udl_force = udls[i] * udl_length
        total_force += udl_force
        # Moment arm for UDL is at the center of the UDL
        udl_position = (udl_start_positions[i] + udl_end_positions[i]) / 2
        total_moment_about_hinge += udl_force * (udl_position - hinge_position)

    # Solve for reaction at the roller support (vertical force only since roller can't take horizontal force)
    roller_reaction = total_moment_about_hinge / (roller_position - hinge_position)

    # Solve for reaction at the hinge support
    hinge_reaction = total_force - roller_reaction

    # Step 5: Output Section
    st.subheader("Calculated Reactions")
    st.write(f"Reaction at the hinge support (Ra): {hinge_reaction:.2f} N")
    st.write(f"Reaction at the roller support (Rb): {roller_reaction:.2f} N")

    # Step 6: Simulative Representation
    st.subheader("Beam Simulation")

    # Initialize the beam plot
    fig, ax = plt.subplots(figsize=(10, 2))

    # Plot the beam as a line
    ax.plot([0, beam_length], [0, 0], 'black', lw=5, label='Beam')

    # Plot the hinge and roller supports
    ax.plot(hinge_position, 0, 'go', markersize=12, label='Hinge Support')
    ax.plot(roller_position, 0, 'bo', markersize=12, label='Roller Support')

    # Plot point loads
    for i in range(len(point_loads)):
        ax.arrow(point_positions[i], 0.1, 0, -0.2, head_width=0.1, head_length=0.1, fc='r', ec='r', lw=2)
        ax.text(point_positions[i], 0.2, f'P{i+1}', ha='center', color='r')

    # Plot UDLs
    for i in range(len(udls)):
        x_udl = np.linspace(udl_start_positions[i], udl_end_positions[i], 100)
        y_udl = np.ones_like(x_udl) * 0.1
        ax.fill_between(x_udl, y_udl, 0, color='cyan', alpha=0.4, label=f'UDL {i+1}' if i == 0 else "")

    # Labels and legend
    ax.set_xlim(-0.5, beam_length + 0.5)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xlabel('Position along the beam (m)')
    ax.legend()

    # Display the plot
    st.pyplot(fig)
