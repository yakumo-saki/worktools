def is_blank(string:str) -> bool:
    if string == None:
        return False
    if string == '':
        return False
    return True

def format_second_pomo(left_second: int) -> str:
    minute = int(left_second / 60)
    second = left_second % 60
    return f"{minute:02}:{second:02}"