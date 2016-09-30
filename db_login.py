import pdb
import logging
from flask import Flask, session, redirect, url_for, escape, request, flash, render_template, g, redirect
# TODO: mv to datastore
names = {"admin": "123",
		  "guest": ""}

def log_the_user_in(user_name):
	session['username'] = user_name
	flash('You were successfully logged in')
	return redirect(url_for('dashboard'))


def valid_login(user_name, user_pass):
	#pdb.set_trace()
	if user_name in names and names[user_name] == user_pass:
		logging.info("Login credential Accepted")
		return True
	logging.info("False Attempt!")
	return False