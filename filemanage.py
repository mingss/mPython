#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import policy
from email.parser import BytesParser
import os

class AccountCheck:
    def diff(self, list1, list2):
        return list(set(list1).symmetric_difference(set(list2)))

    # 전체 사용자 리스트
    def get_entire_users(self, data):
        roles = data.split("\n\n")[1:]
        users = []
        for i in range(0,len(roles)):
            role = roles[i].split("\n\t")
            tmpusers = (role[1:])
            for tusers in tmpusers:
                users.append(str(tusers).split(" =>")[0])
        return list(set(users))

    #신규입사자 퇴사자 구분
    def check_employee_status(self, current_users,pre_users):
        changed_users = self.diff(current_users, pre_users)
        if(len(changed_users) != 0):
            print (changed_users)

        new_employee = []
        terminate_employee = []
        for user in changed_users:
            if user in current_users:
                new_employee.append(user)
                # print "New employee: " + user
            elif user in pre_users:
                terminate_employee.append(user)
                # print "Terminate employee: " + user

        #print "New employee: " + str(new_employee)
        #print "Terminate employee: " + str(terminate_employee)

        return new_employee, terminate_employee

    def user_name_split(self, user_names):
        user_name = []
        for i in range(0, len(user_names)):
            user_name.append(str(user_names[i]).split(" =>")[0])
        return user_name

    def get_mail_content(self, file_name):
        # msg = email.message_from_file(open('sample.eml'))
        with open(file_name, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)
        text = msg.get_body(preferencelist=('plain')).get_content()
        fp.close()
        return text

    def get_file_content(self, file_name):
        f = open(file_name, 'r')
        data = f.read()
        f.close()
        return data

    def get_file_data(self, file_name):
        if str.lower(file_name[-3:])=='eml':
            data=self.get_mail_content(file_name)
        else:
            data=self.get_file_content(file_name)
        return data

    def create_report(self, file_name, content):
        f = open(file_name, 'w')
        f.write(content)
        f.close()

    def make_report(self, file_name, content):
        f = open(file_name, 'a')
        f.write(content)
        f.close()

    def check(self, title, file_name, pre_file_name):
        data = self.get_file_data(file_name)
        current_users = self.get_entire_users(data)
        current_roles = data.split("\n\n")

        predata = self.get_file_data(pre_file_name)
        pre_users = self.get_entire_users(predata)
        pre_roles = predata.split("\n\n")

        #신규입사자, 퇴사자 체크
        new_employee, terminate_employee = self.check_employee_status(current_users, pre_users)

        added_user = []
        erased_user = []
        permission_added_user = []
        permission_deleted_user = []

        for i in range(0, len(current_roles)):
            for j in range(0, len(pre_roles)):
                if not (current_roles[i] == pre_roles[j]):
                    role = self.user_name_split(current_roles[i].split("\n\t"))
                    prerole = self.user_name_split(pre_roles[j].split("\n\t"))
                    if (role[0] == prerole[0]):
                        #changed_users = diff(role, prerole)
                        #print(changed_users)
                        for changed_user in self.diff(role, prerole):
                            if changed_user in new_employee and changed_user in role:
                                #print "For " + role[0] + " added: " + str(user)
                                added_user.append(str(changed_user))
                            elif changed_user in terminate_employee and changed_user in prerole:
                                #print "For " + role[0] + " erased: " + str(user)
                                erased_user.append(str(changed_user))
                            elif changed_user not in new_employee and changed_user in role:
                                permission_added_user.append((role[0],str(changed_user)))
                                #print role[0] + "permission Added: " + str(user)
                            elif changed_user not in terminate_employee and changed_user in prerole:
                                permission_deleted_user.append((role[0], str(changed_user)))
                                #print role[0] + "permission deleted: " + str(user)
                            else:
                                print ('ISSUES!!!!!' + str(changed_user))

       # print(changed_user)
        report_path = '/Users/minsu.kim/Documents/_MingCDN/Information Security Team/2019/Admin Permission Review/report/' + title + ".txt"

        #title
        self.create_report(
            report_path,
            title + "\n")

        report_new_employee = "[New Employee]\n  -Permission added" + str(list(set(added_user)))+"\n"
        report_terminate_employee = "[Terminate Employee]\n  -Permission deleted" + str(list(set(erased_user))) +"\n"
        report_modified_employee_title = "[Working Employee]\n"
        report_modified_employee_added = "  -Permission added" + str(permission_added_user)+"\n"
        report_modified_employee_deleted = "  -Permission deleted" + str(permission_deleted_user)+"\n"
        report_number_of_employee = str(len(self.get_entire_users(self.get_file_data(file_name))))

        if (len(added_user) != 0):
            print(report_new_employee)
            self.make_report(
                report_path,
                report_new_employee)
        if (len(erased_user) != 0):
            print(report_terminate_employee)
            self.make_report(
                report_path,
                report_terminate_employee)

        if(len(permission_added_user) != 0 or len(permission_deleted_user) != 0):
            print(report_modified_employee_title)
            self.make_report(
                report_path,
                report_modified_employee_title)
        if(len(permission_added_user) != 0):
            print(report_modified_employee_added)
            self.make_report(
                report_path,
                report_modified_employee_added)
        if (len(permission_deleted_user) != 0):
            print(report_modified_employee_deleted)
            self.make_report(
                report_path,
                report_modified_employee_deleted)

        self.make_report(
            report_path,
            report_number_of_employee
        )

if __name__ == '__main__':
    path = '/Users/minsu.kim/Documents/_MingCDN/Information Security Team/2019/Admin Permission Review/'
    listing = sorted(os.listdir(path))
    print(listing)

    for i in range(2, 52):
        first_filename = '%dw[NGP LDAP] Permission Summary.eml' % i
        second_filename = '%dw[NGP LDAP] Permission Summary.eml' % (i+1)
        #filename = "%dw.txt" % i

        print("%d week summary" % i)
        #print(first_filename, second_filename)
        ac = AccountCheck()
        try:
            ac.check(second_filename ,path + second_filename , path + first_filename)
        except FileNotFoundError:
            print ('No result')
            break
