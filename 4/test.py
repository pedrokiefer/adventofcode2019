from main import is_valid_password

def test_passwd_1():
    assert is_valid_password(122345) == True


def test_passwd_2():
    assert is_valid_password(111123) == True


def test_passwd_3():
    assert is_valid_password(135679) == False


def test_passwd_4():
    assert is_valid_password(111111) == True


def test_passwd_5():
    assert is_valid_password(223450) == False


def test_passwd_6():
    assert is_valid_password(123789) == False


def test_passwd_7():
    assert is_valid_password(112233) == True


def test_passwd_8():
    assert is_valid_password(123444) == False


def test_passwd_9():
    assert is_valid_password(111122) == True
