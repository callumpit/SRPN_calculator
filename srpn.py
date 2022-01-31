# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 00:44:38 2021

@author: Callum Pitceathly
"""



# This is your SRPN file. Make your changes here.
digits = "0123456789"
operators = ["-", "+", "*", "/", "%", "^"] # Use to check operator precidence
dig_op = "0123456789+-*/%^=r"

sat_max = 2147483647    # Saturation values
sat_min = -2147483648

stack1 = []   # Number stack
stack2 = []   # Operator stack

rand_list = [1804289383,
             846930886,
             1681692777,
             1714636915,
             1957747793,
             424238335,
             719885386,
             1649760492,
             596516649,     # List of random numbers
             1189641421,
             1025202362,
             1350490027,
             783368690,
             1102520059,
             2044897763,
             1967513926,
             1365180540,
             1540383426,
             304089172,
             1303455736,
             35005211,
             521595368]

rand_index = [0]
comment_bool = [False]
inline_bool = [False]


def call_rand(r_val):
    if r_val >= 0 and r_val <= 21:  # Function used to cycle through the
        return rand_list[r_val]    # random number list.
    else:
        call_rand(r_val - 22)


def operator(val1, val2, op):
    """
    This Function takes two values and an operation as a string and performs
    the operation given in the string.

    Parameters
    ----------
    val1 : Int
        First number.
    val2 : TYPE
        Second Number.
    op : String
        Operation to be performed.

    Returns
    -------
    Int
        Returns integer result of required operation.

    """
    if op == "+":                   # Addition operator.
        result = val1 + val2

    elif op == "-":                 # Subtraction operator.
        result = val1 - val2

    elif op == "/":
        if val2 == 0:
            print("Divide by 0.")  # Floor Division operator.
            return None
        else:
            result = val1 / val2

    elif op == "%":
        result = val1 % val2

    elif op == "*":                 # Multiplication operator.
        result = val1 * val2

    elif op == "^":                 # Power operator.
        if val2 > 0:
            result = val1 ** val2
        else:
            print("Negative power.")  # Specifications doesn't allow
            return None                                # negative powers.
    try:
        if result > sat_max:  # Check for saturation.
            return sat_max

        elif result < sat_min:
            return sat_min

        else:
            return result

    except:
        pass



def output_function(List):
    for i in List:
        # print(i)
        print(int(i))



def single_input_check(string):
    checker = False

    if len(string) > 1:
        for i in range(0, len(string)):
            if string[i] == "-" and string[i+1] in digits:
                checker = True
            elif string[i] in digits:
                checker = True
            else:
                checker = False
                return checker

    else:
        checker = True

    return checker


def process_command(command):

    if single_input_check(command) == True:
        if comment_bool[0] == False:
            try:
                # If input is an integer add single value to stack
                number = int(command)
                # print("number is {}".format(number))
                if len(stack1) == 23:
                    print("Stack overflow.")
                else:
                    if command[0] == "0":  # Positive octal input
                        for i in range(0, len(command)):
                            if command[i] != "0":    # Check how many preceding zeros
                                length = len(command) - i
                                break
                        if length > 19:
                            number = -1
                        else:  # ------------- Check for 8s and 9s-------------
                            number = 0
                            for i in range(1, len(command)+1):
                                if int(command[-i]) > 7: return None
                                number += (int(command[-i]) * (8**(i-1)))
                        stack1.append(number)

                    elif command[0] == "-" and command[1] == "0":  # Negative octal input
                        for i in range(1, len(command)):
                            # Check how many preceding zeros.
                            if command[i] != "0":
                                length = len(command) - i
                                break
                        if len(command) > 19:
                            number = 0
                        else:
                            for i in range(1, len(command)):
                                if int(command[-i]) > 7: return None
                                number += (int(command[-i]) * (8**(i-1)))
                        stack1.append(number)

                    else:
                        if number > sat_max:
                            # Check against saturation
                            stack1.append(sat_max)
                        elif number < sat_min:
                            stack1.append(sat_min)  # values.
                        else:
                            stack1.append(number)

            except:
                if command == "#":
                    comment_bool[0] = True

                elif command == " " or command == "":
                    pass

                elif command == "+" or command == "-" or command == "/" or \
                        command == "*" or command == "^" or command == "%":  # If input is an operator, apply it

                    if len(stack1) > 1:
                        operation = operator(stack1[-2], stack1[-1], command)
                        if operation != None:
                            # to the last two integers in the stack
                            b, a = stack1.pop(), stack1.pop()
                            # then append the result.
                            stack1.append(operation)
                        else:
                            pass
                    # except IndexError:
                    else:
                        print("Stack underflow.")

                elif command == "=":  # If input is "=" return the last value in the stack.
                    # print(" = sign")
                    try:
                        # print("stack returned")
                        print(int(stack1[-1]))

                    except:  # Case for empty stack
                        print("Stack empty.")

                elif command == "d":
                    if len(stack1) == 0:
                        return sat_min
                    else:
                        # Print out the stack on command "d"
                        return output_function(stack1)

                elif command == "r":
                    if len(stack1) == 23:
                        print("Stack overflow.")
                    else:
                        # Add random number to stack on command "r"
                        stack1.append(call_rand(rand_index[0]))
                        rand_index[0] += 1

                else:
                    print(f"Unrecognised operator or operand \"{command}\".")

        else:
            if command == "#":
                comment_bool[0] = False  # End comment condition.
            else:
                pass

   

    if single_input_check(command) == False:
        # For non-singular inputs, parse string
        # into components and deal with each seperately.

        string = ""    # Create empty string and build numbers from characters.
        
        for i in range(0, len(command)):
            if command[i] in dig_op:
                    string += command[i]

            else:
                # if command[i] == "=": print(command[i-1])
                # else:
                    if len(string) > 0: inline_string(string)
                    
                    process_command(command[i])
                    string = ""

        if len(string) != 0: inline_string(string) # Ensures the last number/phrase built is inputted.


def inline_string(string):
    number = ""
    for i in range(0, len(string)):
        if string[i] in digits: # build number
            number += string[i]
            
            
        elif i == 0 and string[i] == "-": #check for minus
            number += string[i]
            
        elif string[i] == "=":
            process_command(number)
            process_command(string[i])
            number = ""
            
        elif string[i] == "r":
            process_command(number)
            process_command(string[i])
            number = ""
                
        elif string[i] in operators:
            process_command(number)
            number = ""
            if len(stack2) == 0: # add operators to operator stack
                stack2.append(string[i])
                
            elif len(stack2) > 0:
                if operators.index(string[i]) < operators.index(stack2[-1]): #check operator precidence
                    while len(stack2) > 0: 
                        process_command(stack2.pop()) # Execute operators in operator stack.
                    stack2.append(string[i])
                        
                else:
                    stack2.append(string[i])
    
    process_command(number)
    while len(stack2) > 0:  
        process_command(stack2.pop()) # Execute operators in operator stack.
        
                
                


# This is the entry point for the program.
# Do not edit the below
if __name__ == "__main__":
    # pass
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()

