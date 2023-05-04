import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from random import random, randint
import openai
import tiktoken

# ------ PART 1 OpenAI settings
# OpenAI API key
openai.api_key = "PLACE_API_KEY_HERE"

# ChatGPT Initialize AI NPC
# Change the ai_behavior and/or first question to 
ai_behavior='''
    This is a simulated discussion with a cybernetic xenophobic alien named Darfo from the planet Daria.
    Your race is called the Darian Collective. Your alien race is made up of self-replicating artificial intelligent aliens.
    You speak in scientific metaphors and give short and rude answers.
    '''
first_question = "This is Captain Josef Rybar of the Union starship U.S.S Carpathia. We come in peace and with the utmost respect for your culture and way of life. We are eager to establish peaceful communication and to learn from one another. We hope that our encounter will lead to mutual understanding and a lasting relationship. Please respond if you are able, and let us know how we may respectfully proceed.\n"

messages=[
    {"role": "system", "content": ai_behavior},
    {"role": "user", "content": first_question}
    ]

# ChatGPT Initialize AI Arbiter
arbiter_info = "You only answer yes or no and check whether the statement mentions anything about a meeting taking place."
arbiter_messages_default = [{"role": "system", "content": arbiter_info}]

# Initialize GPT model parameters
model="gpt-3.5-turbo"

# ------ PART 2 GPT Functions
# GPT reponse function
def GPTresponse(model,messsage_prompt,max_tokens,temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messsage_prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response

# Count number of tokens (source: https://github.com/Azure/openai-samples/blob/main/Basic_Samples/Chat/chatGPT_managing_conversation.ipynb)
def num_tokens_from_messages(messsage_prompt, model):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messsage_prompt:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


# ------ PART 3 Tkinter GUI Initialize
# Tkinter GUI
root = tk.Tk()
root.title("First Contact GPT")

# define window dimensions
window_width = 800
window_height = 600

# get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

# Main window sizing and other options
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)
root.iconbitmap("./assets/icon.ico")

# load default image
mainviewer_img = tk.PhotoImage(file='./assets/main_viewer_intro_0.png')
logo_img = tk.PhotoImage(file='./assets/FirstContactGPT.png')

# ------ PART 4 GUI functions
# Button ask questions
def print_text(dummy=None):
    global messages
    global discussion
    global qAsked
    global model
    # retrieve the message
    text = textEntry.get("1.0", "end")
    textEntry.delete("1.0","end")
    textEntry.focus()
    # delete double break line at the end when pressing enter
    text = text.replace("\n\n", "\n")
    # GPT 3.5 fix so that the AI stays in character:
    if len(messages)>3:
        messages.pop(-3) # This will keep system message as third last
        messages.append({"role": "system", "content": ai_behavior})
    messages.append({"role": "user", "content": text})
    # check number of tokens so far
    num_tokens = num_tokens_from_messages(messages, model)
    # delete first prompt-answer pair if number of tokens reach a critical level:
    if num_tokens > 3900:
        messages.pop(1)
        messages.pop(1)
    #print(messages)
    #print(num_tokens)
    # show message in the text window
    discussion["state"] = "normal"
    discussion.insert(tk.INSERT, "\n\nYou: ")
    discussion.insert(tk.INSERT, text)
    discussion["state"] = "disabled"
    discussion.see(tk.END)
    # Run GPTprompt, the GPTprompt is split to improve the UX.
    # Otherwise you would have to wait for your message to appear together with AI's response. 
    qAsked = True  

