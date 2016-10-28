from __future__ import unicode_literals

from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

class UserManager(models.Manager):
    def login(self, email, password):
        if len(email) < 0 or not EMAIL_REGEX.match(email):
            return {'error': 'Email Invalid'}
        try:
            user = User.objects.get(email=email)
        except:
            return {'error': 'Email not found'}
        pword = user.password.encode('utf-8')
        password = password.encode('utf-8')
        if not bcrypt.hashpw(password, pword) == pword:
            return {'error': 'Password does not match'}
        return {'success': user}
    def register(self, postdata):
        try:
            User.objects.get(email=email)
            return {'error': 'Email already exists'}
        except:
            pass
        fname = postdata['fname']
        if len(fname) < 2 or not fname.isalpha:
            return {'error': 'First Name must be letters and longer than 2'}
        lname = postdata['lname']
        if len(lname) < 2 or not lname.isalpha:
            return {'error': 'Last Name must be letters and longer than 2'}
        email = postdata['email']
        if len(email) < 0 or not EMAIL_REGEX.match(email):
            return {'error': 'Email Invalid'}
        pword = postdata['password']
        if len(pword) < 8:
            return {'error': 'Password Invalid'}
        pword2 = postdata['confirm']
        if pword != pword2:
            return {'error': 'Passwords don\'t match'}
        pword = pword.encode('utf-8')
        hashpw = bcrypt.hashpw(pword, bcrypt.gensalt())
        User.objects.create(first_name=fname, last_name=lname, email=email, password=hashpw)
        return {'user':User.objects.get(email=email)}



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
