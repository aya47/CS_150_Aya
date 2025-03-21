"""
CS 150 Final Project: 40-year Simulation in financial literacy
Author: Aya Ben Saghroune
Edit Date: Thursday, March 20th, 2025
This file contains:
- Person class
- Simulation class
- run_tests function
- Main program

A UML diagram and a FinancialLiteracyResponses.txt file for responses are submitted separately

"""

# Constants
INITIAL_SAVINGS = 5000.0
INITIAL_DEBT = 30100.0
HOUSE_COST = 175000.0
MONTHLY_RENT = 850.0
RENT_PER_YEAR = MONTHLY_RENT * 12  # $10,200 per year
INCOME = 59000.0
SAVINGS_DEPOSIT = INCOME * 0.20  # 20% of income: $11,800 per year into savings
CHECKING_DEPOSIT = INCOME * 0.30  # 30% of income: $17,700 per year into checking
FL_SAVINGS_RATE = 0.07  # 7% annual interest
NFL_SAVINGS_RATE = 0.01 # 1% annual interest
HOUSE_DOWN_PAYMENT_FL = 0.20 * HOUSE_COST  # $35,000 down for fl
HOUSE_DOWN_PAYMENT_NFL = 0.05 * HOUSE_COST  # $8,750 down for nfl
MORTGAGE_RATE_FL = 0.045  # 4.5% annual for fl
MORTGAGE_RATE_NFL = 0.05  # 5% annual for nfl (including PMI)
MONTHS_IN_YEAR = 12
TOTAL_YEARS = 40

class Person:
    """
    Represents a person with financial attributes and methods to update their accounts.
    """
    def __init__(self, is_financially_literate: bool):
        """
        Initializes the person
        
        is_financially_literate: True if the person is fl, False otherwise (nfl)
        """
        self.is_financially_literate = is_financially_literate
        self.savings = INITIAL_SAVINGS
        self.checking = 0.0
        self.debt = INITIAL_DEBT
        self.loan = 0.0
        self.has_house = False
        # Set the appropriate mortgage rate
        self.mortgage_rate = MORTGAGE_RATE_FL if is_financially_literate else MORTGAGE_RATE_NFL

    def add_income(self):
        """
        Adds the annual income in savings and checking
        $11,800 goes to savings and $17,700 goes to checking
        """
        self.savings += SAVINGS_DEPOSIT
        self.checking += CHECKING_DEPOSIT

    def update_savings(self):
        """
        Updates the savings account after one year with interest
        fl invests in a mutual fund of 7% return
        nfl uses a simple savings account of 1% return
        """
        # assign interest rate depending on financial_literacy status
        rate = FL_SAVINGS_RATE if self.is_financially_literate else NFL_SAVINGS_RATE
        # savings increase by interest_rate after one year 
        self.savings *= (1 + rate)

    def update_debt(self):
        """
        Simulates monthly debt payments for one year and applies 20% annual interest on any remaining debt

        Each month, the minimum payment is 3% of the remaining debt plus an additional $15 for fl OR $1 for nfl 

        Payments stop once the debt is cleared
        
        Returns: 
            total_payment: Total debt payment made during the year
        """
        # initialize return value to zero: counter for amount paid in that year
        total_payment = 0.0
        for _ in range(MONTHS_IN_YEAR): # loop over the 12 months
            if self.debt <= 0:
                self.debt = 0
                # debt is paid off, move on
                break 
            monthly_minimum = self.debt * 0.03
            #extra $15 for fl, extra $1 for nfl
            additional = 15 if self.is_financially_literate else 1 
            payment = monthly_minimum + additional
            # Tweak: only pay the remaining debt if it's less than the total payment that adds the extra payment -> + accuracy
            if payment > self.debt:
                payment = self.debt
            self.debt -= payment
            total_payment += payment
        # 20% annual interest if debt remains for the next year 
        if self.debt > 0:
            self.debt *= 1.2
        return total_payment

    def pay_rent(self):
        """
        Subtracts the annual rent ($850 per month for FL and NFL) from the checking account
        """
        # check if rent amount is available in checking account
            # -> avoid a negative checking balance 
        if self.checking > RENT_PER_YEAR:
            self.checking -= RENT_PER_YEAR
        # if not, take the remaining amount from savings balance 
        else:
            self.savings -= (RENT_PER_YEAR - self.checking)
            self.checking = 0

    def purchase_house(self):
        """
        Purchases a house if the person has enough in checking for the required down payment

        The required down payment out of the house cost is:
        FL: 20%
        NFL: 5%

        After purchasing, the loan amount is set to the house cost minus the down payment
        and the house flag is set to True

        I created a separate method to update mortgage loan balance with applied interest every year
        """
        if self.is_financially_literate:
            down_payment = HOUSE_DOWN_PAYMENT_FL
        else:
            down_payment = HOUSE_DOWN_PAYMENT_NFL
        if self.checking >= down_payment:
            self.checking -= down_payment
            self.loan = HOUSE_COST - down_payment
            self.has_house = True

    def update_mortgage(self):
        """
        Update mortgage loan balance with applied interest every year
        The monthly payment is calculated based on a 30-year term (360 months) and the applicable mortgage rate based on fl status
        Eveery month, the payment reduces the loan balance and is deducted from the checking account.
        """
        if self.loan <= 0:
            return
        N = 360  # total number of payments (30 years -> 360 months)
        monthly_interest = self.mortgage_rate / 12 
        # Calculate the discount factor
        discount_factor = ((1 + monthly_interest) ** N - 1) / (monthly_interest * ((1 + monthly_interest) ** N))
        monthly_payment = self.loan / discount_factor
        for _ in range(MONTHS_IN_YEAR):
            if self.loan <= 0:
                self.loan = 0
                break # mortgage loan is cleared, move on
            interest_payment = self.loan * monthly_interest
            principal_payment = monthly_payment - interest_payment
            self.loan -= principal_payment
            self.checking -= monthly_payment

    def get_wealth(self):
        """
        Returns the Person's wealth, qhich is:
            wealth = savings + checking - debt - loan
        The value is rounded to the nearest integer (needed for viz)
        """
        return round(self.savings + self.checking - self.debt - self.loan)

    def __str__(self):
        status = "Financially Literate" if self.is_financially_literate else "Not Financially Literate"

        return (f"{status} Person - Savings: ${self.savings:.2f}, Checking: ${self.checking:.2f}, "
                f"Debt: ${self.debt:.2f}, Loan: ${self.loan:.2f}, Has House: {self.has_house}")

