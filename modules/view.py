import os
import logging
import tkinter as tk
from tkinter import messagebox
from NBY_api_parser import get_exchange_rate_by_date, analyze_exchange_rate_dict

from CONFIG import LOGS_DIR

logging.basicConfig(
    level=logging.INFO, 
    filename=os.path.join(LOGS_DIR, 'nbu_parser_logs.log'),
    filemode="a", 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def on_calculate():
    start_date = entry_start.get().strip()
    end_date = entry_end.get().strip()

    logging.info(f"User clicked 'Calculate' for period: {start_date} - {end_date}")

    if not start_date or not end_date:
        logging.warning("Calculation failed: Empty date fields.")
        messagebox.showwarning("Увага", "Введіть обидві дати!")
        return

    try:
        data = get_exchange_rate_by_date(startDate=start_date, endDate=end_date)
        
        if not data:
            logging.error(f"Failed to fetch data for period: {start_date}-{end_date}")
            messagebox.showerror("Помилка", "Дані не отримано. Перевірте формат ДД.ММ.РРРР")
            return

        min_data, max_data, avg = analyze_exchange_rate_dict(data)

        if avg is None:
            logging.info(f"No exchange rate data found for: {start_date}-{end_date}")
            messagebox.showinfo("Інформація", "Даних за цей період немає.")
            return

        min_val = list(min_data.keys())[0]
        min_dates = ", ".join(min_data[min_val])

        max_val = list(max_data.keys())[0]
        max_dates = ", ".join(max_data[max_val])
        
        lbl_dates.config(text=f"Період: {start_date} — {end_date}")
        lbl_avg.config(text=f"Середній курс: {avg:.2f} грн за 1 EUR")
        lbl_min.config(text=f"Мінімум: {min_val:.2f} грн за 1 EUR (дата: {min_dates})")
        lbl_max.config(text=f"Максимум: {max_val:.2f} грн за 1 EUR (дата: {max_dates})")
        
        logging.info(f"Success: Avg={avg:.2f}, Min={min_val}, Max={max_val}")

    except Exception as e:
        logging.exception(f"Critical error in UI calculate loop: {e}")
        messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")

logging.info("--- Application Started ---")

root = tk.Tk()
root.title("NBU Parser")
root.geometry("500x350") 

tk.Label(root, text="Аналіз курсу EUR").pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Початок:").grid(row=0, column=0)
entry_start = tk.Entry(frame_input)
entry_start.grid(row=0, column=1, padx=5, pady=5)
entry_start.insert(0, "01.01.2024")

tk.Label(frame_input, text="Кінець:").grid(row=1, column=0)
entry_end = tk.Entry(frame_input)
entry_end.grid(row=1, column=1, padx=5, pady=5)
entry_end.insert(0, "15.01.2024")

tk.Button(root, text="Розрахувати", command=on_calculate).pack(pady=10)

lbl_dates = tk.Label(root, text="Оберіть період та натисніть Розрахувати", font=("Arial", 10, "italic"))
lbl_dates.pack(pady=5)
lbl_avg = tk.Label(root, text="Середній курс: --")
lbl_avg.pack(pady=5)

lbl_min = tk.Label(root, text="Мінімальний курс: --", wraplength=450) 
lbl_min.pack(pady=5)

lbl_max = tk.Label(root, text="Максимальний курс: --", wraplength=450)
lbl_max.pack(pady=5)

def on_close():
    logging.info("--- Application Closed ---")
    root.destroy()

tk.Button(root, text="Вихід", command=on_close).pack(side="bottom", pady=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()