
import matplotlib.pyplot as plt

# === CONFIGURATION ===
layer_thicknesses_mils = [0.4, 1.4, 12.6, 1.4, 0.4]  # Modify as needed

# Convert mils to mm
layer_thicknesses_mm = [t * 0.0254 for t in layer_thicknesses_mils]

# Colors alternate: copper = orange, insulator = green
colors = [ "green" if i % 2 == 0 else "orange" for i in range(len(layer_thicknesses_mm))]

# Calculate positions
positions = [0]
for t in layer_thicknesses_mm[:-1]:
    positions.append(positions[-1] + t)

# === Dynamic figure size based on total thickness ===
total_height_mm = sum(layer_thicknesses_mm)
fig_height = max(6, total_height_mm * 2)  # Scale figure height
fig, ax = plt.subplots(figsize=(3, fig_height))

# Plot layers
for i, (pos, thickness) in enumerate(zip(positions, layer_thicknesses_mm)):
    ax.bar(x=0, height=thickness, width=0.5, bottom=pos, color=colors[i], edgecolor="black")
    ax.text(0.6, pos + thickness / 2, f"{layer_thicknesses_mils[i]} mil", ha="left", va="center", fontsize=8)

# Adjust axis with extra padding
ax.set_ylim(-total_height_mm * 0.05, total_height_mm * 1.05)  # Add padding below and above
ax.set_xlim(-1, 2)
ax.axis("off")

# Title
plt.title("Stackup REAL thickness", fontsize=12)

# Adjust layout
plt.tight_layout()
fig.subplots_adjust(top=0.95, bottom=0.05)

# === Save ===
#output_file = "pcb_stackup_vertical.png"
#plt.savefig(output_file, dpi=300)
#print(f"Saved visualization as {output_file}")

# Show plot
plt.show()
