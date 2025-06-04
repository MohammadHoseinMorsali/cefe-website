from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields import EmailField # Correct import for EmailField
from wtforms.validators import DataRequired, Length, Optional, Email

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = StringField('Price (e.g., $3.50 or 3.50)', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Save Menu Item')

class CafeInfoForm(FlaskForm):
    about_us_text = TextAreaField('About Us Text', validators=[Optional(), Length(max=2000)])
    contact_address = StringField('Contact Address', validators=[Optional(), Length(max=250)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=50)])
    contact_email = EmailField('Contact Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Update Cafe Information')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=20)])
    submit = SubmitField('Publish Post')
