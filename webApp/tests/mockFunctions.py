"""
Mock functions file is created to hold replicas of the functions used in the asset manager.
The results of the functions have been minorly altered to allow asset test cases to ensure functionality.
"""


# Mock signup fucntion to validate users input
def mock_signUp(request):
    # Check if the request is a post - A submitted form
    if request.get("method") == "POST":
        formData = request.get("form")
        username = mock_sanitise_input(formData.get("username").lower())
        password = mock_sanitise_input(formData.get("password"))
        confPassword = mock_sanitise_input(formData.get("confPassword"))

        if len(username) < 4:
            # If the username is too short then notify the user
            return "Username length"
        elif password != confPassword:
            return "Password match"
        elif len(password) < 7:
            return "Password length"
        elif not any(char in ["!", "@", "#", "$", "£"] for char in password):
            # If the password does not contain symbols then notify the user
            return "Password symbol"
        elif not any(char.isdigit() for char in password):
            return "Password digit"
        elif not any(char.isupper() for char in password):
            return "Password case"
        else:
            # If the details are valid then create the users account and log them in
            return "Success"
        # endif
    # endif
    return "GET method"


# function to sanitise inputs from forms
def mock_sanitise_input(input):
    # Function made to replace characters input whihc could be used in injection attacks
    EMPTY = ""
    # Return the stripped sanitised input
    return (
        input.replace("'", EMPTY)
        .replace("--", EMPTY)
        .replace("%", "Percent")
        .replace(";", EMPTY)
        .replace("*", EMPTY)
    )
