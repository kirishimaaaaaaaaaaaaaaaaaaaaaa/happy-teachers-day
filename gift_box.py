import tkinter as tk
import subprocess
import sys

def open_emotion_detector():
    root.destroy()  
   
    subprocess.run([sys.executable, "emotion_detector.py"])

root = tk.Tk()
root.title("Gift Box 🎁")
root.geometry("300x200")

label = tk.Label(root, text="🎁 Click the box 🎁", font=("Arial", 16))
label.pack(pady=20)

button = tk.Button(root, text="Click Me!", font=("Arial", 14), bg="pink", command=open_emotion_detector)
button.pack(pady=20)

root.mainloop()

