from faker import Faker

def extract_userList():
    fake = Faker('ko-KR')

    test_user_data = [(fake.name(), fake.address(), fake.phone_number(),
                        fake.email(), fake.pyint(min_value=0,max_value=19))
                          for i in range(50)]
    
    return test_user_data