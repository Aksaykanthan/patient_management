from datetime import date

def calculate_age(dob):
  today = date.today()
  try:
    birth_date = date.fromisoformat(dob)
  except ValueError:
    return "Invalid date format. Please use YYYY-MM-DD."

  age = today.year - birth_date.year

  if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1  
  return age

