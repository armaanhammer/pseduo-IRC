# from __future__ import division
# import time

class Room:
  def __init__(
    self,
    room_name,
    some_other_name,
    users,  # dict of socket objects?
    num_users = 0
  ):
    
    self.room_name = room_name
    self.users = {}
    self.num_users = 0
    
    def join(self, user_name):
      self.users.add(user_name)
      self.num_users = num_users+1
      if (len(users) != num_users):
        print('ERROR: num_users and len(users) inconsistent')
        print('num_users')
        print(num_users)
        print('len(users)')
        print(len(users))
      
    def publish(self, message):
      temp = num_users
      while(temp>0):
        users[num_users - temp].send
        temp = temp-1
        
    def leave(self, user_name):
      self.users.remove(user_name)
      self.num_users = num_users-1
      if (len(users) != num_users):
        print('ERROR: num_users and len(users) inconsistent')
        print('num_users')
        print(num_users)
        print('len(users)')
        print(len(users))
        
        
class WTF:
  def __init__(
      self,
      users,
      more_users,
      num_users,
      more_num_users
      ):
    self.users = {}
    self.num_users = 0
    
class MoreWTF:
  def __init__(
      self
  ):
    
    self.users,
    self.more_users = 0,
    self.test = {}
  