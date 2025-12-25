from pathlib import Path
from datetime import date
import json
import random
import string

class Student:
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("sorry we are facing some issue")

    except Exception as err:
        print("an error occured" , err)

    @classmethod
    def __update(cls):
        with open(cls.database , "w") as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __scholarno():
        digits = random.choices(string.digits , k = 5)
        random.shuffle(digits)
        return "".join(digits)

    def create_profile(self):
        d = {
            'name':input("enter the name"),
            'grade':input("enter the grade"),
            'email':input("enter your email"),
            'scholarno':Student.__scholarno(),
            'password':input("enter your password"),
            'phoneno':input("enter your phone number")
        }                            

        print("please note down your scholar number" , d["scholarno"])
        if len(str(d['phoneno'])) != 10:
            print("please review your phone number")
        elif len(str(d['password'])) != 6:
            print("please review your password")
        else:
            Student.data.append(d)
            Student.__update()
            print("profile created")   

    def update_profile(self):
        name = input("enter your name")
        scholarno = input("enter the scholar number")
        grade = input("enter your grade")
        user_data = [i for i in Student.data if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade] 
        if not user_data:
            print("user not found")
        else:
            print("you cannot change name,scholarno,grade")
            print("press enter to skip")
            #email,password,phoneno
            new_data = {
                'email':input("enter your new email"),
                'password':input("enter your new password"),
                'phoneno':input("enter your new phone number")
            }          

            new_data["name"] = user_data[0]["name"]
            new_data["scholarno"] = user_data[0]["scholarno"]
            new_data["grade"] = user_data[0]["grade"]

            for i in new_data:
                if new_data[i] == "":
                    new_data[i] = user_data[0][i]   
            print(new_data)

            for i in user_data[0]:
                if user_data[0][i] == new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i] = int(new_data[i])

                    else:
                        user_data[0][i] = new_data[i]
            print(user_data)
            Student.__update()
            print("details update!")

    def report_card(self):
        name = input("enter your name")
        scholarno = input("enter your scholar number")
        grade = input("enter your grade")
        user_data = [i for i in Student.data if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade]
        if not user_data:
            print("user not found")
        else:
            print("enter your marks(out of 100)")
            maths = int(input("enter your maths marks:"))
            science = int(input("enter your science marks"))
            english =int(input("enter your english marks:"))
            hindi = int(input("enter your hindi marks:"))
            computer = int(input("enter your computer marks:"))

            total = maths + science + english + hindi + computer
            percentage = total / 5

            if percentage >= 90:
                print("A+")
            elif percentage >= 80:
                print("B+")
            elif percentage >= 70:
                print("C+")
            elif percentage >= 60:
                print("D+")
            else:
                print("Fail")

            student = user_data[0]
            #report card data    
            print("REPORT CARD")
            print("name" , student["name"])
            print("scholarno:" , student["scholarno"])
            print("grade" , student["grade"])
            print("total marks:" , total)
            print("percentage" , percentage)

            #save the data
            student["report_card"] = {
                "maths:":maths,
                "science:":science,
                "english:":english,
                "hindi:":hindi,
                "computer:":computer,
                "total":total,
                "percentage":percentage,
            }

            Student.__update()
            print("report_card done")

    def delete_profile(self):   
        name = input("enter your name")
        scholarno = input("enter your scholar number")
        grade = input("enter your grade")
        user_data = [i for i in Student.data if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade]
        if not user_data:
            print("user not found")
        else:
            for i in Student.data:
                if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade:
                    Student.data.remove(i)
            Student.__update()
            print("data deleted")


    def attendance_mark(self):
        name = input("enter your name")
        scholarno = input("enter your scholar number")
        user_data = None
        for i in Student.data:
            if i["name"] == name and i["scholarno"] == scholarno:
                user_data = i
                break

        if not user_data:
            print("student not found")
        else:
            # if attendance do not exit create it as an empty list
            if "attendance" not in user_data:
                user_data["attendance"] = []

            today = str(date.today())
            
            if today not in user_data["attendance"]:
                print("attendance marked for today" , today)
            else:
                user_data["attendnace"].append(today)
                Student.__update()
                print("attendnace marked for today of" , name , "on" , today)


print("Student data")
user = Student()
print("press1 for creating a profile")
print("press2 updating the profile")
print('press3 for report card')
print("press4 for deleting the student profile")
print("press5 for marking the attendance of a student")
check = int(input("enter the number of choice you want to perform"))

if check == 1:
    user.create_profile()

if check == 2:
    user.update_profile()

if check == 3:
    user.report_card()

if check == 4:
    user.delete_profile()

if check == 5:
    user.attendance_mark()
