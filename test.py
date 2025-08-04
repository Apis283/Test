import json
import tkinter as tk
from tkinter import messagebox, simpledialog, PanedWindow, messagebox
from PIL import ImageTk, Image

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CFETP Test")
        self.root.resizable(False, False)
        self.root.geometry("800x600")
        self.root.config(bg="black")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize the image using Pillow (shrink to 75% and fit within 800x600)
        original_image = Image.open('emblem.png')
        new_width = int(original_image.width * 1.3)
        new_height = int(original_image.height * 1.3)

        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(150, 300, image=self.bg_image)  # Center the resized image
        while True:
            self.user_name = tk.simpledialog.askstring("User Information", "Please enter your name:")
            if self.user_name == None:
                messagebox.showwarning("Warning", "Test Canceled.")
                quit()
            elif not self.user_name.replace(" ", "").isalpha():
                messagebox.showwarning("Warning", "Invalid name entered. Please use letters only.")
                continue
            break
        
        self.data = self.load_data()
        self.tests = self.data['tests']
        self.current_test_index = None
        self.current_section_index = 0
        self.current_subsection_index = 0
        self.current_question_index = 0
        self.user_answers = []
        self.missed_subsections = set()
        self.selected_answer = tk.IntVar(value=-1)
        self.show_test_selection()
        self.root.bind("<F12>", lambda e: self.show_results())

    def load_data(self):
        # Loads the JSON data from the file
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def show_test_selection(self):
        # Clears the window and sets up the test selection screen
        self.root.geometry("800x600")  # Reset window size
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(bg="black")  # Sets the window background to black first

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize the image using Pillow (shrink to 75% and fit within 800x600)
        original_image = Image.open('emblem.png')
        new_width = int(original_image.width * 1.3)
        new_height = int(original_image.height * 1.3)

        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(150, 300, image=self.bg_image)  # Center the resized image

        # Add title label with transparent background at custom position
        title_label = tk.Label(self.root,text=f"{self.user_name} \n Select a Test", bg="black", fg="white", font=("Arial", 20), wraplength=200, justify="center")
        title_label.place(x=575, y=70)  # Adjust these x, y values to move the title``

        # Add buttons with red border at custom positions
        button_y = 213  # Starting y position for the first button
        for i, test in enumerate(self.tests):
            frame = tk.Frame(self.root, bg="red", highlightthickness=0)
            frame.place(x=595, y=button_y, width=170, height=40)  # Adjust width/height as needed
            btn = tk.Button(frame, text=f"Test {i+1}", command=lambda idx=i: self.start_test(idx),
                            bg="black", fg="white", activebackground="gray", activeforeground="white",
                            borderwidth=0, width=15, height=1, font=("Arial", 16))
            btn.place(x=3, y=3, width=164, height=34)  # Slightly inside the frame for border effect
            button_y += 60  # Space between buttons
            
    def start_test(self, test_index):
        # Initializes variables for the selected test and starts the first question
        self.current_test_index = test_index
        self.current_section_index = 0
        self.current_subsection_index = 0
        self.current_question_index = 0
        self.user_answers = []
        self.missed_subsections = set()
        self.show_question()

    def show_question(self):
        # Displays the current question and answer options
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(bg="white")
        test = self.tests[self.current_test_index]
        section = test['sections'][self.current_section_index]
        subsection = section['subsections'][self.current_subsection_index]
        question = subsection['questions'][self.current_question_index]

        # Add test name in the top left
        tk.Label(
            self.root,
            text=test['name'],
            bg="white",
            fg="black",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).place(x=10, y=10)

        tk.Label(self.root, text=f"{section['name']} - {subsection['name']}", bg="white", font=("Arial", 10)).pack(pady=10)
        tk.Label(self.root, text=question['text'], wraplength=600, bg="white", font=("Arial",16)).pack(pady=10)
        self.selected_answer.set(-1)
        for i, option in enumerate(question['options']):
            tk.Radiobutton(self.root, text=option, variable=self.selected_answer, value=i, bg="white", font=("Arial",16)).pack(anchor='w')
        tk.Button(self.root, text="Next", command=self.submit_answer, bg="white", width=10, height=1, font=("Arial",16,"bold")).pack(pady=10)

        cancel_btn = tk.Button(self.root, text="Cancel Test", command=self.cancel_test, bg="white")
        cancel_btn.place(x=700, y=550, width=90, height=35)

    def submit_answer(self):
        # Handles answer submission and moves to the next question or shows results
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Warning", "Please select an answer")
            return
        test = self.tests[self.current_test_index]
        section = test['sections'][self.current_section_index]
        subsection = section['subsections'][self.current_subsection_index]
        question = subsection['questions'][self.current_question_index]
        selected = self.selected_answer.get()
        self.user_answers.append({
            'subsection_name': f"{section['name']} - {subsection['name']}",
            'question_index': self.current_question_index,
            'selected_index': selected
        })
        if selected != question['correct_index']:
            self.missed_subsections.add(f"{section['name']} - {subsection['name']}")
        self.current_question_index += 1
        if self.current_question_index >= len(subsection['questions']):
            self.current_question_index = 0
            self.current_subsection_index += 1
        if self.current_subsection_index >= len(section['subsections']):
            self.current_question_index = 0
            self.current_subsection_index = 0
            self.current_section_index += 1
        if self.current_section_index >= len(test['sections']):
            self.show_results()
        else:
            self.show_question()

    def show_results(self):
        # Displays the results and missed subsections
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.resizable(True, True)
        base_height = 200
        line_height = 30
        dynamic_height = base_height + (len(self.missed_subsections) * line_height)
        self.root.geometry(f"800x{dynamic_height}")
        self.root.config(bg="white")  # Set window background to white

        test = self.tests[self.current_test_index]
        with open(f'Missed_{self.user_name}_{test["name"]}.doc', 'w') as f:
            f.write(f"Test Results for {self.user_name} {test['name']}\n")
            f.write("=" * 40 + "\n")
            f.write("\nMissed Subsections:\n")
            for subsec in self.missed_subsections:
                f.write(f"- {subsec}\n")
            f.write(f"\n\nTrainer Signature:________________________________________\n\nTrainee Signature:________________________________________  Date:__________________\n")

        with open(f'Results_{self.user_name}_{test["name"]}.doc', 'w') as f:
            f.write(f"Test Results for {self.user_name} {test['name']}\n")
            f.write("=" * 40 + "\n")
            for answer in self.user_answers:
                # if answer['selected_index'] == answer['question_index']:                                                                                                  
                f.write(f"Subsection: {answer['subsection_name']}, Question Index: {answer['question_index']}, Selected Index: {answer['selected_index']}\n")
            f.write(f"\n\nTrainer Signature:________________________________________\n\nTrainee Signature:________________________________________  Date:__________________\n")

        tk.Label(self.root, text="Test Complete", bg="white", fg="black", font=("Arial", 10)).pack(pady=10)
        tk.Label(self.root, text="Missed subsections (weaknesses):", bg="white", fg="black", font=("Arial", 10)).pack(pady=5)
        if not self.missed_subsections:
            tk.Label(self.root, text="None - Great job!", bg="white", fg="black", font=("Arial", 10)).pack(pady=5)
        else:
            for subsec in self.missed_subsections:
                tk.Label(self.root, text=subsec, bg="white", fg="black", font=("Arial", 10)).pack(pady=5)
        tk.Button(self.root, text="Back to Tests", command=self.show_test_selection,bg="white").pack(pady=10)
        
    def cancel_test(self):
        confirm = messagebox.askyesno("Cancel Test", "Are you sure you want to cancel the test and return to the main menu?")
        if confirm:
            messagebox.showinfo("Test Canceled", "Test canceled. Returning to main menu.")
            self.show_test_selection()

if __name__ == "__main__":
    # Starts the application
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()