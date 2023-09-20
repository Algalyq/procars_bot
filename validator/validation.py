

def validation_phone_number(phone_number):
    if phone_number.startswith(("+7708","+8708", "8708","+7705","+7747","+7701","8701","8747")) and len(phone_number) == 12 or len(phone_number) == 11:
        return True
    else:
        return False