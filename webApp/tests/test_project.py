from webApp.models import User
from werkzeug.security import generate_password_hash
from mockFunctions import mock_signUp, mock_sanitise_input


# Test password hashing is in place
def test_password_hashing():
    # Test to ensure the password input is not the same as the database by checking password is hashed with function
    new_user = User(
        username="testuser2",
        password=generate_password_hash("Pizza567!", method="sha256"),
    )

    assert new_user.password != "Pizza567!"
    assert generate_password_hash("Pizza567!", method="sha256") != "Pizza567!"


# Test to check inouts are sanitised
def test_sanitise():
    # Test -- to empty
    string = "Test string--"
    assert mock_sanitise_input(string) == "Test string"

    # Test ' to empty
    string = "'Test string'"
    assert mock_sanitise_input(string) == "Test string"

    # Test ; to empty
    string = "Test ;string;;;"
    assert mock_sanitise_input(string) == "Test string"

    # Test % to Percent
    string = "Test string 10%"
    assert mock_sanitise_input(string) == "Test string 10Percent"


# Test the signup validation
def test_signup():
    request = {
        "method": "GET",
        "form": {
            "username": "use",
            "password": "passWord1!",
            "confPassword": "passWord1!",
        },
    }

    # Test doesnt allow get method
    assert mock_signUp(request) == "GET method"

    # Alter request to check username length
    request["method"] = "POST"
    assert mock_signUp(request) == "Username length"

    # Alter request to check passwords match
    request["form"]["username"] = "user1"
    request["form"]["confPassword"] = "differentPass1!"
    assert mock_signUp(request) == "Password match"

    # Alter request to check password length
    request["form"]["password"] = "Pass1!"
    request["form"]["confPassword"] = "Pass1!"
    assert mock_signUp(request) == "Password length"

    # Alter request to check password contains symbol
    request["form"]["password"] = "Password123"
    request["form"]["confPassword"] = "Password123"
    assert mock_signUp(request) == "Password symbol"

    # Alter request to check password contains a digit
    request["form"]["password"] = "Password!!!"
    request["form"]["confPassword"] = "Password!!!"
    assert mock_signUp(request) == "Password digit"

    # Alter request to check password contains an uppercase letter
    request["form"]["password"] = "password1!!!"
    request["form"]["confPassword"] = "password1!!!"
    assert mock_signUp(request) == "Password case"

    # Alter request to check password success if all is correct
    request["form"]["password"] = "Password1!!!"
    request["form"]["confPassword"] = "Password1!!!"
    assert mock_signUp(request) == "Success"
