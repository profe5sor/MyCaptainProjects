import csv

def wic(info_list):
    with open('s_info.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['Name','Age','Contact No.','Email ID'])
        writer.writerow(info_list)
if __name__ == '__main__':
    condition = True
    s_num = 1

    while condition:
        s_info = input('Enter Student Info in format(First_Name Age Contact_No Email_id):')

        student_info_list = s_info.split(' ')


        print(f'Entered information is \nFirst Name: {student_info_list[0]}\nAge: {student_info_list[1]}\n' +
        f'Contact No.: {student_info_list[2]}\nEmail_id: {student_info_list[3]}')

        info_check = input('Enter (y/n) if the information is correct:')

        if info_check == 'y':
            wic(student_info_list)
            condition_check = input('Enter ( y/n ) to input new student info:')

            if condition_check == 'y':
                condition = True
                s_num += 1
            elif condition_check == 'n':
                condition = False
        elif info_check == 'n':
            print('Please  enter the information again')
