# regex-data-testing
A repository to demonstrate with technical examples how to use regex to search for sensitive data. Specifically social security and credit card numbers

#### Workflow

 - First, I need to create fake or synthetic sensitive data 
 - Then I can use my awk script to then perform a regex search against the data to surface sensitive data

#### Generation of synthetic sensitive data 

In order to create this data, I am using the python utility `faker` which creates synthetic sensitive data. 

```
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
```

This script performs two main actions using the faker library. It generates a file with fake credit card numbers and another file with fake social security numbers. I have configure the file to create 50 numbers for each file. The outputs of this script are 2 files, `fake_credit_card_numbers.txt` and `fake_social_security_numbers.txt`. 

Run the script to generate the files. Then you are ready with your synthetic data to run awk commands against that data to verify you can search data files using regex to identify sensitive credit card and social security data. 

#### Running awk to surface sensitive data 

We will review 2 examples, one for social security number data, and another for credit card data 

#### Scanning a file for social security numbers data

 - In this first awk example, I am scanning the file `fake_social_security_numbers.txt` to surface the social security numbers.

 - Explanation:
   This AWK script uses a regular expression pattern to search for text that matches the format of U.S. social security numbers (SSNs). The pattern `/(^| )[0-9]{3}-[0-9]{2}-[0-9]{4}($| )/` specifically looks for:
    - `(^| )`: Matches the start of a line or a space character, ensuring the SSN is not part of a larger string.
    - `[0-9]{3}`: Exactly three digits.
    - `-`: A hyphen following the first set of digits.
    - `[0-9]{2}`: Exactly two digits after the first hyphen.
    - `-`: Another hyphen following the second set of digits.
    - `[0-9]{4}`: Exactly four digits for the last part.
    - `($| )`: Matches the end of a line or a space character, ensuring the SSN does not run into any subsequent text.
    This script scans each line of `fake_social_security_numbers.txt`, looking for matches to this pattern and outputs lines containing valid SSN formats.
 
 - Demonstration:
 - Because this file has 50 entries, I am limiting the output to only show the top 5 entries. 

```
awk '/(^| )[0-9]{3}-[0-9]{2}-[0-9]{4}($| )/' fake_social_security_numbers.txt | head -n 5
684-78-8563
198-36-7231
688-50-8568
785-44-0026
077-38-8021
```

 - We can then use the `wc -l` utility to verify that the script captured all 50 instances of social security numbers

```
awk '/(^| )[0-9]{3}-[0-9]{2}-[0-9]{4}($| )/' fake_social_security_numbers.txt | wc -l
      50
```



#### Scanning a file for credit card data 

 - In this first awk example, I am scanning the file `fake_credit_card_numbers.txt` to surface the social security numbers.

### Credit Card Number Detection:
- Script:
    ```bash
    awk '/^[0-9]{13,19}$/' fake_credit_card_numbers.txt
    ```
- Explanation:
    This script targets lines that exclusively contain a sequence of 12 to 19 digits, accommodating the length variations in most credit card numbers. The regex pattern `^[0-9]{12,19}$` consists of:
    - `^`: Asserts the start of a line.
    - `[0-9]{12,19}`: Matches a sequence of digits with a minimum length of 12 and a maximum of 19, covering the range for most credit card standards.
    - `$`: Asserts the end of a line.

    This approach is ideal for processing unformatted or raw data streams where credit card numbers are not punctuated and are placed on separate lines. It's useful for scanning through large datasets where credit card numbers are extracted as part of data cleansing processes or when they are input without formatting.

 - Demonstration:
 - Because this file has 50 entries, I am limiting the output to only show the top 5 entries. 

```
awk '/^[0-9]{12,19}$/' fake_credit_card_numbers.txt | head -n 5
30177397308289
4915671064159035
2423758330230614
213139621393775
2226344772813552
```

 - We can then use the `wc -l` utility to verify that the script captured all 50 instances of credit card numbers

```
awk '/^[0-9]{12,19}$/' fake_credit_card_numbers.txt | wc -l
      50
```

#### Limitations

Social Security Number Detection:
- Data Format Dependency: The effectiveness of the social security number detection script relies heavily on the data format. It assumes SSNs are formatted with hyphens (e.g., XXX-XX-XXXX). If SSNs are presented without hyphens or in a different format, they will not be detected.
- False Positives and Negatives: The pattern used may occasionally yield false positives if sequences of numbers accidentally conform to the SSN pattern but are not actual SSNs. Similarly, SSNs that are embedded in longer strings of digits or text (without clear delimiters) may be missed.

Credit Card Number Detection:
- Continuous Digit Format Only: This approach is limited to detecting credit card numbers that appear as continuous strings of digits. It will not capture numbers that are formatted with spaces, hyphens, or other characters typically used in formatting credit card numbers for readability (e.g., 1234 5678 9101 1121 or 1234-5678-9101-1121).
- Lack of Specificity: The regex does not differentiate between different types of credit card numbers (such as VISA, MasterCard, American Express, etc.) and may not correctly handle the varying length specific to each card type. For instance, American Express numbers are typically 15 digits long, while most other major credit cards are 16 digits.
- False Positives: Because the pattern matches any sequence of 12 to 19 digits, it may falsely identify non-credit card numbers as credit cards if they fall within this digit range. This can include phone numbers, numerical codes, or other financial account numbers not intended to be credit card numbers.

These limitations suggest that while AWK scripts provide a useful tool for preliminary scans of sensitive data, they should ideally be complemented with additional validation steps or more sophisticated pattern recognition algorithms to ensure accuracy and completeness in data handling tasks.


