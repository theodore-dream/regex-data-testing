from faker import Faker

fake = Faker()

# Generate fake credit card numbers
credit_card_numbers = [fake.credit_card_number() for _ in range(50)]

# Generate fake social security numbers
ssns = [fake.ssn() for _ in range(50)]

# Save fake credit card numbers to a file
with open("fake_credit_card_numbers.txt", "w") as f:
    for number in credit_card_numbers:
        f.write(number + "\n")

# Save fake social security numbers to a file
with open("fake_social_security_numbers.txt", "w") as f:
    for ssn in ssns:
        f.write(ssn + "\n")
