#!/usr/bin/python
from __future__ import absolute_import
from __future__ import print_function
import pprint
import sys

import duo_client
from six.moves import input

argv_iter = iter(sys.argv[1:])
def get_next_arg(prompt):
    try:
        return next(argv_iter)
    except StopIteration:
        return input(prompt)


def addPermission(user_id, group_id):
  admin_api.add_user_group(
    user_id=user_id,
    group_id=group_id
  )

# Configuration and information about objects to create.
admin_api = duo_client.Admin(
    ikey="", #'get_next_arg('Admin API integration key ("DI..."): '),'
    skey="", #'get_next_arg('integration secret key: '),'
    host="ㅌㅌㅌ.duosecurity.com", #'get_next_arg('API hostname ("api-....duosecurity.com"): '),# '
)

#test = groups.pop(1)
#print(test)
def create_user(user_email_address, user_phone_number, user_phone_platform, user_request_groups):
  EMAILADDR = get_next_arg('user email address: ')
  USERNAME = EMAILADDR.split("@")[0]
  REALNAME = USERNAME
  # Refer to http://www.duosecurity.com/docs/adminapi for more
  # information about phone types and platforms.
  PHONE_NUMBER = get_next_arg('phone number (e.g. +1-555-123-4567): ')
  PHONE_TYPE = "Mobile"  # get_next_arg('phone type (e.g. mobile): ')
  tPHONE_PLATFORM = get_next_arg('phone platform (e.g. google android): ')

  PHONE_PLATFORM = "iOS"
  if tPHONE_PLATFORM == "A":
    PHONE_PLATFORM = "Android"

  # Create and return a new user object.
  user = admin_api.add_user(
    username=USERNAME,
    realname=REALNAME,
    email=EMAILADDR,
  )
  print('Created user:')
  pprint.pprint(user)

  # Create and return a new phone object.
  phone = admin_api.add_phone(
    number=PHONE_NUMBER,
    type=PHONE_TYPE,
    platform=PHONE_PLATFORM,
  )
  print('Created phone:')
  pprint.pprint(phone)

  # Associate the user with the phone.
  admin_api.add_user_phone(
    user_id=user['user_id'],
    phone_id=phone['phone_id'],
  )
  print('Added phone', phone['number'], 'to user', user['username'])

  send_sms_activation(phone['phone_id'])
  set_group_permission(user['user_id'])


def send_sms_activation(phone_id, phone_number):
  # Send two SMS messages to the phone with information about installing
  # the app for PHONE_PLATFORM and activating it with this Duo account.
  act_sent = admin_api.send_sms_activation_to_phone(
    phone_id=phone_id,
    install='1',
  )
  print('SMS activation sent to', phone_number + ':')
  pprint.pprint(act_sent)

def set_group_permission(user_id):
  REQUEST_GROUPS_NAME = get_next_arg('request group name: ')
  request_group_name = REQUEST_GROUPS_NAME.split(",")

  groups = admin_api.get_groups()
  for j in request_group_name:
    for i in groups:
      if i['name'] == j:
        addPermission(user_id, i['group_id'])

def duoResetProcess(user_name, phone_platform=None):
  users = admin_api.get_users_by_name(user_name)
  #print(users)
  for i in users:
    if i['username'] == user_name:
      user_phones = i['phones']
      print(user_phones)
      for j in user_phones:
        if phone_platform is not None:
          change_phone_platform(j['phone_id'], phone_platform)
        send_sms_activation(j['phone_id'], j['number'])


def get_pending_deletion_user():
  users = admin_api.get_users()
  for user in users:
    #print (user)
    if(user['status'] != "active"):
      print(user['status'], user['username'], user['user_id'])
  return user['user_id']


'''
after user phone platform changed, need to activation.
So this method always work with send_sms_actication 
'''
def change_phone_platform(phone_id, phone_platform):
  admin_api.update_phone(phone_id,
                         None,
                         None,
                         None,
                         None,
                         phone_platform,
                         )

if __name__ == '__main__':
  #createuser("","","","")
  #DuoResetProcess("")
  user_id = get_pending_deletion_user()
  #print(user_id)
