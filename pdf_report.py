import matplotlib.pyplot as plt
import csv
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def generate_and_save_graph_to_pdf(pdf_filename):
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
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed
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

    # Save the figure to a PDF file with the current date and time appended to the filename
    current_datetime = datetime.datetime.now()
    date_time_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    graph_pdf_filename = f'reports/emission_report_graph_{date_time_str}.pdf'
    fig.savefig(graph_pdf_filename)

    # Add a table below the graph with all companies and their emissions
    all_companies_energy = energy_sum
    all_companies_transportation = transportation_sum

    table_data = [['Company', 'Energy Emissions (kg CO2)', 'Transportation Emissions (kg CO2)']]
    for company, energy, transportation in zip(companies, all_companies_energy, all_companies_transportation):
        table_data.append([company, energy, transportation])

    # Create a PDF document for the emissions report
    report_pdf_filename = f'reports/emission_report_data_{date_time_str}.pdf'
    doc = SimpleDocTemplate(report_pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a table from the data
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    # Add the table to the document
    elements = [table]
    doc.build(elements)

