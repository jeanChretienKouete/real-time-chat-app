from wtforms import EmailField, Form, PasswordField, validators


class LoginForm(Form):
    email = EmailField("Email Address", [validators.Length(min=6, max=35)])
    password = PasswordField("Password", [validators.DataRequired()])
