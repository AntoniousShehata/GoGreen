import matplotlib.pyplot as plt
import csv
from matplotlib import rcParams

# Set font properties globally
rcParams['font.family'] = 'Arial'
rcParams['font.size'] = 12

def generate_and_show_graph():
    companies = []
    energy_sum = []
    transportation_sum = []

    # Load data from the CSV file
    with open('emissions_data.csv', 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        # Skip the header row
        next(data)

        for row in data:
            companies.append(row[1])  # Company Name
            # Calculate total energy emissions for each company
            total_energy_emissions = round(sum(float(row[i]) for i in range(7, len(row))), 2)
            energy_sum.append(total_energy_emissions)
            # Calculate total transportation emissions for each company
            total_transportation_emissions = round(sum(float(row[i]) for i in range(3, 7)), 2)
            transportation_sum.append(total_transportation_emissions)

    # Find the top 10 companies by total emissions
    top_10_indices = sorted(range(len(energy_sum)), key=lambda i: energy_sum[i] + transportation_sum[i], reverse=True)[:10]
    top_10_companies = [companies[i] for i in top_10_indices]
    top_10_energy_sum = [energy_sum[i] for i in top_10_indices]
    top_10_transportation_sum = [transportation_sum[i] for i in top_10_indices]

    # Plotting code for the top 10 companies
    fig, ax = plt.subplots()
    x = range(len(top_10_companies))
    bar_width = 0.35

    ax.bar(x, top_10_energy_sum, color='b', width=bar_width, label='Energy Emissions')
    ax.bar([i + bar_width for i in x], top_10_transportation_sum, color='r', width=bar_width, label='Transportation Emissions')

    ax.set_xlabel('Company Name')
    ax.set_ylabel('Total Emissions (kg CO2)')
    ax.set_title('Total Emissions by Top 10 Companies')
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(top_10_companies, rotation=45, ha='right')
    ax.legend()

    # Annotate each bar with its value
    for i in x:
        ax.text(i, top_10_energy_sum[i], str(top_10_energy_sum[i]), ha='center', va='bottom')
        ax.text(i + bar_width, top_10_transportation_sum[i], str(top_10_transportation_sum[i]), ha='center', va='bottom')

    return fig
