#   =====================   TASK   =====================
#   Capstone Project - Variables and Control Structures



#   *******  CAPSTONE PROJECT  *******
#   What this program would do:
#      A menu is shown to the user
#      The user is asked to choose which calculation they want to do: "investment" or "bond"
#      If the user doesn’t type in a valid input, an error message will be shown
#      If the user selects ‘investment’, the following will be performed:
#         Ask the user to input the amount of money that they are depositing, and store it
#             in a variable called principal
#         Ask the user to input the interest rate (as a percentage), and store this in a
#             variable called rate [It is assumed that the user will input a number, but
#             not a number with percentage sign]
#         Ask the user to input the number of years they plan on investing, and store this
#             in a variable called years
#         Ask the user to input if they want “simple” or “compound” interest and store this
#             in a variable called interest
#         If neither "simple" nor "compound" is found in interest, print out error message
#         If "simple" is found in interest, do the following:
#             calculate the amount that will be got back using the simple interest formula, and
#             print out the amount showing also the interest type as simple
#         If "compound" is found in interest, do the following:
#             calculate the amount that will be got back using the compound interest formula, and
#             print out the amount showing also the interest type as compound
#      If, otherwise, the user selects ‘bond’, do the following:
#         Ask the user to input the present value of the house and store it in a variable
#             called present_val
#         Ask the user to input the interest rate (as a percentage), and store this in a
#             variable called rate [It is assumed that the user will input a number, but
#             not a number with percentage sign]
#         Ask the user to input the number of months they plan to take to repay the bond, and
#             store it in a variable called months
#         Calculate how much money the user will have to repay each month using the bond
#             repayment formula
#         Print out the amount of money they have to repay each month

#   NOTE: Both amounts in simple and compound interest rate are shown if user type both in 
#         their responses.


#   ********  START OF CAPSTONE PROJECT CODE  ********


import math

#   Accept input of 3 integers
print("\n\ninvestment - to calculate the amount of interest you'll earn on your investment")
print("bond - to calculate the amount you'll have to pay on a home loan \n")
action = input("Enter either 'investment' or 'bond' from the menu above to proceed: ").strip().lower()

#   Show error message if input is neither 'investment' nor 'bond'
if action != "investment" and action != "bond":
    print("\nINPUT ERROR: The input is neither 'investment' nor 'bond'!")

#   Accept amount of money, interest rate and number of years and calculate total amout for investment
elif action == "investment":
    principal = float(input("\nEnter the amount of money you are depositing: "))
    percent_rate = float(input("Enter the interest rate (as a percentage): "))
    years = float(input("Enter number of years you plan on investing: "))
    interest_type = input("Enter 'simple' or 'compound' as the type of interest: ").lower()
    rate = percent_rate / 100
    if "simple" not in interest_type and "compound" not in interest_type:
        print("\nThe total amount is could not be calculated as neither 'simple' nor 'compound' is chosen.")
    else:
        if "simple" in interest_type:
            total_amount = principal * (1 + rate * years)
            print("\nThe total amount is {:.2f} in simple interest.".format(total_amount))
        if "compound" in interest_type:
            total_amount = principal * math.pow((1 + rate), years)
            print("\nThe total amount is {:.2f} in compound interest.".format(total_amount))

#   Accept present value, interest rate and number of months and calculate repayment amout for bond
else:
    present_val = float(input("\nEnter the present value of the house: "))
    percent_rate = float(input("Enter the interest rate (as a percentage): "))
    months = int(input("Enter number of months they plan to take to repay the bond: "))
    monthly_rate = percent_rate / 100 / 12
    repayment = (monthly_rate * present_val)/(1 - (1 + monthly_rate)**(-months))
    print("\nThe monthly repayment is {:.2f}.".format(repayment))


#   ********  END OF CAPSTONE PROJECT CODE  ********

