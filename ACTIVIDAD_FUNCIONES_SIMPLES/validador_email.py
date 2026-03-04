def validar_email(email):
    if '@' in email and '.' in email:
        return True
    else:
        return False
if __name__ == "__main__":
    print(validar_email("test@test.com"))   # True
    print(validar_email("testtest.com"))    # False
    print(validar_email("test@testcom"))    # False
    print(validar_email("testtestcom"))    # False
