import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import utils
from graph_emission import generate_and_show_graph
import os
import shutil

class CustomApplication(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default font for the entire application
        self.default_font = ("Arial", 18)
        self.apply_default_font(self)
   
    def apply_default_font(self, widget):
        if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Text,tk.Listbox)):
            widget.config(font=self.default_font)
            if isinstance(widget, tk.Text):
                self.center_text(widget)
        for child in widget.winfo_children():
            self.apply_default_font(child)

    def center_text(self, text_widget):
        # Create a tag named 'center' and configure it to center the text
        text_widget.tag_configure("center", justify='center')
        # Apply the 'center' tag to all text in the widget
        text_widget.tag_add("center", "1.0", "end")

class EmissionsDataApp(CustomApplication):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("Emissions Data Management")

        # Set fullscreen
        #master.attributes("-fullscreen", True)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Add tabs for different sections
        self.add_data_tab()
        self.retrieve_data_tab()
        self.delete_data_tab()
        self.show_graph_data_tab()
        self.show_index_data_tab()
        self.pdf_data_tab()

        # Apply default font to all widgets
        self.apply_default_font(master)

        self.notebook.bind("<<NotebookTabChanged>>", self.refresh_data)

    def add_data_tab(self):
        # Tab for adding emissions data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Add Data')

        # Company ID entry
        company_id_label = tk.Label(tab, text="Company ID:")
        company_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.company_id_entry = tk.Entry(tab)
        self.company_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Company Name entry
        company_name_label = tk.Label(tab, text="Company Name:")
        company_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.company_name_entry = tk.Entry(tab)
        self.company_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Transportation methods entry
        self.transportation_label = tk.Label(tab, text="Sum Transportation Emissions(Euros/Month):")
        self.transportation_label.grid(row=2, column=0, padx=5, pady=5)
        self.transportation_entries = []
        for i, method in enumerate(['Car', 'Bus', 'Train', 'Bicycle', 'Walking'], start=3):
            label = tk.Label(tab, text=method)
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(tab)
            entry.grid(row=i, column=1, padx=5, pady=5)
            # Check if the method is 'Bicycle' or 'Walking'
            if method in ['Bicycle', 'Walking']:
                entry.insert(0, "0")  # Insert '0' for Bicycle and Walking
                entry.configure(state='disabled')  # Disable the entry
            self.transportation_entries.append(entry)

        # Energy sources entry
        self.energy_label = tk.Label(tab, text="Sum Energy Source Emissions(Euros/Month):")
        self.energy_label.grid(row=8, column=0, padx=5, pady=5)
        self.energy_entries = []
        for j, source in enumerate(['Electricity', 'Natural Gas', 'Fuel Oil', 'Propane', 'Coal'], start=9):
            label = tk.Label(tab, text=source)
            label.grid(row=j, column=0, padx=5, pady=5)
            entry = tk.Entry(tab)
            entry.grid(row=j, column=1, padx=5, pady=5)
            self.energy_entries.append(entry)

        # Add Emissions Data button
        add_button = tk.Button(tab, text="Add Emissions Data", command=self.add_data)
        add_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

    def retrieve_data_tab(self):
        # Tab for retrieving emissions data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Retrieve Data')

        # Company ID entry
        company_id_label = tk.Label(tab, text="Company ID:")
        company_id_label.grid(row=1, column=0, padx=5, pady=5)
        self.retrieve_company_id_entry = tk.Entry(tab)
        self.retrieve_company_id_entry.grid(row=1, column=1, padx=5, pady=5)

        # Retrieve Data button
        retrieve_button = tk.Button(tab, text="Retrieve Data", command=self.display_retrieved_data)
        retrieve_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Display retrieved data
        self.retrieved_data_text = tk.Text(tab, wrap="word", height=10, width=50)
        self.retrieved_data_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for displaying reports
        self.report_frame = ttk.Frame(tab)
        self.report_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Text widget for displaying reports
        self.reports_text = tk.Text(self.report_frame, wrap="word", height=10, width=80)
        self.reports_text.grid(row=0, column=0, padx=5, pady=5)

    def delete_data_tab(self):
        # Tab for deleting emissions data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Delete Data')

        # Company ID entry
        company_id_label = tk.Label(tab, text="Company ID:")
        company_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.delete_company_id_entry = tk.Entry(tab)
        self.delete_company_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Delete Data button
        delete_button = tk.Button(tab, text="Delete Data", command=self.delete_data)
        delete_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def show_graph_data_tab(self, event=None):
        # Tab for displaying graph data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Graph Data')

        
        # Generate and display the graph in the tab
        graph = generate_and_show_graph()  # Call the function to generate the graph
        canvas = FigureCanvasTkAgg(graph, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
    
    def show_index_data_tab(self):
        # Tab for displaying index data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Index Data')

        # Create a treeview widget
        self.tree = ttk.Treeview(tab, columns=("Company ID", "Company Name"), show="headings")
        self.tree.heading("Company ID", text="Company ID")
        self.tree.heading("Company Name", text="Company Name")


        # Apply font, center alignment, and row height to the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 18), anchor="center")
        style.configure("Treeview", font=("Arial", 18), rowheight=30)

        # Set up the background color of all cells to blue
        style.map("Treeview", background=[("selected", "blue")])


        # Set up the border around each cell to simulate grid lines
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove cell borders
        #style.layout("Treeview.Heading", [('Treeview.heading.treearea', {'sticky': 'nswe'})])  # Remove header borders

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Sample data (replace with your actual data)
        data = [
            ("1", "Company A"),
            ("2", "Company B"),
            ("3", "Company C")
        ]

        # Insert data into the treeview
        for item in data:
            self.tree.insert("", tk.END, values=item)

    def pdf_data_tab(self):
        # Tab for displaying PDF data
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='PDF Data')

        # Create a Listbox widget to display available PDF reports
        self.reports_listbox = tk.Listbox(tab, selectmode=tk.SINGLE)
        self.reports_listbox.pack(fill=tk.BOTH, expand=True)

        # Populate the Listbox with available PDF reports
        reports_directory = 'reports'  # Update with your directory containing PDF files
        
        # Get a list of tuples containing (filename, creation_time)
        files_with_time = [(filename, os.path.getctime(os.path.join(reports_directory, filename))) 
                            for filename in os.listdir(reports_directory) 
                            if filename.endswith('.pdf')]
        
        # Sort the list of files by creation time in descending order
        sorted_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)
        
        # Add the sorted filenames to the Listbox
        for filename, _ in sorted_files:
            self.reports_listbox.insert(tk.END, filename)

        # Create a button to download the selected file
        download_button = tk.Button(tab, text="Download Selected", command=self.download_selected)
        download_button.pack()

    def download_selected(self):
        # Get the selected PDF filename
        selected_index = self.reports_listbox.curselection()
        if selected_index:
            selected_filename = self.reports_listbox.get(selected_index[0])
            # Prompt user to choose download location
            download_dir = filedialog.askdirectory(title="Select Download Location")
            if download_dir:
                # Construct source and destination paths
                source_path = os.path.join('reports', selected_filename)
                destination_path = os.path.join(download_dir, selected_filename)
                # Copy the file to the destination
                try:
                    shutil.copyfile(source_path, destination_path)
                    messagebox.showinfo("Download Successful", f"{selected_filename} downloaded successfully.")
                except Exception as e:
                    messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")
   
    def add_data(self):
        # Functionality to add emissions data
        company_id = self.company_id_entry.get()
        company_name = self.company_name_entry.get()
        if not company_id or not company_name:
            messagebox.showerror("Error", "Company ID and Company Name are required.")
            return

        # Transportation data
        transportation_data = [entry.get() for entry in self.transportation_entries]

        # Energy source data
        energy_data = [entry.get() for entry in self.energy_entries]

        data = {'ID': company_id, 'Name': company_name}
        data.update({method: value for method, value in zip(['Car', 'Bus', 'Train', 'Bicycle', 'Walking'], transportation_data)})
        data.update({source: value for source, value in zip(['Electricity', 'Natural Gas', 'Fuel Oil', 'Propane', 'Coal'], energy_data)})

        utils.store_emissions_data(data)
    
    def delete_data(self):
        # Functionality to delete emissions data
        company_id = self.delete_company_id_entry.get()
        utils.delete_emissions_data_by_id(company_id)
   
    def display_retrieved_data(self):
        # Functionality to retrieve and display emissions data

        company_id = self.retrieve_company_id_entry.get()
        retrieved_data_text = self.retrieved_data_text
        reports_text = self.reports_text
        utils.retrieve_emissions_data_by_id(company_id, retrieved_data_text, reports_text)

    def display_reports(self, report_data):
        # Display the reports using the reports text widget
        self.reports_text.delete(1.0, tk.END)  # Clear previous content
        self.reports_text.insert(tk.END, report_data)

    def refresh_data(self, event=None):
        # Call the appropriate refresh method based on the selected tab
        selected_tab = self.notebook.index("current")
        if selected_tab == 0:  # Add Data tab
            pass  # No refresh needed for Add Data tab
        elif selected_tab == 1:  # Retrieve Data tab
            pass  # No refresh needed for Retrieve Data tab
        elif selected_tab == 2:  # Delete Data tab
            pass  # No refresh needed for Delete Data tab
        elif selected_tab == 3:  # Graph Data tab
            self.refresh_graph_data()
        elif selected_tab == 4:  # Index Data tab
            self.refresh_index_data()
        elif selected_tab == 5:  # Pdf Data tab
            self.refresh_pdf_data()

    def refresh_graph_data(self, event=None):
        # Refresh the graph when switching to the "Graph Data" tab
        tab_index = self.notebook.index("current")
        tab_text = self.notebook.tab(tab_index, "text")
        if tab_text == 'Graph Data':
            tab = self.notebook.winfo_children()[tab_index]
            for widget in tab.winfo_children():
                widget.destroy()
            # Generate and display the graph in the tab
            graph = generate_and_show_graph()  # Call the function to generate the graph
            canvas = FigureCanvasTkAgg(graph, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
    
    def refresh_index_data(self, event=None):
        # Clear existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve and parse updated data
        companies_data_str = utils.retrieve_all_companies_data()
        if companies_data_str.startswith("Error occurred"):
            # Handle error
            messagebox.showerror("Error", companies_data_str)
            return
        elif companies_data_str == "No data available.":
            # Handle case when no data is available
            messagebox.showinfo("Information", companies_data_str)
            return
        else:
            # Split the string into lines and parse each line into a tuple
            lines = companies_data_str.strip().split("\n")
            # Skip the first two lines
            data = [tuple(line.strip().split()) for line in lines[2:]]

            # Insert data into the treeview
            for company_data in data:
                self.tree.insert("", tk.END, values=company_data)

    def refresh_pdf_data(self, event=None):
        # Clear existing items in the Listbox
        self.reports_listbox.delete(0, tk.END)

        # Populate the Listbox with available PDF reports
        reports_directory = 'reports'  # Update with your directory containing PDF files
        
        # Get a list of tuples containing (filename, creation_time)
        files_with_time = [(filename, os.path.getctime(os.path.join(reports_directory, filename))) 
                            for filename in os.listdir(reports_directory) 
                            if filename.endswith('.pdf')]
        
        # Sort the list of files by creation time in descending order
        sorted_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)
        
        # Add the sorted filenames to the Listbox
        for filename, _ in sorted_files:
            self.reports_listbox.insert(tk.END, filename)

def main():
    root = tk.Tk()
    app = EmissionsDataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()