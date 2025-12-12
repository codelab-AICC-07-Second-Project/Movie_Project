from datetime import datetime, date
from utils.movie_constants import OCCUPATION_NAMES

def map_gender_to_numerical(gender): # 'F' = 0, 'M' = 1
    if gender.upper() == 'M': return 1
    elif gender.upper() == 'F': return 0
    else: pass

def calculate_age_code(birth): # 생년월일 바탕으로 나이 코드로 변환
    try:
        birthdate = datetime.strptime(birth, '%Y-%m-%d')
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18: return 1
        elif age < 25: return 18
        elif age < 35: return 25
        elif age < 45: return 35
        elif age < 50 : return 45
        elif age < 56 : return 50
        else: return 56
    except:
        return 25 # 기본값 지정

def map_occupation_id_to_name(occupation_id):
    try:
        if 0 <= occupation_id < len(OCCUPATION_NAMES):
            return OCCUPATION_NAMES[occupation_id]
        return None
    except TypeError:
        return None