class Simulation:
    """
    Simulates 40 years of financial decisions for a Person instance
    Tracks the number of years in debt, years spent renting, and total debt paid.
    """
    def __init__(self, person: Person):
        self.person = person
        self.years_in_debt = 0
        self.rented_years = 0
        self.total_debt_paid = 0.0

    def run_simulation(self):
        """
        Runs the simulation for 40 years

        Each year:
                The person receives income
                Savings are updated with interest.
                Debt payments are made.
                Depending on whether the person has purchased a house:
                    Pay rent
                    Pay mortgage 
        Returns:
            wealth_history [list]: 41 wealth values (initial wealth plus one for each of the 40 years )
        """
        wealth_history = []
        # Record initial wealth (should be -25100 for 5000 - 30100 = -25100)
        wealth_history.append(self.person.get_wealth())
        
        for _ in range(1, TOTAL_YEARS + 1):

            # Add annual income
            self.person.add_income()

            # Update savings with interest rate
            self.person.update_savings()

            # Update debt with monthly payments and annual interest

            debt_payment = self.person.update_debt() #Note: all corresponding interest rates are taken into account in
            self.total_debt_paid += debt_payment

            # Count year as in debt if any debt or mortgage remains
            if self.person.debt > 0 or self.person.loan > 0:
                self.years_in_debt += 1
            
            # Housing: if no house has been purchased, check if down payment can be made
            if not self.person.has_house:
                threshold = HOUSE_DOWN_PAYMENT_FL if self.person.is_financially_literate else HOUSE_DOWN_PAYMENT_NFL
                if self.person.checking >= threshold:
                    self.person.purchase_house()
                else:
                    self.person.pay_rent()
                    self.rented_years += 1
            else:
                # If a house has been purchased, make monthly mortgage payments
                self.person.update_mortgage()
            
            wealth_history.append(self.person.get_wealth())
        return wealth_history

