import matplotlib.pyplot as plt

# Data: (English term, English occurrences, Portuguese term, Portuguese occurrences)
terms = [
    ("chest stand / cheststand", 0, "queixinho / mata borrão / borrão", 15),
    ("elbow stand / elbowstand", 0, "parada de cotovelo", 11),
    ("handstand", 0, "parada de mão", 13),
    ("backbend", 6, "poses de coluna / posição de coluna", 1),
    ("bridge", 1, "ponte", 182),
    ("triple fold / triplefold", 8, "dobre triplo", 0),
    ("cobra", 13, "cobrinha", 2),
    ("split", 8, "espacate / espacata / espacato", 158),
    ("oversplit", 1, "espacate negativo / negativado", 3),
    ("front split", 0, "espacate frontal", 40),
    ("middle split", 0, "espacate lateral / abertura de segunda / abertura lateral", 7),
]

# Colors for pie chart
colors = ["beige", "lightgreen"]

# Create subplots with 4 rows and 3 columns
fig, axs = plt.subplots(4, 3, figsize=(14, 14))
fig.subplots_adjust(hspace=2.0, wspace=0.5)  # Add space between charts

# Flatten axes for easy indexing
axs = axs.flatten()

# Plot pie charts
for i in range(12):
    if i < len(terms):
        en_term, en_count, pt_term, pt_count = terms[i]
        total = en_count + pt_count
        en_pct = (en_count / total) * 100 if total else 0
        pt_pct = (pt_count / total) * 100 if total else 0
        data = [en_pct, pt_pct]
        labels = ["EN", "PT"]
        axs[i].pie(data, labels=labels, colors=colors, autopct="%.1f%%", startangle=90)
        axs[i].set_title(f"{en_term}\nvs.\n{pt_term}", fontsize=9)
    else:
        axs[i].axis("off")  # Hide extra plots if needed

# Center the last two charts by hiding the first and last axes in the bottom row
axs[9].axis("off")  # hide leftmost
axs[11].axis("off")  # hide rightmost

plt.suptitle("Relative Frequency of Contortion Terms in English and Portuguese", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
