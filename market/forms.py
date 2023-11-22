from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User 


class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user= User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try again with different username')

    def validate_email(seld,email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists! please try a different email address')



    username = StringField(label='Username :', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email :', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password :', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password :', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='Username :', validators=[DataRequired()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class ItemAdd(FlaskForm):
    title = StringField(label="title :",validators=[Length(min=2, max=50),DataRequired()])
    price = IntegerField(label="Cost :",validators=[DataRequired()])
    description = StringField(label="Description",validators=[Length(min=25, max=1024),DataRequired()])
    image = FileField(label='Images', validators=[FileAllowed(['jpg','png'], 'Images Only!')])
    submit = SubmitField(label="Add Product")
