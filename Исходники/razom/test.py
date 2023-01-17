import hashlib

s = str("123jkfnsgjkdfjhb3h12b3hj12b3j12b3hj12b3123jkfnsgjkdfjhb3h12b3hj12b3j12b3hj12b3123jkfnsgjkdfjhb3h12b3hj12b3j12b3hj12b3123jkfnsgjkdfjhb3h12b3hj12b3j12b3hj12b3123jkfnsgjkdfjhb3h12b3hj12b3j12b3hj12b3")
pwd = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

print(pwd)
