import tkinter as tk
import platform



#### Global Variables ####

state = 0
operation = "+"
operand_one = 0
operand_two = 0
memory = 0
MAX_DIGITS = 21



#### Helper Functions ####

# Function sets display to char

def set_dsp (char):
    
    if (char == "."):
        dsp.configure(text = "0.")
    else:
        dsp.configure(text = char)

# Function appends char to display

def apd_dsp (char):
    
    if (dsp.cget("text") == "0"):
        
        set_dsp(char)
        
    elif (dsp.cget("text") == "-0"):
        
        set_dsp(char)
        dsp.configure(text = "-" + dsp.cget("text"))
        
    else:
        
        if (len(dsp.cget("text")) < MAX_DIGITS):
            
            if (char == "."):
                if ("." not in dsp.cget("text")):
                    dsp.configure(text = dsp.cget("text") + ".")
            else:
                dsp.configure(text = dsp.cget("text") + char)

# Function that adds or takes away - from the display

def neg_dsp ():
    
    if (dsp.cget("text")[0] == "-"):
        dsp.configure(text = dsp.cget("text")[1:])
    else:
        dsp.configure(text = "-" + dsp.cget("text"))

# Function formats numb so that it is not too many characters

def frmt (numb):
    
    sign = ""
    
    if (numb < 0):
        sign = "-"
        numb = -numb
        
    strn = "{:.50f}".format(numb)

    if (len(strn) > MAX_DIGITS):
        num_dec_dig = MAX_DIGITS - strn.find(".") - 1
        if (num_dec_dig >= 0):
            strn = "{:.50f}".format(round(numb, num_dec_dig))[0:MAX_DIGITS]
        else:
            strn = "{:.50f}".format(round(numb))[0:MAX_DIGITS]

    strn = sign + strn

    if ("." in strn):
        while (strn[-1] == "0"):
            strn = strn[:-1]
        if (strn[-1] == "."):
            strn = strn[:-1]

    return strn

# Function evaluates the operation given the two operands

def evaluate ():

    global state, operation, operand_one, operand_two, memory

    try:
        
        result = 0

        if (operation == "+"):
            result = operand_one + operand_two
        elif (operation == "−"):
            result = operand_one - operand_two
        elif (operation == "×"):
            result = operand_one * operand_two
        elif (operation == "÷"):
            result = operand_one / operand_two

        if (result >= 10 ** MAX_DIGITS or result <= -(10 ** MAX_DIGITS)):
            raise OverflowError
        elif (result < 0.1 ** (MAX_DIGITS - 2) and result > -(0.1 ** (MAX_DIGITS - 2))):
            operand_one = 0
            dsp.configure(text = "0")
        else:
            frmt_result = frmt(result)
            operand_one = float(frmt_result)
            dsp.configure(text = frmt_result)
    
    except ZeroDivisionError:
        
        state = 0
        dsp.configure(text = "DIV BY ZERO")
        
    except OverflowError:
        
        state = 0
        dsp.configure(text = "OVERFLOW")



#### Click Functions ####

# Function that is called when 0 is clicked

def click_zero ():
    if (dsp.cget("text") != "0" and dsp.cget("text") != "-0"):
        click_numb("0")

# Function that is called when a digit or . is clicked

def click_numb (num):

    global state, operation, operand_one, operand_two, memory

    if (state == 0):
        state = 1
        set_dsp(num)
        operand_one = float(dsp.cget("text"))
    elif (state == 1):
        state = 1
        apd_dsp(num)
        operand_one = float(dsp.cget("text"))
    elif (state == 2):
        state = 3
        set_dsp(num)
        operand_two = float(dsp.cget("text"))
    elif (state == 3):
        state = 3
        apd_dsp(num)
        operand_two = float(dsp.cget("text"))
    elif (state == 4):
        state = 1
        set_dsp(num)
        operand_one = float(dsp.cget("text"))

    btns[0][0].configure(text = "C")

# Function that is called when = is clicked

def click_equal ():

    global state, operation, operand_one, operand_two, memory

    if (state == 0):
        state = 0
    elif (state == 1):
        state = 1
    elif (state == 2):
        state = 4
        operand_two = float(dsp.cget("text"))
        evaluate()
    elif (state == 3):
        state = 4
        operand_two = float(dsp.cget("text"))
        evaluate()
    elif (state == 4):
        state = 4
        evaluate()

    btns[0][0].configure(text = "C")

# Function that is called when an operation is clicked

