import json
import time

# test config
with open('../frontend_config.json', 'r') as config_file:
    conf = json.load(config_file)

AUTH_PREFIX = conf.get('AUTH_PREFIX')

user_1 = {
    "name": "test user 1",
    "test_email": "webwaymark@gmail.com",
    "test_pass": "Asdf1111",
    "token": "",
}

user_2 = {
    "name": "test user 2",
    "test_email": "mahfuzurrahman5676@gmail.com",
    "test_pass": "Asdf1111",
    "token": ""
}


# ====================================================================================
# ====================================================================================
# users blueprint
# ====================================================================================
# ====================================================================================

# sign-up endpoint
def test_sign_up(api_client):
    # already loggedin user can't access signup
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"
    assert response.json().get("error") == "Forbidden response!"

    # =========================================
    # without payload
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty name
    payload = { "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name cannot be empty."

    # =========================================
    # minimum name
    payload = { "name": "as", "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at least 3 characters."

    # =========================================
    # maximum name
    payload = { "name": "asd" * 20, "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at most 20 characters."
  
    # =========================================
    # empty email
    payload = { "name": user_1["name"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # invalid email format
    payload = { "name": user_1["name"], "email": "asdfddfd" }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # ===================================
    # create user 1
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    if response.status_code == 409:
        if response.json().get("nameStatus"):
            assert response.json().get("nameStatus") == "Username already taken."
        if response.json().get("emailStatus"):
            assert response.json().get("emailStatus") == "Email already taken."

    if response.status_code == 200:
        assert response.json().get("message") == "OTP sent to email."

    # ===================================
    # create user 2
    payload = {
        "name": user_2["name"],
        "email": user_2["test_email"],
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    if response.status_code == 409:
        if response.json().get("nameStatus"):
            assert response.json().get("nameStatus") == "Username already taken."
        if response.json().get("emailStatus"):
            assert response.json().get("emailStatus") == "Email already taken."

    if response.status_code == 200:
        assert response.json().get("message") == "OTP sent to email."

    print("=================== Sign up test passed ==================")


# verify endpoint
def test_verify(api_client):
    # already loggedin user can't access verify
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # =========================================
    # without payload
    response = api_client.post(f"{api_client.base_url}/users/verify/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."
    
    # =========================================
    # empty otp
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # =========================================
    # empty name
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name cannot be empty."

    # =========================================
    # minimum name
    payload = {
        "name": "as",
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at least 3 characters."

    # =========================================
    # maximum name
    payload = {
        "name": "as" * 20,
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at most 20 characters."

    # =========================================
    # empty email
    payload = {
        "name": "asadf",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "name": user_1["name"],
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "name": user_1["name"],
        "email": "asdfdd",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "123",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "123" * 20,
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password format
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "asdfasdf",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."

    # =========================================
    # successful verification user 1
    otp = input('Press enter if user_1 already created. else enter OTP: ')
    if otp:
        payload = {
            "name": user_1["name"],
            "email": user_1["test_email"],
            'password': user_1["test_pass"],
            'otp': otp
        }
        response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
        if response.status_code == 400:
            assert response.json().get("error") == "Timeout or invalid OTP."

        if response.status_code == 200:
            assert response.json().get("message") == "Signup successful."

    # =========================================
    # successful verification user 2
    otp = input('Press enter if user_2 already created. else enter OTP: ')
    if otp:
        payload = {
            "name": user_2["name"],
            "email": user_2["test_email"],
            'password': user_2["test_pass"],
            'otp': otp
        }
        response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
        if response.status_code == 400:
            assert response.json().get("error") == "Timeout or invalid OTP."

        if response.status_code == 200:
            assert response.json().get("message") == "Signup successful."

    # =========================================
    # wait 2m for clear redis cache
    # to test this delete database file and remove comment
    print("sleeping for 80 second for clear redis cache...")
    time.sleep(80)

    # random otp for only test redis cache clear
    payload = {
        "name": user_2["name"],
        "email": user_2["test_email"],
        'password': user_2["test_pass"],
        'otp': "123456"
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    print("=================== Verify test passed ==================")


# login endpoint
def test_log_in(api_client):
    # already loggedin user can't access login
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # ==================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = {
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "email": "asdfdd",
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "email": user_1["test_email"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "email": user_1["test_email"],
        "password": "123",
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "email": user_1["test_email"],
        "password": "123" * 20,
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password
    payload = {
        "email": user_1["test_email"],
        "password": "asdfdfddf",
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."

    # ================================
    # login credentials user 1
    payload = {
        "email": user_1["test_email"],
        'password': user_1["test_pass"],
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    token = response.json().get('token')
    user_1["token"] = token

    # ================================
    # login credentials user 2
    payload = {
        "email": user_2["test_email"],
        'password': user_2["test_pass"],
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    token = response.json().get('token')
    user_2["token"] = token

    print("=================== Login test passed ==================")


# test reset password route
def test_reset_password(api_client):
    # ================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = { "password": user_1["test_pass"] }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = { "email": "asdf" * 200 + "@b.d" }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = { "email": "asdfdd" }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # ===============================================
    # valid credentials
    payload = {"email": user_1["test_email"]}
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "OTP sent to email."

    print("=================== Reset password test passed ==================")


# test reset otp verify
def test_verify_reset_otp(api_client):
    # ====================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = {"otp": 111111}

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = { "email": "asdf" * 200 + "@b.d", "otp": 111111 }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = { "email": "asdfdd", "otp": 111111 }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."


    # =========================================
    # empty otp
    payload = { "email": user_1["test_email"] }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "email": user_1["test_email"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # ===========================================================
    # valid request
    otp = input('Enter otp user_1 to test verify_reset_otp. else enter to pass user_1: ')
    if otp:
        payload = {"email": user_1["test_email"], "otp": otp}
        response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
        assert response.status_code == 200, "Expected status code 200"
        assert response.json().get("message") == "Otp matched."

    print("=================== Verify reset otp test passed ==================")


# test set new password
def test_new_pass(api_client):
    # =========================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/new-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty otp
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123446"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # =========================================
    # empty email
    payload = {
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "email": "asdfdd",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "email": user_1["test_email"],
        "password": "123",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "email": user_1["test_email"],
        "password": "123" * 20,
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password format
    payload = {
        "email": user_1["test_email"],
        "password": "asdfasdf",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."


    # ===========================================================
    # change password
    otp = input('Enter same otp to change password. else enter to pass user_1: ')
    if otp:
        payload = {
            "email": user_1["test_email"],
            "otp": otp,
            "password": user_1["test_pass"]
        }
        response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
        assert response.status_code == 200, "Expected status code 200"
        assert response.json().get("message") == "Password changed."
    
    print("=================== New password test passed ==================")


# account endpoint
def test_account(api_client):
    # =========================================
    # without authorization header
    response = api_client.get(f"{api_client.base_url}/users/account/")
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # wrong secret
    headers = {
        "Authorization": f"unknown asdf"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # without prefix secret
    headers = {
        "Authorization": user_1["token"]
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # invalid jwt
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisainvalidtoken"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # success request
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 200, "Expected status code 200"

    # update user_1 name
    user_1['name'] = response.json().get("name")


    print("=================== Account test passed ==================")