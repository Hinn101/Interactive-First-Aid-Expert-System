import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk


# --------------------------------------------------
# DATA MODEL FOR EACH FIRST AID TOPIC
# --------------------------------------------------
FIRST_AID_DATA = {
    "Bleeding": {
        "steps": [
            "Stay calm and reassure the injured person.",
            "If available, wash hands or wear gloves.",
            "Apply direct pressure on the wound with a clean cloth.",
            "Do NOT remove soaked cloth — add more layers.",
            "Raise the injured limb above heart level.",
            "Once bleeding reduces, clean gently with clean water.",
            "Cover with a sterile bandage."
        ],
        "image": "images/bleeding.jpg",
        "emergency": [
            "Blood is spurting.",
            "Bleeding continues after 10 minutes.",
            "An object is stuck inside the wound."
        ]
    },

    "Burns": {
        "steps": [
            "Move the person away from the heat source.",
            "Cool the burn under running water for 20 minutes.",
            "Remove rings or tight items before swelling starts.",
            "DO NOT apply toothpaste, butter, or oils.",
            "Cover loosely with a clean non-stick cloth.",
            "Do NOT burst blisters."
        ],
        "image": "images/burns.jpg",
        "emergency": [
            "Burn is deep, white, or charred.",
            "Electrical or chemical burns.",
            "Burn affects face or covers a large area."
        ]
    },

    "Choking": {
        "steps": [
            "If they can cough, encourage them to keep coughing.",
            "If they cannot breathe: give 5 back blows.",
            "Then give 5 abdominal thrusts (Heimlich maneuver).",
            "Repeat 5 back blows + 5 abdominal thrusts.",
            "If person collapses, start CPR."
        ],
        "image": "images/choking.jpg",
        "emergency": [
            "Person becomes unconscious.",
            "Choking does not clear."
        ]
    },

    "Fracture": {
        "steps": [
            "Do NOT move the injured area.",
            "Keep the person calm and still.",
            "Support limb using a splint (wood/cardboard).",
            "Apply ice wrapped in cloth.",
            "Check skin colour and sensation.",
            "Do NOT push exposed bone back inside."
        ],
        "image": "images/fracture.jpg",
        "emergency": [
            "Bone is visible.",
            "Limb looks twisted or deformed."
        ]
    }
}


# --------------------------------------------------
# MAIN APP CLASS
# --------------------------------------------------
class FirstAidGUI:

    def __init__(self, root):
        self.root = root
        root.title("First Aid Expert System")
        root.geometry("850x650")
        root.config(bg="#eef7ff")

        self.current_topic = None
        self.current_step_index = 0

        self.create_welcome_screen()

    # --------------------------------------------------
    def create_welcome_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="WELCOME TO THE FIRST AID EXPERT SYSTEM",
                 font=("Arial", 20, "bold"), bg="#eef7ff").pack(pady=30)

        tk.Label(self.root, text="What is your name?", font=("Arial", 15), bg="#eef7ff").pack()

        self.name_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.name_entry.pack(pady=10)

        tk.Button(self.root, text="Continue", font=("Arial", 14),
                  command=self.go_to_main_menu, bg="#4da6ff", fg="white").pack(pady=20)

    # --------------------------------------------------
    def go_to_main_menu(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return
        self.username = name
        self.main_menu()

    # --------------------------------------------------
    def main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Hello {self.username}, how can I assist you?",
                 font=("Arial", 18, "bold"), bg="#eef7ff").pack(pady=15)

        for topic in FIRST_AID_DATA:
            tk.Button(self.root, text=topic, font=("Arial", 15),
                      width=30, command=lambda t=topic: self.start_first_aid(t),
                      bg="#a7cfff").pack(pady=6)

        tk.Button(self.root, text="Exit System", font=("Arial", 14),
                  command=self.exit_system, bg="#ff4d4d", fg="white").pack(pady=20)

    # --------------------------------------------------
    def start_first_aid(self, topic):
        self.current_topic = topic
        self.current_step_index = 0
        self.display_step()

    # --------------------------------------------------
    def display_step(self):
        self.clear_screen()

        topic_data = FIRST_AID_DATA[self.current_topic]

        # Title
        tk.Label(self.root, text=f"{self.current_topic.upper()} — STEP {self.current_step_index + 1}",
                 font=("Arial", 20, "bold"), bg="#eef7ff").pack(pady=10)

        # Load Image
        try:
            img = Image.open(topic_data["image"])
            img = img.resize((400, 250))
            self.tk_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.tk_img, bg="#eef7ff").pack(pady=10)
        except:
            tk.Label(self.root, text="(Image not found)", font=("Arial", 12), bg="#eef7ff").pack()

        # Step Text
        step_text = topic_data["steps"][self.current_step_index]
        tk.Label(self.root, text=step_text, font=("Arial", 16), wraplength=700,
                 bg="#eef7ff").pack(pady=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self.root, bg="#eef7ff")
        nav_frame.pack(pady=20)

        if self.current_step_index > 0:
            tk.Button(nav_frame, text="Previous", font=("Arial", 14),
                      command=self.previous_step, bg="#99bbff").grid(row=0, column=0, padx=10)

        if self.current_step_index < len(topic_data["steps"]) - 1:
            tk.Button(nav_frame, text="Next", font=("Arial", 14),
                      command=self.next_step, bg="#4da6ff", fg="white").grid(row=0, column=1, padx=10)
        else:
            tk.Button(nav_frame, text="Chatbot Summary", font=("Arial", 14),
                      command=self.chatbot_summary, bg="#33cc33", fg="white").grid(row=0, column=1, padx=10)

        tk.Button(self.root, text="Back to Menu", font=("Arial", 14),
                  command=self.main_menu, bg="#8888ff", fg="white").pack(pady=10)

    # --------------------------------------------------
    def previous_step(self):
        self.current_step_index -= 1
        self.display_step()

    def next_step(self):
        self.current_step_index += 1
        self.display_step()

    # --------------------------------------------------
    # CHATBOT-LIKE SUMMARY AND RECOMMENDATIONS
    # --------------------------------------------------
    def chatbot_summary(self):
        self.clear_screen()

        topic = self.current_topic
        data = FIRST_AID_DATA[topic]

        tk.Label(self.root, text=f"{topic} — Chatbot Advice",
                 font=("Arial", 20, "bold"), bg="#eef7ff").pack(pady=20)

        text_box = scrolledtext.ScrolledText(self.root, width=70, height=18, font=("Arial", 14))
        text_box.pack()

        text_box.insert(tk.END, f"👋 Hello {self.username}, here is your quick summary for {topic.lower()}:\n\n")

        for step in data["steps"]:
            text_box.insert(tk.END, f"• {step}\n")

        text_box.insert(tk.END, "\n⚠ Emergency signs:\n")
        for e in data["emergency"]:
            text_box.insert(tk.END, f"❗ {e}\n")

        text_box.configure(state="disabled")

        tk.Button(self.root, text="Back to Menu", font=("Arial", 14),
                  command=self.main_menu, bg="#4da6ff", fg="white").pack(pady=20)

    # --------------------------------------------------
    def exit_system(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            messagebox.showinfo("Thank You", "🙏 Thank you for using the First Aid Expert System.\nStay safe!")
            self.root.destroy()

    # --------------------------------------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# --------------------------------------------------
# RUN THE APPLICATION
# --------------------------------------------------
root = tk.Tk()
app = FirstAidGUI(root)
root.mainloop()