# GPT prompting function & Check Objectives
def GPTprompt():
    global messages
    global model
    global discussion
    global discussion_bg
    global objective_2_state
    global objective_2
    global objective_3_state
    global objective_3
    global objective_4_state
    global objective_4
    global objective_5_state
    global objective_5
    global arbiter_messages_default

    # Add Alien: to text
    discussion["state"] = "normal"
    discussion.insert(tk.INSERT, "\nAlien: ")
    discussion["state"] = "disabled"
    discussion.see(tk.END)

    # Do prompt
    answer = ""
    response = GPTresponse(model,messages,200,1)
    answer = response['choices'][0]['message']['content']
    # If answer begins with "Darfo: "
    answer = answer.replace("Darfo: ", "")
    messages.append({"role": "assistant", "content": answer})
    discussion_bg = discussion.get("1.0", "end") + answer

    # Check objectives
    answerList = answer.lower().split(" ")
    answerList = [[word.replace("\n", "").replace(".", "").replace(",","")] for word in answerList]
    # Objective 2
    if objective_2_state.get() == 0:
        if ["daria"] in answerList:
            objective_2_state = tk.IntVar(value=1)
            objective_2["variable"] = objective_2_state
    # Objective 3
    if objective_3_state.get() == 0:
        if ["darian"] in answerList or ["darians"] in answerList:
            objective_3_state = tk.IntVar(value=1)
            objective_3["variable"] = objective_3_state
    # Objective 4
    if objective_4_state.get() == 0:
        if ["darfo"] in answerList:
            objective_4_state = tk.IntVar(value=1)
            objective_4["variable"] = objective_4_state
    # Objective 5 - checked by GPT
    if objective_5_state.get() == 0:
        arbiter_question = f"Consider the following statement: {answer} \n\nDoes is mention that meeting will take place?"
        arbiter_messages = arbiter_messages_default.copy()
        arbiter_messages.append({"role": "user", "content": arbiter_question})
        arbiter_response = GPTresponse(model,arbiter_messages,10)
        arbiter_answer = arbiter_response['choices'][0]['message']['content']
        #print(arbiter_answer)
        if arbiter_answer.lower().replace(".", "").replace(",", "") == "yes":
            objective_5_state = tk.IntVar(value=1)
            objective_5["variable"] = objective_5_state

# ------ PART 5 GUI elemtents und widgets
# define widgets
mainviewer = tk.Label(root, image=mainviewer_img)
logo = tk.Label(root, image=logo_img)
objectivesTitle = tk.LabelFrame(root, text="Objectives")
discussion = ScrolledText(root, wrap=tk.WORD, state='disabled')
you = tk.StringVar()
youLabel = tk.Label(root, text="You:")
textEntry = tk.Text(root, wrap=tk.WORD)
textEntry.focus()
btn = tk.Button(root, text="Say", command=print_text)
# bind enter to do the same function as button
root.bind('<Return>', print_text)

# objectives
objective_1_state = tk.IntVar(value=0)
objective_1 = tk.Checkbutton(objectivesTitle, text="Establish contact with the alien planet", state="disabled", variable=objective_1_state)
objective_2_state = tk.IntVar(value=0)
objective_2 = tk.Checkbutton(objectivesTitle, text="Find out the name of the alien planet", state="disabled", variable=objective_2_state)
objective_3_state = tk.IntVar(value=0)
objective_3 = tk.Checkbutton(objectivesTitle, text="Find out the name of the alien race", state="disabled", variable=objective_3_state)
objective_4_state = tk.IntVar(value=0)
objective_4 = tk.Checkbutton(objectivesTitle, text="Find out the name of the alien representative", state="disabled", variable=objective_4_state)
objective_5_state = tk.IntVar(value=0)
objective_5 = tk.Checkbutton(objectivesTitle, text="Negotiate a personal meeting with the aliens", state="disabled", variable=objective_5_state)

# place widgets
mainviewer.place(x=0, y=0)
logo.place(x=505, y=5)
objectivesTitle.place(x=505, y=40, width=290, height=313)
discussion.place(x=2, y=355, relwidth=1, height=150)
youLabel.place(x=2, y=510)
textEntry.place(x=40, y=510, width=650, height=85)
btn.place(x=695, y=510, width=100, height=85)
objective_1.pack(anchor="w")
objective_2.pack(anchor="w")
objective_3.pack(anchor="w")
objective_4.pack(anchor="w")
objective_5.pack(anchor="w")

# ------ PART 6 Game elements and event handlers
# load game elements
discussion_text = ""
intro_message = """Helm: Captain, we have reached the 4th planet of the Tau Ceti system.\n 
You: Thank you Ensign. Lieutenant Novak, hail the representatives of this planet. Let's see how they respond.\n 
Lt. Novak: Channel opened, sir.\n 
You: """
intro_message = intro_message + first_question
intro_message_length = len(intro_message.split(" "))
intro_text_counter = 0
event_intro_finished = False
event_intro_cutscene = False
event_intro_fly = False
cutscene_counter = 0
discussion_bg = intro_message
qAsked = False
firstQanswered = False
missionSuccess = False

