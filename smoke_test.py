import time

import requests

url = "http://localhost:8000"
auth = ("daniel", "password123")

r = requests.get(f"{url}/books/search", params={"q": "frankenstein"})
assert r.status_code == 200, r.text
print("search:", r.status_code, r.json()["count"])

## important note I found sometimes the gutendex endpoint fails with id
r = requests.get(f"{url}/books/84")
assert r.status_code == 200, r.text
print("get book:", r.status_code, r.json()["title"])

r = requests.get(f"{url}/book/84", allow_redirects=False)
assert r.status_code == 307, r.text
print("redirect ok", r.status_code)

r = requests.post(
    f"{url}/review",
    auth=auth,
    json={"book_id": 84, "rating": 5, "comment": "Great book"},
)

assert r.status_code == 202, r.text
review_id = r.json()["review_id"]
assert r.json()["status"] == "pending"
print("create review:", r.status_code, "id", review_id)

r = requests.put(
    f"{url}/review/{review_id}",
    auth=auth,
    json={"rating": 4, "comment": "Very great book"},
)
assert r.status_code == 202, r.text
print("update:", r.status_code)

for _ in range(20):
    r = requests.get(f"{url}/review/{review_id}")
    if r.status_code == 200:
        break
    assert r.status_code == 202, r.text
    time.sleep(1)

assert r.status_code == 200, r.text
assert r.json()["status"] == "processed"
assert r.json()["book_title"]
print("get review ok", r.status_code, r.json()["book_title"])

r = requests.delete(f"{url}/review/{review_id}", auth=auth)
assert r.status_code == 200, r.text


print("delete:", r.status_code)
print("Ok")
