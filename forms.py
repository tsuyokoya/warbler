from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField("text", validators=[InputRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing user profile"""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])
    image_url = StringField("(Optional) Image URL")
    header_image_url = StringField("(Optional) Header Image URL")
    bio = StringField("Bio", validators=[InputRequired()])
    password = PasswordField("Enter Current Password", validators=[Length(min=6)])
