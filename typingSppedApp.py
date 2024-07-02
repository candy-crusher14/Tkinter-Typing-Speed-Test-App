from tkinter import *
from random import choice
import time
from data import sentence_data
import pandas as pd
import os

def create_wpm_accuracy_records(file_path):
    if not os.path.isfile(file_path):
        df = pd.DataFrame({
            'wpm': [],
            'accuracy': []
        })
        df.to_csv(file_path, index=False)


def add_wpm_accuracy(file_path,wpm,accuracy):
    data = {
        'wpm': [wpm],
        'accuracy': [accuracy]
    }
    df = pd.DataFrame(data)

    df.to_csv(file_path, mode='a', header=False, index=False)

create_wpm_accuracy_records('wpm_records.csv')
# add_wpm_accuracy('wpm_records.csv', 24, 94)

def read_csv_as_int(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert the columns to integer type
    df = df.astype(int)

    return df


start_time = time.time()
timer_running = False
chosen_sentence = None
time_duration = None
wpm_acc_records = read_csv_as_int('wpm_records.csv').to_dict(orient='list')
highest_wpm_accuracy = None
try:
    i = wpm_acc_records['wpm'].index(max(wpm_acc_records['wpm']))  # Index of highest wpm
except ValueError:
    highest_wpm_accuracy = "Highest WPM/Accuracy: None/None"
else:
    highest_wpm_accuracy = f"Highest WPM/Accuracy: {wpm_acc_records['wpm'][i]}/{wpm_acc_records['accuracy'][i]}%"

# Convert csv file to dictionary list




def start_test():
    global start_time, timer_running, chosen_sentence, time_duration

    start_button.config(state='disabled')
    done_button.config(state='normal')
    start_time = time.time()
    timer_running = True
    time_duration = timer_var.get()

    wpm_label.config(text="WPM: ...")
    cpm_label.config(text="CPM: ...")
    accuracy_label.config(text=f"Accuracy: ...%")

    difficulty_menu.config(state='disabled')
    timer_menu.config(state='disabled')
    high_speed_label.config(text=highest_wpm_accuracy)
    instruction_button.config(state='disabled')

    difficulty = difficulty_var.get()  # Get selected difficulty and choose a sentence
    # Update sentence_label with the chosen sentence
    if difficulty == 'Easy':
        chosen_sentence = choice(sentence_data['easy_sentence'])
        typing_label.config(text=chosen_sentence, bg='lavenderblush', fg='black')
    elif difficulty == 'Medium':
        chosen_sentence = choice(sentence_data['medium_sentence'])
        typing_label.config(text=chosen_sentence, bg='lavenderblush', fg='black')
    else:
        chosen_sentence = choice(sentence_data['hard_sentence'])
        typing_label.config(text=chosen_sentence, bg='lavenderblush', fg='black')

    user_typing.config(state='normal')
    user_typing.delete('1.0', END)
    user_typing.focus()

    timer_function()

def timer_function():
    global time_duration
    if timer_running:
        elapsed_time = time.time() - start_time  # Decrease timer every second
        # Update timer label
        if elapsed_time >= float(time_duration):
            results()
            print('Timer Ended....')
        else:
            info_frame.after(1000, timer_function)  # Run this function every seconds
            timer_label.config(text=f"Timer: {elapsed_time:.0f} second",
                               fg='SpringGreen2'
                               )

def results():
    global timer_running, chosen_sentence,highest_wpm_accuracy, wpm_acc_records, start_time
    timer_running = False
    elapsed_time = time.time() - start_time

    typed_text = user_typing.get('1.0', END).strip()
    num_words = len(typed_text.split())
    num_chars = len(typed_text)

    # Calculate WPM and CPM
    wpm = (num_words / elapsed_time) * 60
    cpm = (num_chars / elapsed_time) * 60
    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(typed_text, chosen_sentence) if a == b)
    accuracy = (correct_chars / len(chosen_sentence)) * 100

    file_path = 'wpm_records.csv' # Write every wpm  with accuracy records
    add_wpm_accuracy(file_path, f'{wpm:.0f}', f"{accuracy:.0f}")

    wpm_acc_records = read_csv_as_int('wpm_records.csv').to_dict(orient='list')
    index = wpm_acc_records['wpm'].index(max(wpm_acc_records['wpm']))  # Index of highest wpm
    highest_wpm_accuracy = f"Highest WPM/Accuracy: {wpm_acc_records['wpm'][index]}/{wpm_acc_records['accuracy'][index]}%"


    # Update results_label with the calculated values
    high_speed_label.config(text=highest_wpm_accuracy)
    timer_label.config(fg='gold')
    wpm_label.config(text=f"WPM: {wpm:.0f}", fg='gold')
    cpm_label.config(text=f"CPM: {cpm:.0f}", fg='gold')
    accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%", fg='gold')
    # Disable text_entry and reset for a new test
    reset_test()