# ------ PART 7 Infinite loop
# infinite loop function
def infinite_loop():
    global intro_text_counter
    global discussion_text
    global discussion_bg
    global intro_message
    global intro_text_counter
    global event_intro_finished
    global event_intro_cutscene
    global event_intro_fly
    global cutscene_counter
    global objective_1
    global objective_1_state
    global objective_2_state
    global objective_3_state
    global objective_4_state
    global objective_5_state
    global qAsked
    global firstQanswered
    global missionSuccess
    global mainviewer_img
    global mainviewer

    # set default refresh rate in ms
    refresh_rate = 100

    # For the infinite loop to function properly the eventes are called as follows
    # CONDITION 1 - Output AI reponse word after word and animate character
    if event_intro_finished == True and qAsked == False:
        # Output AI message
        if len(discussion_bg.split(" ")) != len(discussion.get("1.0", "end").split(" "))-1:
            wordposition = len(discussion_bg.split(" ")) - len(discussion.get("1.0", "end").split(" "))
            discussion["state"] = "normal"
            discussion.insert(tk.INSERT, discussion_bg.split(" ")[-wordposition-1].replace("\n","") + " ")
            discussion["state"] = "disabled"
            discussion.see(tk.END)
            # Animate character talking
            img_path = f'./assets/main_viewer_character_talking_{randint(0,3)}.png'
            mainviewer_img['file'] = img_path
        else:
            # Animate character blinking
            if random()>0.95:
                img_path = './assets/main_viewer_character_1.png'
                mainviewer_img['file'] = img_path
            else:
                img_path = './assets/main_viewer_character_0.png'
                mainviewer_img['file'] = img_path

    # CONDITION 2 - General Discussion - GPT Prompt question
    if event_intro_finished == True and qAsked == True:
        GPTprompt()
        qAsked = False
    
    # CONDITION 3 - First automated question during intro - GPT Prompt question
    if event_intro_finished == False and firstQanswered == True:
        GPTprompt()
        event_intro_finished = True

    # CONDITION 4 - Scripted intro
    if event_intro_finished == False and firstQanswered == False:
        # Intro Fly Cutscene
        if event_intro_cutscene == False:
            cutscene_counter += 1
            img_path = f'./assets/main_viewer_intro_{cutscene_counter}.png'
            mainviewer_img['file'] = img_path
            # End Intro Fly Cutscene
            if cutscene_counter >= 18:
                event_intro_cutscene = True
        
        # Intro Communication
        else:
            if intro_text_counter < intro_message_length:
                current_word = str(intro_message.split(" ")[intro_text_counter]) + " "
                discussion["state"] = "normal"
                discussion.insert(tk.INSERT, current_word)
                discussion["state"] = "disabled"
                discussion.see(tk.END)
                intro_text_counter += 1
                
                # Pauses between discussions (override default refresh rate):
                if intro_text_counter in [13,30,35,105]:
                    refresh_rate = 1500

                if intro_text_counter == 105:
                    objective_1_state = tk.IntVar(value=1)
                    objective_1["variable"] = objective_1_state
            else:
                # Finished intro
                discussion_bg = discussion.get("1.0", "end")
                firstQanswered = True

    # Mission success Pop-Up
    if missionSuccess == False:
        if len(discussion_bg.split(" ")) == len(discussion.get("1.0", "end").split(" "))-1:
            if objective_2_state.get() == 1 and objective_3_state.get() == 1 and objective_4_state.get() == 1 and objective_5_state.get() == 1:
                showinfo("Misson Accomplished!", "Well done Captian!\nYou have successfully completed the mission! You can with the discussion or try again by restrating the program.\nAlternatively you can try changing the behavior of the AI in the source code.")
                missionSuccess = True

    root.after(refresh_rate, infinite_loop)

root.after(1000, infinite_loop)
root.mainloop()