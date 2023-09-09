import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta

class LifespanCalculatorWithVisualization(tk.Tk):
    def __init__(self, birth_date, expected_lifespan_years):
        super().__init__()
        self.title('Lifespan Visualization')
        self.geometry('650x450')

        self.birth_date = birth_date
        self.expected_lifespan_years = expected_lifespan_years
        self.current_date = datetime.now()

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.data_frame = tk.Frame(self.notebook, bg='#f5f5f5')
        self.visualization_frame = tk.Frame(self.notebook, bg='#f5f5f5')
        self.notebook.add(self.data_frame, text="Data")
        self.notebook.add(self.visualization_frame, text="Visualization")
        self.notebook.pack(expand=1, fill='both')

        # Create UI elements for data and visualization
        self.create_data_ui_elements()
        self.create_visualization_elements()

        # Initial UI update
        self.update_ui_elements()

    def create_data_ui_elements(self):
        font_style = ("Arial", 12)
        bg_color = '#f5f5f5'

        # Labels to display data
        self.age_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.elapsed_days_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.elapsed_weeks_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.elapsed_time_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.life_percentage_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.remaining_time_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)
        self.expected_end_date_label = tk.Label(self.data_frame, font=font_style, bg=bg_color, anchor='w', width=50)

        # Layout using grid
        self.age_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        self.elapsed_days_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.elapsed_weeks_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.elapsed_time_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.life_percentage_label.grid(row=4, column=0, padx=20, pady=10, sticky='w')
        self.remaining_time_label.grid(row=5, column=0, padx=20, pady=10, sticky='w')
        self.expected_end_date_label.grid(row=6, column=0, padx=20, pady=10, sticky='w')

    def create_visualization_elements(self):
        # Constants for visualization
        self.SQUARE_SIZE = 2  # Changed to 2x2 pixels
        self.SQUARES_PER_ROW = 300  # Number of squares per row for visualization
        self.TOTAL_SQUARES = int(self.expected_lifespan_years * 365.25)
        self.canvas_width = self.SQUARES_PER_ROW * self.SQUARE_SIZE
        self.canvas_height = (self.TOTAL_SQUARES // self.SQUARES_PER_ROW + 1) * self.SQUARE_SIZE

        self.canvas = tk.Canvas(self.visualization_frame, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(pady=20)

        for i in range(self.TOTAL_SQUARES):
            row = i // self.SQUARES_PER_ROW
            col = i % self.SQUARES_PER_ROW
            x1 = col * self.SQUARE_SIZE
            y1 = row * self.SQUARE_SIZE
            x2 = x1 + self.SQUARE_SIZE
            y2 = y1 + self.SQUARE_SIZE

            color = "deepskyblue" if i < self.calculate_elapsed_days() else "lightgray"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')

    def update_ui_elements(self):
        self.current_date = datetime.now()  # Refresh current date

        self.age_label['text'] = f"當前年齡（年）：{self.calculate_age_years()}年"
        self.elapsed_days_label['text'] = f"已經活了：{self.calculate_elapsed_days():.2f}天"
        self.elapsed_weeks_label['text'] = f"已經活了：{self.calculate_elapsed_weeks()}週"
        self.elapsed_time_label['text'] = f"已經活了：{self.calculate_elapsed_time()}"
        self.life_percentage_label['text'] = f"已經過去/全部壽命的百分比：{self.calculate_life_percentage():.2f}%"
        self.remaining_time_label['text'] = f"剩餘壽命：{self.calculate_remaining_time()}"
        self.expected_end_date_label['text'] = f"預估壽命80年的時間（年月日）：{self.calculate_expected_end_date()}"

        # Schedule the next update after 1 second
        self.after(1000, self.update_ui_elements)

    # The rest of the methods (for calculation and UI updates) remain the same as in previous provided code
    def calculate_age_years(self):
        return self.current_date.year - self.birth_date.year - (
                (self.current_date.month, self.current_date.day) < (self.birth_date.month, self.birth_date.day))

    def calculate_elapsed_days(self):
        return (self.current_date - self.birth_date).days

    def calculate_elapsed_weeks(self):
        return self.calculate_elapsed_days() // 7

    def calculate_elapsed_time(self):
        elapsed_time = self.current_date - self.birth_date
        years = elapsed_time.days // 365
        months = (elapsed_time.days % 365) // 30
        days = (elapsed_time.days % 365) % 30
        return f"{years}年{months}個月{days}天"

    def calculate_life_percentage(self):
        elapsed_seconds = (self.current_date - self.birth_date).total_seconds()
        total_seconds = self.expected_lifespan_years * 365.25 * 24 * 60 * 60
        return (elapsed_seconds / total_seconds) * 100

    def calculate_remaining_time(self):
        elapsed_time = self.current_date - self.birth_date
        total_time = timedelta(days=self.expected_lifespan_years * 365.25)
        remaining_time = total_time - elapsed_time
        years = remaining_time.days // 365
        months = (remaining_time.days % 365) // 30
        days = (remaining_time.days % 365) % 30
        return f"{years}年{months}個月{days}天"

    def calculate_expected_end_date(self):
        return (self.birth_date + timedelta(days=self.expected_lifespan_years * 365.25)).strftime("%Y-%m-%d")

    # The initialization and running code would remain the same as before:
birth_date = datetime(1993, 9, 22)
expected_lifespan_years = 80
app_with_viz = LifespanCalculatorWithVisualization(birth_date, expected_lifespan_years)
app_with_viz.mainloop()  # Commented out to prevent execution error in this environment
