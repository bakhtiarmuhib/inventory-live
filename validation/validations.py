import re
 


 
def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(re.fullmatch(regex, email)):
        return email
 
    else:
        raise Exception("Invalid Email")

def password_validator(value):
    alphabet_count, special_charecter_count, digit_count = 0, 0, 0
    specialchar="""~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/"""
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    digits="0123456789"

    if len(value) >= 8 and len(value) <= 32:
        for i in value:
            if (i in smallalphabets) or (i in capitalalphabets) :
                        alphabet_count+=1           

            if (i in digits):
                digit_count = digit_count + 1       
            

            if(i in specialchar):  
                special_charecter_count = special_charecter_count+1

                    
        if (alphabet_count <= 0 ):
            raise Exception('Password must contain atleast 1 charecter')
            
        elif(digit_count <= 0):
            raise Exception('Password must contain atleast 1 digit')
            
        elif(special_charecter_count <= 0):
            raise Exception('Password must contain atleast 1 special character')
            
        elif(alphabet_count >=1 and digit_count>=1 and special_charecter_count >=1):
            return value
        else:
            raise Exception('Try Another password')
    raise Exception('password must be 8 to 32 characters long')


def phone_number_validator(value):
    digits="0123456789"
    if len(value) == 11:
        for i in value:
            if i not in digits:
                raise Exception('Invalid phone number.')
        return value
    else:
        raise Exception('Invalid phone number.')