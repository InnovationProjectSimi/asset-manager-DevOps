# function to sanitise inputs from forms
def sanitise_input(input):
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