def run_tests():
    """

    Runs test cases for Person and Simulation methods
    Each method is tested with at least three cases

    """
    # Test Person constructor and initial values
    p1 = Person(True)
    assert p1.savings == INITIAL_SAVINGS, "Initial savings should be $5000"
    assert p1.debt == INITIAL_DEBT, "Initial debt should be $30100"
    assert p1.checking == 0, "Initial checking should be $0"
    assert not p1.has_house, "Initially, the person should not have a house"
    
    p2 = Person(False)
    assert p2.mortgage_rate == MORTGAGE_RATE_NFL, "nfl mortgage rate should be 5%"
    assert p2.is_financially_literate is False, "p2 should be non-financially literate"
    
    # Test add_income method
    p_test = Person(True)
    init_savings = p_test.savings
    init_checking = p_test.checking
    p_test.add_income()
    assert p_test.savings == init_savings + SAVINGS_DEPOSIT, "Savings should increase by 20% of income"
    assert p_test.checking == init_checking + CHECKING_DEPOSIT, "Checking should increase by 30% of income"
    print(f"add_income test passed!")
    
    # Test update_savings method for financially literate (7% interest)
    p_test.savings = 1000
    p_test.is_financially_literate = True
    p_test.update_savings()
    expected = 1000 * (1 + FL_SAVINGS_RATE)
    assert abs(p_test.savings - expected) < 0.01, "Savings update for fl should apply 7% interest"
    print(f"update_savings FL test passed!")
    
    # Test update_savings method for non-financially literate (1% interest)
    p_test.savings = 1000
    p_test.is_financially_literate = False
    p_test.update_savings()
    expected = 1000 * (1 + NFL_SAVINGS_RATE)
    assert abs(p_test.savings - expected) < 0.01, "Savings update for nfl should apply 1% interest"
    print(f"update_savings NFL test passed!")
    
    # Test update_debt method with simulated payments
    p_debt = Person(True)
    p_debt.debt = 1000  # set a small debt amount
    payment = p_debt.update_debt()
    assert payment >= 45, "Debt payment should be at least $45 for fl with $1000 debt"
    print(f"update_debt FL test passed!")
    
    # Test update_debt for debt that can be fully paid in one month
    p_debt2 = Person(False)
    p_debt2.debt = 10
    payment2 = p_debt2.update_debt()
    assert p_debt2.debt == 0, "Debt should be zero if fully paid off"
    print(f"update_debt NFL test passed!")
    
    # Test pay_rent method
    p_rent = Person(True)
    p_rent.checking = 20000
    p_rent.pay_rent()
    assert abs(p_rent.checking - (20000 - RENT_PER_YEAR)) < 0.01, "Rent payment should subtract $10,200 from checking"
    print(f"pay_rent test passed!")
    
    # Test purchase_house method for fl
    p_house = Person(True)
    p_house.checking = 40000
    p_house.purchase_house()
    assert p_house.has_house, "Person should purchase a house when sufficient funds are available"
    expected_loan_fl = HOUSE_COST - HOUSE_DOWN_PAYMENT_FL
    assert abs(p_house.loan - expected_loan_fl) < 0.01, "Loan should be house cost minus down payment for fl"
    print(f"purchase_house test for FL passed!")
    
    # Test purchase_house method for nfl
    p_house2 = Person(False)
    p_house2.checking = 10000
    p_house2.purchase_house()
    assert p_house2.has_house, "nfl should purchase a house if checking >= down payment threshold"
    expected_loan_nfl = HOUSE_COST - HOUSE_DOWN_PAYMENT_NFL
    assert abs(p_house2.loan - expected_loan_nfl) < 0.01, "Loan should be house cost minus down payment for nfl"
    print(f"purchase_house test for NFL passed!")
    
    # Test update_mortgage method
    p_mortgage = Person(True)
    p_mortgage.checking = 50000
    p_mortgage.loan = 100000  # sample loan balance
    p_mortgage.has_house = True
    prev_loan = p_mortgage.loan
    p_mortgage.update_mortgage()
    assert p_mortgage.loan < prev_loan, "Loan should decrease after a mortgage payment"
    print(f"update_mortgage test for fl passed!")
    
    # Test Simulation run_simulation method (wealth history length should be 41: initial + 40 years)
    p_sim = Person(True)
    sim = Simulation(p_sim)
    wealth_history = sim.run_simulation()
    assert len(wealth_history) == TOTAL_YEARS + 1, "Wealth history should have 41 entries (initial wealth + 40 years)"
    print(f"run_simulation test passed!")
    
    print("All tests passed!")

