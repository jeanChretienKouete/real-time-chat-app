from wtforms import EmailField, Form, PasswordField, StringField, validators


class RegistrationForm(Form):
    fname = StringField("Username", [validators.Length(min=1, max=25)])
    lname = StringField("Username", [validators.Length(min=1, max=25)])
    email = EmailField("Email Address", [validators.Length(min=6, max=35)])
    password = PasswordField("Password", [validators.DataRequired()])
