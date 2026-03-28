
# Translates BlazBlue notation into something more familiar.
def translatecommands(rawinputs):

    translation = ""
    inputs = str(rawinputs).lower()
    inputs = inputs.replace("j.", "^")
    inputs = inputs.replace("66", "u")
    inputs = inputs.replace("44", "u")
    inputs = inputs.replace("hold", "h")
    # Okay, for simplicity's sake, I'll be converting all the moves to single digits or chars. here would be the translation of the custom ones:
    # ^ for jump
    # u for dash forward
    # i for dash backward
    # h for hold
    for x in inputs:
        command_dict = {"1":"↙️","2":"⬇️","3":"↘️","4":"⬅️","5":"✳️","6":"➡️","7":"↖️","8":"⬆️","9":"↗️", "u":"⏩", "i": "⏪",
                        "a":" **A** ", "b":" **B** ", "c":" **C** ", "d":" **D** ", "h":"  **HOLD**  ","^":"  **Jump**  ", ">":" > ", " ":" > "}
    
        if x.lower() in command_dict.keys() or x in command_dict.keys():
            translation = translation + command_dict[x.lower()]

        else:
            return "**Invalid string.**"

    return translation




# Checks if the messages has any slurs.
def slurchecker(text, author):
    amount = 0
    blackslurs = ("nigga", "nigger", "uncle tom", "niggas", "niggers", "negro", "negros", "negroes")
    yellowslurs = ("ching chong", "chink", "intsek", "zipperhead", "chinks", "zipperheads")
    gayslurs = ("fag", "faggot", "tranny", "dyke", "fags", "faggots", "dykes")
    disabledslurs = ("retarded", "retard",  "retards")
    robotslurs = ("clanker", "clankers", "clanka", "clankas")
    responses = [f"Multiple slurs was detected from {author}'s message.",
                 f"A racial slur targetted towards black people was said by {author}.",
                 f"A racial slur targetted towards asian people was said by {author}.",
                 f"A slur targetted towards LGBTQ+ people was said by {author}.",
                 f"A slur targetted towards people with disabilities was said by {author}.",
                 f"A slur targetted towards my people was said by {author}.",
                 f""
                ]
            
    is_slur = False
    prev_type = 6
    mixed_slurs = False
    text = text.split()
    for x in text:
        slur_type = 6
        if x in blackslurs:
            slur_type = 1
        elif x in yellowslurs:
            slur_type = 2
        elif x in gayslurs:
            slur_type = 3
        elif x in disabledslurs:
            slur_type = 4
        elif x in robotslurs:
            slur_type = 5
        
        if slur_type != 6:
            is_slur = True
            amount = amount + 1

        if prev_type != slur_type:
           mixed_slurs = True

        prev_type = slur_type
    if mixed_slurs:
        slur_type = 0
    return [is_slur, responses[slur_type], amount]