def click_oper (opn):

    global state, operation, operand_one, operand_two, memory
    
    if (state == 0):
        state = 2
        if (dsp.cget("text") == "OVERFLOW" or dsp.cget("text") == "DIV BY ZERO"):
            dsp.configure(text = "0")
        operand_one = float(dsp.cget("text"))
        operation = opn
    elif (state == 1):
        state = 2
        operand_one = float(dsp.cget("text"))
        operation = opn
    elif (state == 2):
        state = 2
        operation = opn
    elif (state == 3):
        state = 2
        operand_two = float(dsp.cget("text"))
        evaluate()
        operation = opn
    elif (state == 4):
        state = 2
        operand_one = float(dsp.cget("text"))
        operation = opn

    btns[0][0].configure(text = "C")

# Function that is called when ± is clicked

def click_negate ():

    global state, operation, operand_one, operand_two, memory

    if (state == 0):
        state = 1
        neg_dsp()
        operand_one = float(dsp.cget("text"))
    elif (state == 1):
        state = 1
        neg_dsp()
        operand_one = float(dsp.cget("text"))
    elif (state == 2):
        state = 3
        neg_dsp()
        operand_two = float(dsp.cget("text"))
    elif (state == 3):
        state = 3
        neg_dsp()
        operand_two = float(dsp.cget("text"))
    elif (state == 4):
        state = 1
        neg_dsp()
        operand_one = float(dsp.cget("text"))

    btns[0][0].configure(text = "C")

# Function that is called when AC or C is clicked

def click_clear ():

    global state, operation, operand_one, operand_two, memory
    
    if (btns[0][0].cget("text") == "AC"):
        dsp.configure(text = "0")
        state = 0
        operand_one = 0
        operand_two = 0
    elif (btns[0][0].cget("text") == "C"):
        dsp.configure(text = "0")
        btns[0][0].configure(text = "AC")
        if (state in [0, 1, 4]):
            operand_one = 0
        elif (state in [2, 3]):
            operand_two = 0

# Function that is called when MS is clicked

def click_memset ():

    global state, operation, operand_one, operand_two, memory

    if (dsp.cget("text") == "OVERFLOW" or dsp.cget("text") == "DIV BY ZERO"):
        dsp.configure(text = "0")

    memory = float(dsp.cget("text"))

# Function that is called when MR is clicked

def click_memrcl ():

    global state, operation, operand_one, operand_two, memory

    if (state == 0):
        state = 1
        dsp.configure(text = frmt(memory))
        operand_one = memory
    elif (state == 1):
        state = 1
        dsp.configure(text = frmt(memory))
        operand_one = memory
    elif (state == 2):
        state = 3
        dsp.configure(text = frmt(memory))
        operand_two = memory
    elif (state == 3):
        state = 3
        dsp.configure(text = frmt(memory))
        operand_two = memory
    elif (state == 4):
        state = 1
        dsp.configure(text = frmt(memory))
        operand_one = memory

    btns[0][0].configure(text = "C")



#### Window Setup #####

# Configuring Window

win = tk.Tk()
win.title("Calculator")
if platform.system() == "Windows":
    win.iconbitmap("calculator.ico")
win.geometry("250x250")
win.resizable(False, False)

# Configuring Frame

frm = tk.Frame(win)
frm.pack(padx = 5, pady = 5, fill = "both", expand = True)

# Configuring Grid Size

for row_num in range(6):
    frm.rowconfigure(row_num, minsize = 40, weight = 1)

for col_num in range(4):
    frm.columnconfigure(col_num, minsize = 60, weight = 1)



#### Widgets Setup ####

# Font Variable

if platform.system() == "Linux":
    fnt = ("Dejavu Sans Mono", 12)
else:
    fnt = ("Consolas", 14)

# Adding Display

dsp = tk.Label(frm, text = "0", bg = "#FFFFFF", relief = "sunken", font = fnt, anchor = "e")
dsp.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5, sticky = "nsew")

# Button Variables

btns = []
btn_syms = [["AC", "MS", "MR", "±"], ["7", "8", "9", "÷"], ["4", "5", "6", "×"], ["1", "2", "3", "−"], ["0", ".", "=", "+"]]

def btn_fun (sym):
    if (sym == "0"):
        return click_zero
    elif (sym in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "."]):
        return lambda : click_numb(sym)
    elif (sym == "="):
        return click_equal
    elif (sym in ["+", "−", "×", "÷"]):
        return lambda : click_oper(sym)
    elif (sym == "±"):
        return click_negate
    elif (sym == "AC"):
        return click_clear
    elif (sym == "MS"):
        return click_memset
    elif (sym == "MR"):
        return click_memrcl

# Adding Buttons

for r in range(5):
    
    btn_row = []
    
    for c in range(4):
        
        new_btn = tk.Button(frm, text = btn_syms[r][c], font = fnt, command = btn_fun(btn_syms[r][c]))
        btn_row.append(new_btn)
        
        btn_row[c].grid(row = r + 1, column = c, padx = 5, pady = 5, sticky = "nsew")
        
    btns.append(btn_row)



#### Main Loop ####

win.mainloop()
