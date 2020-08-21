# import generate_password_hash and check_password_hash here:
from werkzeug.security import generate_password_hash,check_password_hash

hardcoded_password_string = "SomU052011@@"

# generate a hash of hardcoded_password_string here:
hashed_password = generate_password_hash(hardcoded_password_string)
print(hashed_password)

password_attempt_one = "abcdefghij_123456789"

# check password_attempt_one against hashed_password here:
hash_match_one = check_password_hash(hashed_password, password_attempt_one)
print(hash_match_one)

password_attempt_two = "SomU052011@@"

# check password_attempt_two against hashed_password here:
hash_match_two = check_password_hash(hashed_password, password_attempt_two)
print(hash_match_two)