# This script enables flawless SRPN calculation funtionality up to, and including:
# Section 4 tests
# except for (11+1+1+d) - for which output should be: Stack underflow. \n 13

# SETUP START
# This is the initialisation preamble

# Importing packages from standard library
import re

# Saturation variables
minn = -2147483648 # Maximum 
maxn = 2147483647 # Minimum

stack = [] # Initialising stack

# List of psuedo random "r" values identified in Bath SRPN
list_r = [1804289383,846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368]
indx_r = 0 # Global variable tracks the position of the nth term in list_r, used in conjunction with "r" input logic in line ~158

print("You can now start interacting with the SRPN calculator") # Startup message to user

# SETUP END

# SATURATION FUNCTION
def saturate(raw_val): 
  """ This function saturates a value to the maximum and minimum permitted integers of the SRPN calculator """
  sat_val = raw_val
  if sat_val > maxn:
    sat_val = maxn
  if sat_val < minn:
    sat_val = minn
  return sat_val

# OVERFLOW CHECK FUNCTION
def check_overflow(stack): 
  """ This function caps length of/number of elements in stack to 23 """
  if len(stack) >= 23:
    print("Stack overflow.")
    return True
  else:
    return False

# FILLING STACK FUNCTION
def fill_stack(vstack, value): 
  """ This funtion is needed to check for stack overflow before appending input to stack """
  if not check_overflow(vstack):
    vstack.append(int(value))
  return None

# RETRIEVING STACK FUNCTION
def stack_retrieve(in_list): 
  """ This function retrieves values from the stack for operations and catches underflow cases """
  a = None
  b = None
  if len(in_list) > 1:
    try:
      a = in_list.pop()
      b = in_list.pop()
    except IndexError:
      print("Stack underflow.")  # Displaying relevant error message
  else:
    print("Stack underflow.") # Displaying relevant error message
  return a, b

# CHARACTER CHECK FUNCTION
def isANumber(val): 
  """ This function checks if a variable is a number or a text character """
  res = False
  if not isinstance(val, bool):
    try:
      nval = float(val)
    except ValueError:
      res = False
    else:
      res = True
  else:
    res = False
  return res 

# INTEGER CHECK FUNCTION

# def isInt(a_number): 
#   """ This function checks that a number is an integer """
#   res = False
#   if isANumber(a_number):
#     try:
#       num = int(a_number)
#     except Exception:
#       res = False
#     else:
#       if str(num) == str(a_number):
#         res = True
#       else:
#         res = False
#   else:
#     res = False
#   return res

def isInt(a_number): 
  """ This function checks that a number is an integer and is the successor to the function commented out above as it handles negative numbers better. Both kept for sake of regression testing """
  res = False
  if isANumber(a_number):
    try: 
      num = int(a_number)
    except Exception:
      res = False
    else:
      if str(a_number).strip()[0] in ['-', '+']: # checking is the number has a sign attached
        sign = str(a_number).strip()[0] # capturing the sign (if present)
        if sign == "-": # if the sign is negative then discard
          sign = ""
      else: # if there is no sign, nothing more to do
        sign = ""
      if (sign + str(num)) == str(a_number).strip(): # number & sign compared with original number, if they are the same then number is integer
        res = True
      else:
        res = False
  else:
    res = False
  return res

# STRIPPING FUNCTION
def strip_cases(u_in_raw):
  """ This function strips comments and adds or removes spacing either side of the user input as required using regular expressions. It also accounts for an excecptional case where ^ and = are not separated by a space """
  u_in_exp = re.sub(r"\^=$", "=^", u_in_raw) # excecptional case
  u_in_sgn = re.sub(r"((\+|\-)\d+)", r" \g<1> ", u_in_exp) # Adds spacing around numbers including plus or minus
  # u_in_sgn = re.sub(r"([(\-|\+)\d]+)", r" \g<1> ", u_in_exp) # (redundant, succeeded by the above but kept in case it boke anything)
  # u_in_spc = re.sub(r"(\D+)", r" \g<1> ", u_in_sgn) # Adds spacing before and after operators in string to ensure string is split correcty by this function (doesn't work)
  u_in_cmt = re.sub(r'\#.*\#', '', u_in_sgn) # Removes hashtags and strings bounded by them
  u_in_cmt = u_in_cmt.strip() # Removes redundant whitespaces either side of user input
  return u_in_cmt

