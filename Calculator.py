import customtkinter as ctk
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Инженерный калькулятор")
        self.geometry("800x600")
        self.resizable(True, True)

        self.history = []
        self.current_mode = "basic"  # "basic" или "scientific"

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(fill="x", padx=5, pady=5)

        self.theme_button = ctk.CTkButton(
            top_frame,
            text="Тема: Тёмная",
            command=self.toggle_theme,
            width=150
        )
        self.theme_button.pack(side="left", padx=5)

        self.mode_button = ctk.CTkButton(
            top_frame,
            text="Режим: Базовый",
            command=self.toggle_mode,
            width=150,
            fg_color="purple"
        )
        self.mode_button.pack(side="left", padx=5)

        self.calc_frame = ctk.CTkFrame(main_frame)
        self.calc_frame.pack(side="left", fill="y", padx=(0, 10))

        self.entry_var = ctk.StringVar()
        self.entry_var.trace('w', self.on_entry_change)

        self.entry = ctk.CTkEntry(
            self.calc_frame,
            textvariable=self.entry_var,
            width=400,
            height=60,
            font=("Arial", 24),
            justify="right",
            border_width=2,
            corner_radius=10
        )
        self.entry.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

        self.create_buttons()

        history_frame = ctk.CTkFrame(main_frame)
        history_frame.pack(side="right", fill="both", expand=True)

        history_label = ctk.CTkLabel(history_frame, text="История", font=("Arial", 18, "bold"))
        history_label.pack(pady=10)

        clear_history_btn = ctk.CTkButton(
            history_frame,
            text="Очистить историю",
            command=self.clear_history,
            fg_color="red",
            hover_color="darkred"
        )
        clear_history_btn.pack(pady=(0, 10))

        self.history_scrollable = ctk.CTkScrollableFrame(history_frame)
        self.history_scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.bind("<Key>", self.on_key_press)
        self.entry.focus_set()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_button.configure(text="Тема: Светлая")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_button.configure(text="Тема: Тёмная")

    def toggle_mode(self):
        if self.current_mode == "basic":
            self.current_mode = "scientific"
            self.mode_button.configure(text="Режим: Научный")
        else:
            self.current_mode = "basic"
            self.mode_button.configure(text="Режим: Базовый")
        self.create_buttons()

    def on_entry_change(self, *args):
        text = self.entry_var.get()
        if len(text) > 25:
            self.entry_var.set(text[-25:])

    def create_buttons(self):
        for widget in self.calc_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget != self.entry:
                widget.destroy()

        if self.current_mode == "basic":
            self.create_basic_buttons()
        else:
            self.create_scientific_buttons()

    def create_basic_buttons(self):
        buttons = [
            ('C', 1, 0, self.clear, "red"),
            ('←', 1, 1, self.backspace, "gray"),
            ('%', 1, 2, lambda: self.add_to_expression('%'), "gray"),
            ('√', 1, 3, self.square_root, "gray"),
            ('÷', 1, 4, lambda: self.add_to_expression('÷'), "gray"),

            ('7', 2, 0, lambda: self.add_to_expression(7), "gray"),
            ('8', 2, 1, lambda: self.add_to_expression(8), "gray"),
            ('9', 2, 2, lambda: self.add_to_expression(9), "gray"),
            ('x²', 2, 3, self.square, "gray"),
            ('×', 2, 4, lambda: self.add_to_expression('×'), "gray"),

            ('4', 3, 0, lambda: self.add_to_expression(4), "gray"),
            ('5', 3, 1, lambda: self.add_to_expression(5), "gray"),
            ('6', 3, 2, lambda: self.add_to_expression(6), "gray"),
            ('1/x', 3, 3, self.inverse, "gray"),
            ('-', 3, 4, lambda: self.add_to_expression('-'), "gray"),

            ('1', 4, 0, lambda: self.add_to_expression(1), "gray"),
            ('2', 4, 1, lambda: self.add_to_expression(2), "gray"),
            ('3', 4, 2, lambda: self.add_to_expression(3), "gray"),
            ('±', 4, 3, self.toggle_sign, "gray"),
            ('+', 4, 4, lambda: self.add_to_expression('+'), "gray"),

            ('π', 5, 0, self.add_pi, "gray"),
            ('0', 5, 1, lambda: self.add_to_expression(0), "gray"),
            ('.', 5, 2, lambda: self.add_to_expression('.'), "gray"),
            ('=', 5, 3, self.calculate, "orange", 1, 2),
        ]

        self.place_buttons(buttons)

    def create_scientific_buttons(self):
        buttons = [
            ('C', 1, 0, self.clear, "red"),
            ('←', 1, 1, self.backspace, "gray"),
            ('(', 1, 2, lambda: self.add_to_expression('('), "gray"),
            (')', 1, 3, lambda: self.add_to_expression(')'), "gray"),
            ('%', 1, 4, lambda: self.add_to_expression('%'), "gray"),
            ('÷', 1, 5, lambda: self.add_to_expression('÷'), "gray"),
            ('xʸ', 1, 6, lambda: self.add_to_expression('^'), "gray"),

            ('sin', 2, 0, self.sin_func, "gray"),
            ('cos', 2, 1, self.cos_func, "gray"),
            ('tan', 2, 2, self.tan_func, "gray"),
            ('√', 2, 3, self.square_root, "gray"),
            ('x²', 2, 4, self.square, "gray"),
            ('×', 2, 5, lambda: self.add_to_expression('×'), "gray"),
            ('1/x', 2, 6, self.inverse, "gray"),

            ('log', 3, 0, self.log_func, "gray"),
            ('ln', 3, 1, self.ln_func, "gray"),
            ('eˣ', 3, 2, self.exp_func, "gray"),
            ('10ˣ', 3, 3, self.ten_power_func, "gray"),
            ('x!', 3, 4, self.factorial_func, "gray"),
            ('-', 3, 5, lambda: self.add_to_expression('-'), "gray"),
            ('±', 3, 6, self.toggle_sign, "gray"),

            ('7', 4, 0, lambda: self.add_to_expression(7), "gray"),
            ('8', 4, 1, lambda: self.add_to_expression(8), "gray"),
            ('9', 4, 2, lambda: self.add_to_expression(9), "gray"),
            ('π', 4, 3, self.add_pi, "gray"),
            ('e', 4, 4, self.add_e, "gray"),
            ('+', 4, 5, lambda: self.add_to_expression('+'), "gray"),
            ('=', 4, 6, self.calculate, "orange", 2, 1),

            ('4', 5, 0, lambda: self.add_to_expression(4), "gray"),
            ('5', 5, 1, lambda: self.add_to_expression(5), "gray"),
            ('6', 5, 2, lambda: self.add_to_expression(6), "gray"),

            ('1', 6, 0, lambda: self.add_to_expression(1), "gray"),
            ('2', 6, 1, lambda: self.add_to_expression(2), "gray"),
            ('3', 6, 2, lambda: self.add_to_expression(3), "gray"),
            ('0', 6, 3, lambda: self.add_to_expression(0), "gray", 1, 2),
            ('.', 6, 5, lambda: self.add_to_expression('.'), "gray"),
        ]

        self.place_buttons(buttons)

    def place_buttons(self, buttons):
        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            command = button[3]
            color = button[4] if len(button) > 4 else "gray"
            rowspan = button[5] if len(button) > 5 else 1
            colspan = button[6] if len(button) > 6 else 1

            fg_color = "red" if color == "red" else "gray50"
            if color == "orange":
                fg_color = "orange"

            ctk.CTkButton(
                self.calc_frame,
                text=text,
                font=("Arial", 14, "bold"),
                width=60,
                height=50,
                corner_radius=10,
                fg_color=fg_color,
                hover_color="gray30",
                command=command
            ).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, padx=2, pady=2)

    def add_to_expression(self, value):
        current = self.entry_var.get()
        self.entry_var.set(current + str(value))

    def clear(self):
        self.entry_var.set("")

    def backspace(self):
        current = self.entry_var.get()
        if current:
            self.entry_var.set(current[:-1])

    def square_root(self):
        try:
            value = float(self.entry_var.get())
            if value < 0:
                raise ValueError("Нельзя извлекать корень из отрицательного числа")
            result = math.sqrt(value)
            self.entry_var.set(str(result))
        except Exception:
            self.entry_var.set("Ошибка")

    def square(self):
        try:
            value = float(self.entry_var.get())
            result = value ** 2
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def inverse(self):
        try:
            value = float(self.entry_var.get())
            if value == 0:
                raise ZeroDivisionError
            result = 1 / value
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def toggle_sign(self):
        current = self.entry_var.get()
        if current:
            try:
                value = float(current)
                self.entry_var.set(str(-value))
            except:
                pass

    def add_pi(self):
        self.add_to_expression(str(math.pi))

    def add_e(self):
        self.add_to_expression(str(math.e))

    def sin_func(self):
        try:
            value = float(self.entry_var.get())
            result = math.sin(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def cos_func(self):
        try:
            value = float(self.entry_var.get())
            result = math.cos(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def tan_func(self):
        try:
            value = float(self.entry_var.get())
            result = math.tan(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def log_func(self):
        try:
            value = float(self.entry_var.get())
            if value <= 0:
                raise ValueError("Логарифм определен только для положительных чисел")
            result = math.log10(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def ln_func(self):
        try:
            value = float(self.entry_var.get())
            if value <= 0:
                raise ValueError("Логарифм определен только для положительных чисел")
            result = math.log(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def exp_func(self):
        try:
            value = float(self.entry_var.get())
            result = math.exp(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def ten_power_func(self):
        try:
            value = float(self.entry_var.get())
            result = 10 ** value
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def factorial_func(self):
        try:
            value = int(float(self.entry_var.get()))
            if value < 0:
                raise ValueError("Факториал определен только для неотрицательных целых чисел")
            result = math.factorial(value)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")

    def calculate(self):
        try:
            expression = self.entry_var.get()
            original_expression = expression
            expression = expression.replace('×', '*').replace('÷', '/').replace('^', '**').replace('%', '/100')
            result = eval(expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            history_text = f"{original_expression} = {result}"
            self.history.append(history_text)
            self.add_to_history_display(history_text)

            self.entry_var.set(str(result))
        except Exception:
            self.entry_var.set("Ошибка")

    def add_to_history_display(self, text):
        label = ctk.CTkLabel(
            self.history_scrollable,
            text=text,
            font=("Arial", 14),
            anchor="w",
            cursor="hand2"
        )
        label.pack(fill="x", pady=2, padx=5)
        label.bind("<Button-1>", lambda e: self.entry_var.set(text.split(' = ')[0]))

    def clear_history(self):
        for widget in self.history_scrollable.winfo_children():
            widget.destroy()
        self.history.clear()

    def on_key_press(self, event):
        key = event.char
        keysym = event.keysym

        if key in '0123456789().':
            self.add_to_expression(key)
        elif key == '+':
            self.add_to_expression('+')
        elif key == '-':
            self.add_to_expression('-')
        elif key == '*':
            self.add_to_expression('×')
        elif key == '/':
            self.add_to_expression('÷')
        elif key == '^':
            self.add_to_expression('^')
        elif key == '%':
            self.add_to_expression('%')
        elif key == 'c' or key == 'C' or keysym == 'Delete':
            self.clear()
        elif key == '\r' or keysym == 'Return':
            self.calculate()
        elif key == '\x1b':
            self.clear()
        elif key == '\x08' or keysym == 'BackSpace':
            self.backspace()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()