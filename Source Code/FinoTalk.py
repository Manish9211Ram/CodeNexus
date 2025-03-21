import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import google.generativeai as genai

# Set up Google Gemini API
os.environ["API_KEY"] = 'AIzaSyCJulisxyfFXjp9q67YwQ1chhEYDyHJn08'  # Free API key
genai.configure(api_key=os.environ["API_KEY"])

# Use the correct model for v1beta
model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
chat = model.start_chat()

# Financial Keywords for Question Classification (60% of original list)
financial_keywords = [
    "finance", "investment", "stocks", "economy", "banking", "cryptocurrency", "currency",
    "forex", "exchange rate", "gold price", "market", "trading", "mutual funds", "equity",
    "bonds", "insurance", "loan", "interest rate", "credit", "debit", "savings", "mortgage",
    "budget", "inflation", "GDP", "tax", "audit", "capital", "liquidity", "debt", "real estate",
    "commodity", "interest", "credit score", "futures", "options", "monetary policy", "central bank",
    "GST", "CGST", "income tax", "corporate tax", "dividend", "portfolio", "hedge fund", "derivatives",
    "bull market", "bear market", "IPO", "private equity", "venture capital", "ROI", "ROE", "EPS",
    "P/E ratio", "dividend yield", "market cap", "blue-chip stocks", "index fund", "ETF", "recession",
    "stagflation", "fiscal policy", "quantitative easing", "credit rating", "treasury bills", "repo rate",
    "credit card", "EMI", "personal loan", "home loan", "business loan", "working capital", "cash flow",
    "balance sheet", "profit and loss", "financial statement", "tax evasion", "tax avoidance", "KYC",
    "AML", "financial inclusion", "microfinance", "NBFC", "payment bank", "RBI", "Federal Reserve",
    "IMF", "World Bank", "bankruptcy", "insolvency", "debt restructuring", "credit risk", "market risk",
    "hedging", "arbitrage", "leverage", "margin trading", "call option", "put option", "volatility",
    "diversification", "asset class", "fixed income", "real assets", "crypto", "blockchain", "Bitcoin",
    "Ethereum", "DeFi", "NFT", "digital currency", "e-Rupee", "forex trading", "currency pair", "pip",
    "technical analysis", "fundamental analysis", "gold", "silver", "crude oil", "futures contract",
    "options contract", "swap", "stock market", "bond market", "forex market", "crypto market", "bullish",
    "bearish", "volatility index", "VIX", "market sentiment", "risk appetite", "safe haven", "trade war",
    "tariff", "globalization", "supply chain", "working capital management", "cash management", "treasury management",
    "financial planning", "wealth management", "retirement planning", "tax planning", "trust", "will",
    "inheritance tax", "estate tax", "CSR", "ESG", "sustainable investing", "green bonds", "impact investing",
    "financial literacy", "digital banking", "mobile banking", "UPI", "NEFT", "RTGS", "Paytm", "Google Pay",
    "contactless payment", "cryptocurrency wallet", "hardware wallet", "decentralized exchange", "peer-to-peer lending",
    "crowdfunding", "real estate crowdfunding", "REIT", "property management", "commercial real estate", "infrastructure",
    "PPP", "project finance", "syndicated loan", "insurance policy", "life insurance", "health insurance", "term insurance",
    "pension", "provident fund", "EPF", "PPF", "NPS", "Atal Pension Yojana", "PMJJBY", "PMSBY", "PMMY", "stand-up India",
    "start-up India", "make in India", "digital India", "smart India", "renewable energy", "solar energy", "wind energy",
    "carbon credit", "carbon tax", "climate finance", "green finance", "sustainable finance", "impact finance",
    "dollar value", "currency value", "currency exchange", "currency conversion", "currency fluctuation", "currency risk",
    "currency hedging", "currency market", "currency trading", "currency reserve", "currency depreciation", "currency appreciation"
]

# Function to Check If a Question is Financial
def is_financial_question(question):
    """
    Check if the question contains any financial keywords.
    """
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in financial_keywords)