def real_time_results(event):
    global chosen_sentence, start_time

    elapsed_time = time.time() - start_time
    typed_text = user_typing.get('1.0', END).strip()
    num_words = len(typed_text.split())
    num_chars = len(typed_text)

    # Calculate WPM and CPM
    # wpm = (num_words / elapsed_time) * 60
    cpm = (num_chars / elapsed_time) * 60

    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(typed_text, chosen_sentence) if a == b)
    accuracy = (correct_chars / len(chosen_sentence)) * 100 if chosen_sentence else 0

    # wpm_label.config(text=f"WPM: {wpm:.0f}")
    cpm_label.config(text=f"CPM: {cpm:.0f}")
    accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")


def reset_test():
    typing_label.config(text='Check Results...', fg='gold', bg='gray15')
    start_button.config(state='disabled')
    user_typing.focus()

def reset():
    global start_time, timer_running, chosen_sentence
    start_time = None
    timer_running = False
    chosen_sentence = None
    difficulty_menu.config(state='normal')
    timer_menu.config(state='normal')
    start_button.config(state='normal')
    typing_label.config(text='Reset Activated...', fg='black', bg='lavenderblush')
    timer_label.config(text='Timer: 00', fg='salmon')
    wpm_label.config(text='WPM: 00', fg='salmon')
    cpm_label.config(text='CPM: 00', fg='salmon')
    accuracy_label.config(text='Accuracy: 0%', fg='salmon')
    done_button.config(state='disabled')
    instruction_button.config(state='normal')
    user_typing.delete('1.0', END)

def instructions():
    typing_label.config(text="""Instructions\n1. Start Button to Start \
                             \n2. Click Done Button when you completed sentence before timer and get results \
                             \n3.Reset Button to Reset Everything and Start Again
                             """,
                        bg='black',
                        fg='salmon'
                        )

def compare_text(event):
    typed_text = user_typing.get('1.0', END).strip()
    correct_text = chosen_sentence
    if not correct_text:
        return

    user_typing.tag_remove("correct", "1.0", "end")
    user_typing.tag_remove("incorrect", "1.0", "end")

    for i, char in enumerate(typed_text):
        if i < len(correct_text):
            if char == correct_text[i]:
                user_typing.tag_add("correct", f"1.{i}", f"1.{i+1}")
            else:
                user_typing.tag_add("incorrect", f"1.{i}", f"1.{i+1}")

window = Tk()
window.config(height=800, width=1000, padx=20, pady=20, bg='black')
window.title('Typing Speed App')

label_fonts = ("Verdana", 14)

# Frame For Typing
typing_frame = Frame(window, bg='black')
typing_frame.grid(row=0, column=0, padx=10, pady=10)

# Frame For info
info_frame = Frame(window, bg='black')
info_frame.grid(row=0, column=1, padx=20, pady=10, sticky='n')

typing_label = Label(typing_frame,
                     height=20,
                     width=30,
                     font=label_fonts,
                     wraplength=350)
typing_label.grid(row=0, column=0)

write_below = Label(typing_frame,
                    text='Write Below',
                    bg='black',
                    fg='lightcyan',
                    font=("Georgia", 14)
                    )
write_below.grid(row=1, column=0, pady=(10, 5))

user_typing = Text(typing_frame,
                   font=label_fonts,
                   width=25,
                   height=2
                   )
