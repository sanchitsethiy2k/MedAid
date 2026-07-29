from tabulate import tabulate
import sys
import os
import csv
from datetime import date
import re

class Patient:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @classmethod
    def get_patient(cls):
        aaj = date.today()
        while True:
            try:
                name = validate_name(input("Enter Patient Name: ").title().strip())
                print("")
                break
            except ValueError:
                print("No Name Entered")
                print("")
                continue

        if not os.path.exists(f"{name}.csv"):

            while True:
                try:
                    bday = validate_bday(input("Enter Patient D.O.B (FORMAT: YYYY-MM-DD): ").strip())
                    bday = bday.replace("/", "-")
                    print("")
                    break
                except ValueError:
                    print("Invalid Birth Date Entered (Did u check the format carefully?)")
                    print("")
                    continue

            while True:
                try:
                    gender = validate_gender(input("Enter Patient Gender(M/F): ").upper().strip())
                    if gender.startswith("M"):
                        gender = "M"
                    elif gender.startswith("F"):
                        gender = "F"
                    print("")
                    break
                except ValueError:
                    print("Invalid Gender Entered")
                    print("")
                    continue

            janam = date.fromisoformat(bday)
            if janam.month > aaj.month:
                age = aaj.year - janam.year - 1

            elif janam.month == aaj.month:
                if janam.day > aaj.day:
                    age = aaj.year - janam.year - 1

                else:
                    age = aaj.year - janam.year

            else:
                age = aaj.year - janam.year
        else:
            with open(f"{name}.csv") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    age = int(row["Age"])
                    gender = row["Gender"]

        return cls(name, age, gender)


    def patient_csv(self):
        with open(f"{self.name}.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames = ["Name", "Age", "Gender"])
            writer.writeheader()
            writer.writerow({"Name": self.name, "Age": self.age, "Gender": self.gender})



class Med:
    def __init__(self, patient, med_list):
        self.med = med_list
        self.name = patient.name



    @classmethod
    def get_meds(cls, patient):
        med_list = []
        while True:
            while True:
                try:
                    med = input("Enter Med (Add meds one by one. Type 'Done' when finished): ").strip().title()
                    if not med:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("No Med Entered")
                    print("")

                    continue

            if med == "Done":
                break

            while True:
                try:
                    strength = int(input(f"Strength of {med} (in mg, enter '0' if not sure): ").strip())
                    if strength < 0:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid Strength Entered")
                    print("")

                    continue

            while True:
                try:
                    frequency = int(input(f"Frequency of {med} used (per day): ").strip())
                    if not frequency:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid Frequency Entered")
                    print("")
                    continue

            while True:
                try:
                    doses = int(input(f"Doses of {med} bought: "))
                    if not doses:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid No. Of Doses Entered")
                    print("")
                    continue

            med_list.append({"Med": med, "Strength": strength, "Frequency": frequency, "Doses": doses})

        return cls(patient, med_list)




    def med_csv(self):
        with open(f"{self.name}_med.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames = ["Med", "Strength", "Frequency", "Doses"])
            writer.writeheader()
            writer.writerows(self.med)

    @classmethod
    def load(cls, patient):
        med_list = []
        with open(f"{patient.name}_med.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Frequency"] = int(row["Frequency"])
                row["Strength"] = int(row["Strength"])
                row["Doses"] = int(row["Doses"])
                med_list.append({"Med": row["Med"], "Strength": row["Strength"], "Frequency": row["Frequency"], "Doses": row["Doses"]})

        return cls(patient, med_list)

    def add(self):
        print("")
        print("You currently have the following meds on file")
        print("")
        n = 1
        for row in self.med:
            print(f"{n}. {row['Med']}")
            n += 1
        print("")

        while True:
            while True:
                try:
                    med = input("Enter Med (Add meds one by one. Type 'Done' when finished): ").strip().title()
                    if not med:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("No Med Entered")
                    print("")
                    continue

            if med == "Done":
                break

            while True:
                try:
                    strength = int(input(f"Strength of {med} (in mg, enter '0' if not sure): ").strip())
                    if strength < 0:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid Strength Entered")
                    print("")
                    continue

            while True:
                try:
                    frequency = int(input(f"Frequency of {med} used (per day): ").strip())
                    if not frequency:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid Frequency Entered")
                    print("")
                    continue

            while True:
                try:
                    doses = int(input(f"Doses of {med} bought: "))
                    if not doses:
                        raise ValueError
                    print("")
                    break
                except ValueError:
                    print("Invalid No. Of Doses Entered")
                    print("")
                    continue

            self.med.append({"Med": med, "Strength": strength, "Frequency": frequency, "Doses": doses})


    def refill(self):
        print("")
        print("You currently have the following meds on file:")
        print("")
        n = 1
        for row in self.med:
            print(f"{n}. {row['Med']}")
            n += 1
        print("")
        print("Choose the NUMBER corresponding to the med u would like to refill")
        print("")
        while True:
            try:
                option = int(input("Option: "))
                print("")
                if not 1 <= option <= len(self.med):
                    raise ValueError
                break
            except ValueError:
                print("Invalid Option Entered. Did u enter the NUMBER corresponding to the med?")
                print("")
                continue

        while True:
            try:
                refill_amt = int(input(f"{self.med[option-1]['Doses']} doses of {self.med[option-1]['Med']} currently on file. No. of doses would you like to add: "))
                if not refill_amt >  0:
                    raise ValueError
                break
            except ValueError:
                print("Refill amount must be a whole no. greater than 0")
                print("")
                continue


        self.med[option-1]["Doses"] += refill_amt
        print("")


    def remove(self):
        med_list = []
        print("")
        print("You currently have the following meds on file:")
        print("")
        n = 1
        for row in self.med:
            print(f"{n}. {row['Med']}")
            n += 1
        print("")
        print("Choose the NUMBER corresponding to the med u would like to remove")
        print("")
        while True:
            try:
                option = int(input("Option: ").strip())
                if not 1 <= option <= len(self.med):
                    raise ValueError
                break
            except ValueError:
                print("Invalid Option Entered. Did u enter the NUMBER corresponding to the med?")
                print("")
                continue
        for i in range(len(self.med)):
            if i != option - 1:
                med_list.append(self.med[i])

        self.med = med_list
        print("")

    def log(self):
        log_list = []

        today = date.today()

        for row in self.med:
            n = 1
            print("")
            while n <= row["Frequency"]:
                if row["Doses"] > 0:
                    while True:
                        try:
                            taken = input(f"Dose {n} of {row['Med']} taken today (Y/N): ").strip().upper()
                            if not taken in ["Y", "N", "YES", "NO"]:
                                raise ValueError
                            print("")
                            break

                        except ValueError:
                            print("Invalid Input")
                            print("")
                            continue

                    if taken == "YES":
                        taken = "Y"
                    elif taken == "NO":
                        taken = "N"


                    if taken == "Y":
                        row["Doses"] -= 1

                else:
                    taken = "N"


                log_list.append({"Date": today, "Med": row["Med"], "Dose": n, "Taken": taken})

                n += 1

            if row["Doses"] > 5:
                print(f"You have {row['Doses']} doses of {row['Med']} left")

            elif 1 < row["Doses"] <= 5:
                print(f"STOCK ALERT: You have ONLY {row['Doses']} doses of {row['Med']} left")

            elif row["Doses"] == 1:
                print(f"STOCK ALERT: You have ONLY 1 dose of {row['Med']} left")
            

            elif row["Doses"] == 0:
                print(f"STOCK ALERT: You have NO doses of {row['Med']} left. Update more (via option 1) to log")


        with open(f"{self.name}_log.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames = ["Date", "Med", "Dose", "Taken"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(log_list)

        print("")



    def history(self):
        log_list = []
        adherence_list = []
        with open(f"{self.name}_log.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                log_list.append(row)

        print(tabulate(log_list, headers = "keys", tablefmt = "heavy_grid"))
        print("")

        for line in self.med:
            a = 0
            b = 0
            n = line["Med"]
            for log in log_list:
                if log["Med"] == n:
                    if log["Taken"] == "Y":
                        a += 1
                    b += 1
            try:
                adherence = str(round((a/b) * 100, 2)) + "%"

            except ZeroDivisionError:
                adherence = f"{n} not logged"

            adherence_list.append({"Med": n, "Adherence": adherence})


        print(tabulate(adherence_list, headers = "keys", tablefmt = "heavy_grid"))
        print("")



def main():
    print("")
    print("Welcome To MedAid, an ADHERENCE TOOL for... well meds(duh)")
    print("")

    patient = Patient.get_patient()
    if not os.path.exists(f"{patient.name}.csv"):
        patient.patient_csv()
    while True:
        print("**************************************************************")
        print("Choose the NUMBER corresponding the option u would like to use")
        print("")
        print("""1. Add/Refill/Remove Medication
2. Log Medicine Intake
3. View Patient Med Intake History
4. Get Cheaper Generic Alternatives
5. Exit""")
        print("**************************************************************")
        print("")

        option = input("Option: ")

        if option == "1":
            patient_med_func(patient)

        elif option == "2":
            if os.path.exists(f"{patient.name}_med.csv"):
                med = Med.load(patient)
                med.log()
                med.med_csv()
            else:
                print("")
                print("No Meds Found On File To Log. Kindly add meds (via OPTION 1) first in order to log them")
                print("")

        elif option == "3":
            if os.path.exists(f"{patient.name}_log.csv"):
                med = Med.load(patient)
                med.history()

            else:
                print("")
                print("Kindly log your med intake (via OPTION 2) first in order to get med intake history")
                print("")

        elif option == "4":
            generic()



        elif option == "5":
            print("")
            sys.exit("""Thanks for using MedAid Bye Cutieeeeeee
            """)



def patient_med_func(patient):
    print("")
    print("**************************************************************")
    print("Choose the NUMBER corresponding the option u would like to use")
    print("")
    print("""1. Add New Med
2. Refill Med
3. Remove Med""")
    print("***************************************************************")
    print("")
    option = input("Option: ")

    filename = f"{patient.name}_med.csv"
    file_exists = os.path.exists(filename)

    if option == "1":

        if not file_exists:
            print("")
            med = Med.get_meds(patient)
            med.med_csv()

        elif file_exists:
            med = Med.load(patient)
            med.add()
            med.med_csv()

    elif option == "2":
        if file_exists:
            med = Med.load(patient)
            med.refill()
            med.med_csv()

        else:
            print("")
            print("No Meds Found On File To Refill. Kindly Add Meds (via option 1) to proceed")
            print("")

    elif option == "3":
        if file_exists:
                med = Med.load(patient)
                med.remove()
                med.med_csv()

        else:
            print("")
            print("No Meds Found On File To Remove. Kindly Add Meds (via option 1) to proceed")
            print("")


def generic():
    print("")
    while True:
        try:
            active = input("Enter the ACTIVE INGREDIENT of the med you would like to see cheaper generic alternatives for: ").title()
            if not active:
                raise ValueError
            print("")
            break
        except ValueError:
            print("No Active Ingredient Inputted")
            print("")
            continue

    while True:
        try:
            strength = int(input("Strength of med (in mg, in case of vitamins, type 0 IF strength not specified on med): "))
            print("")
            break

        except ValueError:
            print("Invalid Strength Inputted")
            print("")
            continue

    while True:
        try:
            price = float(input("How much did u buy the meds for?(per dose in inr): "))
            if not 0 < price:
                raise ValueError
            print("")
            break
        except ValueError:
            print("Price must be a non zero number")
            print("")
    n = 0
    with open("generic_med.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Active_In"] == f"{active} {strength} mg":
                n += 1
                if float(row["Cost"]) < price:
                    per = round(((price-float(row["Cost"]))/price) * 100, 2)
                    
                    print(f"A generic med is available at a {per}% LESS cost at Rs. {float(row['Cost'])}")


                if float(row["Cost"]) == price:

                    print("Meds u have bought are the SAME COST as those in our database.")


                if float(row["Cost"]) > price:

                    print("Meds u have bought are EVEN CHEAPER than those in our database. You should be recommending us meds lmao :)")


        if n == 0:
            print("Active ingredient you entered not currently in our database. New data will be added to this file, kindly stay tuned :))")

        print("")


def validate_name(name):
    if not name:
        raise ValueError
    return name

def validate_bday(bday):
    if not re.search(r"^(19[1-9][0-9]|20[0-1][0-9]|202[0-6])(-|/)(1[0-2]|0[0-9])(-|/)(3[0-1]|[1-2][0-9]|0[1-9])$", bday):
        raise ValueError
    return bday

def validate_gender(gender):
    if not gender in ["M", "F", "MALE", "FEMALE"]:
        raise ValueError
    return gender


if __name__ == "__main__":
    main()
