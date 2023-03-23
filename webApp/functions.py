def sanitise_input(input):
    EMPTY = ""
    return (
        input.replace("'", EMPTY)
        .replace("--", EMPTY)
        .replace("%", "Percent")
        .replace(";", EMPTY)
        .replace("*", EMPTY)
    )
