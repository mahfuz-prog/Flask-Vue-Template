import json
import pytest
import time

# test config
with open('../config.json', 'r') as config_file:
    conf = json.load(config_file)

AUTH_PREFIX = conf.get('AUTH_PREFIX')
test_email = "webwaymark@gmail.com"
test_pass = "Asdf1111"

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
    # without proper payload
    payload = {
        "name_": "testuser",
        "email_": "testuser@example.com",
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name and email are required."

    # ===================================
    # with proper payload
    payload = {
        "name": "test user",
        "email": test_email,
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    if response.status_code == 409:
        if response.json().get("nameStatus"):
            assert response.json().get("nameStatus") == "Username already taken."
        if response.json().get("emailStatus"):
            assert response.json().get("emailStatus") == "Email already taken."

    if response.status_code == 200:
        assert response.json().get("message") == "OTP sent to email."


# verify endpoint
def test_verify(api_client):
    # already loggedin user can't access verify
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # =========================================
    # without proper payload
    payload = {
        "name": "test user",
        "email": test_email,
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid credentials!"

    # =========================================
    # successful verification
    otp = input('Enter otp or ENTER to pass: ')
    payload = {
        "name": "test user",
        "email": test_email,
        'password': test_pass,
        'otp': otp
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    if response.status_code == 400:
        assert response.json().get("error") == "Invalid credentials!"

    if response.status_code == 200:
        assert response.json().get("message") == "Signup successful."

    # =========================================
    # wait 2m for clear redis cache
    # to test this delete database file and remove comment
    # time.sleep(120)
    # response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    # assert response.json().get("error") == "Timeout or invalid OTP."

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
    assert response.status_code == 401, "Expected status code 401"
    assert response.json().get("error") == "Invalid credentials!"

    # ===================================
    # invalid information
    payload = {
        "email": "_ebwaymark@gmail.com",
        'password': 'asdf',
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 401, "Expected status code 401"
    assert response.json().get("error") == "Invalid credentials!"

    # ================================
    # login credentials
    payload = {
        "email": test_email,
        'password': test_pass,
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 200, "Expected status code 200"


# test reset password route
def test_reset_password(api_client):
    # invalid credentials
    payload = {"email": "webwaymark@gmail.comm"}
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Please check your email address."

    # ==============================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid credentials!"

    # ===============================================
    # valid credentials
    payload = {"email": test_email}
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "OTP sent to email."


# test reset otp verify
def test_verify_reset_otp(api_client):
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid credentials!"

    # ====================================================
    # invalid otp
    payload = {"email": test_email, "otp": 111111}
    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # ===========================================================
    # valid request
    otp = input('Enter otp: ')
    payload = {"email": test_email, "otp": otp}
    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "Otp matched."


# test set new password
def test_new_pass(api_client):
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/new-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid credentials!"
    # =========================================================
    # invalid credentials
    payload = {
    "email": test_email,
    "otp": 111111,
    "pass": test_pass
    }
    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Something went wrong!"

    # ===========================================================
    # change password
    otp = input('Enter otp: ')
    payload = {
    "email": test_email,
    "otp": otp,
    "pass": test_pass
    }
    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "Password changed."


# account endpoint
def test_account(api_client):
    # get the jwt
    payload = {
        "email": test_email,
        'password': test_pass,
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    token = response.json().get('token')

    # =========================================
    # without authorization header
    response = api_client.get(f"{api_client.base_url}/users/account/")
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # wrong secret
    headers = {
        "Authorization": f"unknown {token}"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # without prefix secret
    headers = {
        "Authorization": token
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # success request
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {token}"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 200, "Expected status code 200"

    # =========================================
    # invalid jwt
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisainvalidtoken"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"