# Main Program
# Run tests first
run_tests()

# Create two persons for simulation:
# fl: financially literate
fl_person = Person(True)
# nfl: not financially literate
nfl_person = Person(False)

# Create simulations for both persons
sim_fl = Simulation(fl_person)
sim_nfl = Simulation(nfl_person)

# Run the 40-year simulation for both
wealth_history_fl = sim_fl.run_simulation()
wealth_history_nfl = sim_nfl.run_simulation()

# Print simulation results
print("\nFinancially Literate Person Wealth Over 40 Years:")
print(wealth_history_fl)

print("\nNon-Financially Literate Person Wealth Over 40 Years:")
print(wealth_history_nfl)

# Print Stats for Fl and Nfl
print("\nAdditional Metrics:")
print(f"Financially Literate: Years in debt = {sim_fl.years_in_debt}, Rented years = {sim_fl.rented_years}, Total debt paid = ${sim_fl.total_debt_paid:.2f}, Total Wealth = {fl_person.get_wealth()}")
print(f"Non-Financially Literate: Years in debt = {sim_nfl.years_in_debt}, Rented years = {sim_nfl.rented_years}, Total debt paid = ${sim_nfl.total_debt_paid:.2f}, Total Wealth = {nfl_person.get_wealth()}")
print(f"FL has ${fl_person.get_wealth()-nfl_person.get_wealth()} more in wealth than NFL after 40 years")

# My touch:  visualize the evolution of wealth over 40 years for FL and NFL
# Create a graph to compare their wealtj
import matplotlib.pyplot as plt

years = list(range(TOTAL_YEARS+1))
plt.figure()
plt.plot(years, wealth_history_fl, label="FL Person")
plt.plot(years, wealth_history_nfl, label="NFL Person")
plt.xlabel("Years")
plt.ylabel("Wealth ($)")
plt.title("Wealth Evolution over 40 years")
plt.grid(True)
plt.legend()
plt.show()

# Create FinancialLiteracyResponses.txt
with open("FinancialLiteracyResponses.txt", "w") as f:
    # Answer to question #1
    f.write("Answer to question #1\n")
    f.write("I learned that how much of a difference a house down payment makes\n")
    f.write("I also realized the power of paying just a few more dollars in debt per month, and how it accumulates over the years because of interest\n")
    
    # Answer to question #2
    f.write("\nAnswer to question #2\n")
    difference_in_paid_debt = sim_nfl.total_debt_paid - sim_fl.total_debt_paid
    f.write(f"nfl ended up paying ${difference_in_paid_debt:.3f} more in debt than fl\n")

    # Answer to question 3
    f.write("\nAnswer to question #3\n")
    f.write("fl and nfl were in debt for the same number of years per instructions\n")

    # answer to question #4
    f.write("\nAnswer to question #4\n")
    f.write(f"FL has ${fl_person.get_wealth()-nfl_person.get_wealth()} more in wealth than NFL after 40 years\n")

    # Answer to question #5
    f.write("\nAnswer to question #5\n")
    f.write("I think the biggest thing is investing in a high-yields savings account\n")
    f.write("While nfl was losing an average of 1% per year on their money due to inflation after the 1% simple interest\n")
    f.write("FL was investing with a 7% yearly return, which compouds to millions of dollars over time\n")
    f.write("The power of compound growth should not be underestimated\n")