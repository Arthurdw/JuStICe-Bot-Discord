from discord import User


def member_replacements(sentence: str, member: User):
    return_value = sentence
    member_replacements_values = [
        ["member", str(member)], ["discriminator", str(member.discriminator)], ["id", str(member.id)],
        ["mention", member.mention], ["created", str(convert_time(member.created_at))], ["name", member.name]
    ]
    for value in member_replacements_values:
        return_value = return_value.replace('{' + value[0] + '}', value[1])
    return return_value.replace("\\n", "\n")


def convert_time(time):
    return time.strftime("%d/%m/%Y | %H:%M:%S")
