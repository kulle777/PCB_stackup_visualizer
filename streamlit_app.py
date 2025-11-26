import streamlit as st
import matplotlib.pyplot as plt
import io

st.title("PCB Stackup Visualization")

user_input = st.text_input(
    "Enter layer thicknesses (comma-separated) starting from soldermask:",
    "0.01,0.0175,0.1960,0.0350,1.0300,0.0350,0.1960,0.0175,0.01"
)
# Toggle to hide/show top & bottom thickness values
hide_ends = st.toggle("Hide soldermask (top,bot)", value=True)

# Suffix text to append to each label
label_suffix = st.text_input("Append any text to each layer label (optional):", "mm")

st.text('Press "enter" to calculate. Download available at bottom.')

# Convert input string to list of floats
try:
    layer_thicknesses = [float(x.strip()) for x in user_input.split(",") if x.strip()]
except ValueError:
    st.error("Please enter valid numbers separated by commas.")
    st.stop()

# Colors alternate: copper = orange, insulator = green
colors = ["green" if i % 2 == 0 else "orange" for i in range(len(layer_thicknesses))]

# Calculate positions
positions = [0]
for t in layer_thicknesses[:-1]:
    positions.append(positions[-1] + t)

# Dynamic figure size (smaller for app)
total_height_mm = sum(layer_thicknesses)
fig_height = min(8, max(4, total_height_mm * 0.5))  # Keep between 4 and 8 inches
fig, ax = plt.subplots(figsize=(3, fig_height))

# Plot layers
for i, (pos, thickness) in enumerate(zip(positions, layer_thicknesses)):
    ax.bar(x=0, height=thickness, width=0.5, bottom=pos, color=colors[i], edgecolor="black")

    # Build label: thickness plus optional suffix (with a leading space only if suffix exists)
    label = f"{layer_thicknesses[i]}{(' ' + label_suffix) if label_suffix else ''}"

    # Conditionally show label based on toggle
    if not (hide_ends and (i == 0 or i == len(layer_thicknesses) - 1)):
        ax.text(0.6, pos + thickness / 2, label, ha="left", va="center", fontsize=8)

# Adjust axis
ax.set_ylim(-total_height_mm * 0.05, total_height_mm * 1.05)
ax.set_xlim(-1, 2)
ax.axis("off")

plt.tight_layout()
fig.subplots_adjust(top=0.95, bottom=0.05)

# Show plot in Streamlit
st.pyplot(fig)

# Save figure to buffer for download
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300)
buf.seek(0)

# Download button
st.download_button(
    label="Download Image",
    data=buf,
    file_name="pcb_stackup.png",
    mime="image/png"
)
st.text("Creator: Kalle Paasio,\nhttps://github.com/kulle777/PCB_stackup_visualizer\n\n")
st.text("I add some keywords, so google might find this one day: \n pcb, stackup, layer, height, "
        "thickness, real, 1to1, 1:1, visual, visualize, represent, layout, copper, dielectric,"
        " cross-section, multilayer, diagram ")

st.text('')
