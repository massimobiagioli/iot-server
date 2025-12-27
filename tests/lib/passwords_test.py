from app.lib.passwords import hash_password, verify_password


def test_hash_password():
    password = "supersecret"

    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert len(hashed) == 64
    assert hashed == hash_password(password)
    assert hashed != hash_password("different")


def test_verify_password():
    password = "mypassword"

    hashed = hash_password(password)

    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)