# Database Setup Function
def setup_database():
    """
    Set up the database and create the required table if it doesn't exist.
    """
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="root")
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        if "finotalk" not in databases:
            cursor.execute("CREATE DATABASE finotalk")
        connection.database = "finotalk"

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_details (
                name VARCHAR(255),
                phone_number VARCHAR(15),
                user_id VARCHAR(50) PRIMARY KEY,
                password VARCHAR(255)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

setup_database()

# GUI Class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FinoTalk - Financial AI Assistant")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.original_image = Image.open("C:/Users/Lenovo/Desktop/Mission Code/Programs/CodeNexus/Source Code/_internal/bg.jpg")
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((400, 500), Image.Resampling.LANCZOS))

        self.canvas = tk.Canvas(self.root, width=400, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.bg_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.sign_in_page()

    def clear_canvas_widgets(self):
        """
        Clear all widgets from the canvas except the background image.
        """
        for widget in self.root.winfo_children():
            if widget not in [self.canvas]:
                widget.destroy()
        self.canvas.delete("widgets")

    def sign_in_page(self):
        """
        Display the sign-in page.
        """
        self.clear_canvas_widgets()
        self.canvas.create_text(200, 70, text="Sign In", font=("Times New Roman", 22, "bold"), fill="black", tags="widgets")

        self.canvas.create_text(100, 140, text="User ID:", font=("Helvetica", 14, "bold"), fill="black", tags="widgets")
        self.user_id_entry = tk.Entry(self.root, font=("Helvetica", 14), width=18)
        self.canvas.create_window(250, 140, window=self.user_id_entry, tags="widgets")

        self.canvas.create_text(100, 190, text="Password:", font=("Helvetica", 14, "bold"), fill="black", tags="widgets")
        self.password_entry = tk.Entry(self.root, font=("Helvetica", 14), show="*", width=18)
        self.canvas.create_window(250, 190, window=self.password_entry, tags="widgets")

        submit_btn = tk.Button(self.root, text="Login", command=self.validate_login, bg="#007bff", font=("Helvetica", 14, "bold"), width=10)
        self.canvas.create_window(200, 250, window=submit_btn, tags="widgets")

        self.canvas.create_text(200, 310, text="New User?", font=("Helvetica", 14, "bold"), fill="black", tags="widgets")
        signup_btn = tk.Button(self.root, text="Sign Up", fg="black", bg="#007bff", font=("Helvetica", 14, "bold"), width=10, command=self.sign_up_page)
        self.canvas.create_window(200, 340, window=signup_btn, tags="widgets")

    def sign_up_page(self):
        """
        Display the sign-up page.
        """
        self.clear_canvas_widgets()
        self.canvas.create_text(200, 50, text="Sign Up", font=("Helvetica", 22, "bold"), fill="black", tags="widgets")

        labels = ["Name:", "Phone Number:", "User ID:", "Password:"]
        self.entries = {}

        y_pos = 120
        for label in labels:
            self.canvas.create_text(100, y_pos, text=label, font=("Helvetica", 14, "bold"), fill="black", tags="widgets")
            entry = tk.Entry(self.root, font=("Helvetica", 14), width=18)
            if label == "Password:":
                entry.config(show="*")
            self.canvas.create_window(250, y_pos, window=entry, tags="widgets")
            self.entries[label] = entry
            y_pos += 50

        submit_btn = tk.Button(self.root, text="Register", command=self.validate_signup, bg="#ff5733", fg="white", font=("Helvetica", 14, "bold"), width=10)
        self.canvas.create_window(200, y_pos + 20, window=submit_btn, tags="widgets")

        back_btn = tk.Button(self.root, text="Back", command=self.sign_in_page, bg="#007bff", font=("Helvetica", 14, "bold"), width=10)
        self.canvas.create_window(200, y_pos + 70, window=back_btn, tags="widgets")

    def validate_signup(self):
        """
        Validate and process the sign-up form.
        """
        name = self.entries["Name:"].get()
        phone = self.entries["Phone Number:"].get()
        userid = self.entries["User ID:"].get()
        password = self.entries["Password:"].get()

        if not userid.isalnum():
            messagebox.showerror("Error", "User ID should be alphanumeric")
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root", database="finotalk")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_details (name, phone_number, user_id, password) VALUES (%s, %s, %s, %s)", 
                           (name, phone, userid, password))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Sign Up Successful!")
            self.sign_in_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def validate_login(self):
        """
        Validate and process the login form.
        """
        userid = self.user_id_entry.get()
        password = self.password_entry.get()

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root", database="finotalk")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_details WHERE user_id = %s AND password = %s", (userid, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.home_page()
            else:
                messagebox.showerror("Error", "Invalid User ID or Password")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def home_page(self):
        """
        Display the home page with the question and answer sections.
        """
        self.clear_canvas_widgets()
        self.canvas.create_text(200, 50, text="FinoTalk", font=("Helvetica", 22, "bold"), fill="black", tags="widgets")

        # Question Box
        self.question_entry = tk.Entry(self.root, font=("Helvetica", 14), width=30)
        self.canvas.create_window(200, 130, window=self.question_entry, tags="widgets")

        # Add "message finotalk" inside the question box
        self.placeholder_text = "message finotalk"
        self.question_entry.insert(0, self.placeholder_text)  # Insert placeholder text
        self.question_entry.config(fg="grey")  # Set placeholder text color to grey

        # Bind events to handle placeholder behavior
        self.question_entry.bind("<FocusIn>", self.clear_placeholder)
        self.question_entry.bind("<FocusOut>", self.restore_placeholder)
        self.question_entry.bind("<Enter>", self.hide_placeholder)  # Hide on hover
        self.question_entry.bind("<Leave>", self.show_placeholder)  # Show on leave

        # Ask Button (changed to "Ask Me")
        ask_btn = tk.Button(self.root, text="Ask Me", command=self.ask_question, bg="#4CAF50", fg="white", font=("Helvetica", 14, "bold"), width=10)
        self.canvas.create_window(200, 180, window=ask_btn, tags="widgets")

        # Answer Box (Text Widget) - Increased height to 15
        self.answer_text = tk.Text(self.root, font=("Helvetica", 12), wrap=tk.WORD, width=40, height=15, bg="white", fg="black")
        self.answer_text.config(state=tk.DISABLED)  # Disable editing
        self.canvas.create_window(200, 350, window=self.answer_text, tags="widgets")

        # Add "Ans:-" in the top-left corner of the answer box
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.insert(tk.END, "Ans:- ")
        self.answer_text.config(state=tk.DISABLED)

    def clear_placeholder(self, event):
        """
        Clear the placeholder text when the user clicks inside the question box.
        """
        if self.question_entry.get() == self.placeholder_text:
            self.question_entry.delete(0, tk.END)
            self.question_entry.config(fg="black")  # Change text color to black

    def restore_placeholder(self, event):
        """
        Restore the placeholder text if the question box is empty and loses focus.
        """
        if not self.question_entry.get():
            self.question_entry.insert(0, self.placeholder_text)
            self.question_entry.config(fg="grey")  # Change text color to grey

    def hide_placeholder(self, event):
        """
        Hide the placeholder text when the cursor hovers over the question box.
        """
        if self.question_entry.get() == self.placeholder_text:
            self.question_entry.delete(0, tk.END)
            self.question_entry.config(fg="black")  # Change text color to black

    def show_placeholder(self, event):
        """
        Show the placeholder text when the cursor leaves the question box and it's empty.
        """
        if not self.question_entry.get():
            self.question_entry.insert(0, self.placeholder_text)
            self.question_entry.config(fg="grey")  # Change text color to grey

    def ask_question(self):
        """
        Send the user's question to the Gemini API and display the response.
        """
        question = self.question_entry.get()
        if question == self.placeholder_text:  # Ignore if the placeholder text is present
            question = ""
        if question and is_financial_question(question):
            try:
                response = chat.send_message(question)
                self.display_answer(response.text)
            except Exception as e:
                messagebox.showerror("API Error", f"Error: {e}")
        else:
            messagebox.showwarning("Warning", "Please ask a financial-related question.")

    def display_answer(self, answer):
        """
        Display the answer in the answer box.
        """
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)  # Clear previous answer
        self.answer_text.insert(tk.END, "Ans:- " + answer)  # Add "Ans:-" before the answer
        self.answer_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()