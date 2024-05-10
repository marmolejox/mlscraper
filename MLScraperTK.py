import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from bs4 import BeautifulSoup
import requests

# base declarations
base_url = 'https://listado.mercadolibre.com.mx/'
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}

# initialize an empty array for the elements
data = []

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sets the title of the window to "App"
        self.title("ML Product Scrapper")
        self.state('zoomed')  # This line maximizes the window at startup

        self.entryFrame = tk.Frame(self)
        self.entryFrame.pack(side="top", fill="x", padx=10, pady=10)

        self.tableFrame = tk.Frame(self)
        self.tableFrame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        # Product
        self.productLabel = tk.Label(self.entryFrame, text="Product")
        self.productLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Product Entry
        self.productEntry = tk.Entry(self.entryFrame, font=("Arial", 12))
        self.productEntry.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        # Scrape Button
        self.scrapeButton = tk.Button(self.entryFrame, text="Scrape", command=self.scrape)
        self.scrapeButton.grid(row=0, column=6, columnspan=2, padx=10, pady=10, sticky="ew")

        # Save CSV Button
        self.saveCsvButton = tk.Button(self.entryFrame, text="Save CSV", command=self.save_csv)
        self.saveCsvButton.grid(row=0, column=8, columnspan=2, padx=10, pady=10, sticky="ew")

        self.table = ttk.Treeview(self.tableFrame, columns=("Title", "Price", "Link", "Image"), show="headings")
        self.table.heading("Title", text="Product")
        self.table.heading("Price", text="Price")
        self.table.heading("Link", text="Link")
        self.table.heading("Image", text="Image")
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

    def scrape(self):
        global data
        data = []

        product = self.productEntry.get().replace(" ", "-")
        if not product:
            return

        url = base_url + product
        print(url)

        page = requests.get(url, headers=custom_headers)
        soup = BeautifulSoup(page.text, "html.parser")
        content = soup.find_all('li', class_='ui-search-layout__item')

        # Limpiar la tabla antes de insertar nuevos datos
        self.table.delete(*self.table.get_children())

        if content:
            for post in content:
                title = post.find('h2').text
                price = post.find('span', class_='andes-money-amount__fraction').text
                post_link = post.find("a")["href"]
                try:
                    img_link = post.find("img")["data-src"]
                except:
                    img_link = post.find("img")["src"]

                post_data = {
                    "title": title,
                    "price": price,
                    "post link": post_link,
                    "image link": img_link
                }

                data.append(post_data)

            for item in data:
                self.table.insert("", "end", values=(item["title"], item["price"],
                                                     "Full link on the .csv file" if len(item["post link"]) > 50 else
                                                     item["post link"], item["image link"]))
        else:
            messagebox.showerror('Error', 'No results!')
            print("\nError: no results!")

    def save_csv(self):
        if data:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                df = pd.DataFrame(data)
                df.to_csv(file_path, sep=";", index=False)
        else:
            messagebox.showerror('Error', 'No data to save!')
            print("No data to save.")

if __name__ == "__main__":
    app = App()
    app.mainloop()