user_typing.grid(row=2, column=0, pady=(10, 5))
user_typing.bind("<KeyRelease>", compare_text)
# user_typing.bind("<KeyRelease>", real_time_results)

user_typing.tag_configure("correct", foreground="green")
user_typing.tag_configure("incorrect", foreground="red")

instruction_button = Button(typing_frame,
                            text='Instructions',
                            bg='black',
                            fg='mediumpurple',
                            font=label_fonts,
                            activeforeground='black',
                            activebackground='deeppink2',
                            width=10,
                            command=instructions
                            )
instruction_button.grid(row=3, column=0, pady=(20, 0))

about_label = Label(info_frame,
                    text='Welcome To Typing Speed',
                    bg='black',
                    fg='lightcyan',
                    font=("Georgia", 14)
                    )
about_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

timer_label = Label(info_frame,
                    text='Timer: 00',
                    bg='black',
                    fg='salmon',
                    font=label_fonts
                    )
timer_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

wpm_label = Label(info_frame,
                  text='WPM: 00',
                  bg='black',
                  fg='salmon',
                  font=label_fonts
                  )
wpm_label.grid(row=2, column=0, pady=(10, 5))

cpm_label = Label(info_frame,
                  text='CPM: 00',
                  bg='black',
                  fg='salmon',
                  font=label_fonts
                  )
cpm_label.grid(row=3, column=0, pady=(10, 5))

accuracy_label = Label(info_frame,
                       text='Accuracy: 0%',
                       bg='black',
                       fg='salmon',
                       font=label_fonts
                       )
accuracy_label.grid(row=4, column=0, pady=(10, 5))






high_speed_label = Label(info_frame,
                         text=highest_wpm_accuracy,
                         bg='black',
                         fg='salmon',
                         font=label_fonts,
                         wraplength=200
                         )
high_speed_label.grid(row=5, column=0, pady=(10, 5))

timer_option = Label(info_frame,
                         text="Time Duration(s)",
                         font=("Segoeui", 14),
                         bg='black',
                         fg='deepskyblue')
timer_option.grid(row=6, column=0, pady=(20, 10), padx=(10, 10), sticky='nw')

timer_var = StringVar(info_frame, value="60")  # Get Answer by "difficulty_var.get()".
timer_options = ["30", "40", "60", "80", "120"]
timer_menu = OptionMenu(info_frame, timer_var, *timer_options)
timer_menu.grid(row=6, column=0, pady=(20, 10), padx=(10, 10), sticky='ne')

difficulty_label = Label(info_frame,
                         text="Select Difficulty",
                         font=("Segoeui", 14),
                         bg='black',
                         fg='deepskyblue')
difficulty_label.grid(row=7, column=0, pady=(20, 10), padx=(10, 10), sticky='nw')

difficulty_var = StringVar(info_frame, value="Easy")  # Get Answer by "difficulty_var.get()".
difficulty_options = ["Easy", "Medium", "Hard"]
difficulty_menu = OptionMenu(info_frame, difficulty_var, *difficulty_options)
difficulty_menu.grid(row=7, column=0, pady=(20, 10), padx=(10, 10), sticky='ne')

start_button = Button(info_frame,
                      text='Start',
                      bg='black',
                      fg='olivedrab1',
                      font=label_fonts,
                      activeforeground='black',
                      activebackground='lightblue',
                      width=10,
                      command=start_test
                      )
start_button.grid(row=8, column=0, pady=(10, 10), sticky='nw')

reset_button = Button(info_frame,
                     text='Reset',
                     bg='black',
                     fg='olivedrab1',
                     font=label_fonts,
                     activeforeground='black',
                     activebackground='lightblue',
                     width=10,
                     command=reset
                     )
reset_button.grid(row=8, column=0, pady=(10, 10), sticky='ne')

done_button = Button(info_frame,
                     text='Done',
                     bg='black',
                     fg='olivedrab1',
                     font=label_fonts,
                     activeforeground='black',
                     activebackground='lightblue',
                     width=10,
                     command=results,
                     state='disabled'
                     )
done_button.grid(row=9, column=0)

window.mainloop()
