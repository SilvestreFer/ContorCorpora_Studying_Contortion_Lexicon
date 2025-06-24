import matplotlib.pyplot as plt

# Data
labels = ['Portuguese', 'English']
values = [430, 24]
total = sum(values)
percentages = [v / total * 100 for v in values]

# Colors
colors = ['lightgreen', 'beige']

# Plot
fig, ax = plt.subplots()
ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.set_title('Uso de UL em PT-BR no ContorCorpora')

plt.show()