# COMPUTATION LOGIC
def SRPN_calculator(u_in):
  """ This is the main calculator function that completes operations after saturating the input and checking if the input is an integer before it can accept the input - it's a bit messy and complex as result of having to prioritise functionality and do enough to make it work in time for submission but it could do with some more cleaning up """
  if isANumber(u_in):
    if isInt(u_in): # First checking input is an integer
      u_in_sat = saturate(int(float(u_in)))
      fill_stack(stack,u_in_sat)
    else: # Catching cases where input is a floating point/not an integer
      print("Unrecognised operator or operand \".\".") # Displaying relevant error message for decimal input
      # if u_in contains "." then do the three lines below to replicate how Bath SRPN calc handles floating input
      split = u_in.split(".")  # Splitting floated value and appending individual integers either side of the "." to the stack separately
      fill_stack(stack,saturate(int(split[0])))
      fill_stack(stack,saturate(int(split[-1])))
  else:
    for lmnt in u_in:
      if lmnt == "=": # Display result of operation
        if len(stack) == 0:
          print("Stack empty.") # Displaying relevant error message for Index Error when stack empty
        else:
          print(stack[-1])
      elif lmnt == "+": # Addition operation
        a, b = stack_retrieve(stack)
        if a is not None and b is not None:
          result = saturate(int(b+a))
          fill_stack(stack,result)
      elif lmnt == "-": # Subtraction operation
        a, b = stack_retrieve(stack)
        if a is not None and b is not None:
          result = saturate(int(b-a))
          fill_stack(stack,result)
      elif lmnt == "*": # Multiplication operation
        a, b = stack_retrieve(stack)
        if a is not None and b is not None:
          result = saturate(int(b*a))
          fill_stack(stack,result)
      elif lmnt == "/": # Division operation
        if stack[-1] != 0: # 1st level divide by zero check to see if operation can be performed
          a, b = stack_retrieve(stack)
          if a is not None and b is not None:
            try: # 2nd level divide by zero check to see if operation can be performed
              result = saturate(int(b/a))
              fill_stack(stack,result)
            except ZeroDivisionError: 
              print("Divide by 0.") # Math Error message - identical to original SRPN
        else:
          print("Divide by 0.") # Math Error message - identical to original SRPN
      elif lmnt == "%": # Modulo operation
        a, b = stack_retrieve(stack)
        if a is not None and b is not None:
          result = saturate(int(b%a))
          fill_stack(stack,result)
      elif lmnt == "^": # Exponentiation operation
        a, b = stack_retrieve(stack)
        if a is not None and b is not None:
          result = saturate(int(b**a))
          fill_stack(stack,result)
      elif lmnt == "d": # Display stack - default value in the stack on startup is the saturated minumum - test by running "d" command in Bath SRPN calculator
        if len(stack) > 0:
          for elmnt in stack:
            print(elmnt)
        else:
          print(minn)
      elif lmnt == "r": # Pseudo random generator of a large integer
        global indx_r
        fill_stack(stack,list_r[indx_r])
        indx_r = (indx_r + 1) % 22
      else:
        print('Unrecognised operator or operand "'+lmnt+'".') # Catching erroneous inputs and displaying each letter in the erroneous string individually

# INPUT AND FILTER LOGIC
while True:
  """ This function handles input to the calculator and the exceptions below catch program termination commands at any point """
  try:
    u_in = input() # program accepts user input
    u_in = strip_cases(u_in).split() # filtering input to calculator compatible form
    for lmnt in u_in: # running each element of the input string through the SPN calculator function
      SRPN_calculator(lmnt)
  except EOFError: # Catches Ctl + D, no error/exit message to display
    break 
  except KeyboardInterrupt: # Catches Ctrl + C, identical error/exit message displayed
    print("exited, interrupt")
    break
