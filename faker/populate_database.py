from faker import Faker
import requests
import time

BASE_URL = "http://backend:5000"
USER_COUNT = 10

WAIT_FOR_BACKEND_RETRIES = 10
BACKEND_WAIT_TIME = 5

fake = Faker()

log = open("/app/logs/log.txt", "w")

users = []


def create_user():
    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    body = {"username": username, "email": email, "password": password}

    response = requests.post(f"{BASE_URL}/register", json=body)

    if response.status_code != 201:
        log.write(
            f"Failed to create user {username} with email {email} and password {password}\n"
        )
        return

    log.write(f"User {username} created with email {email} and password {password}\n")
    users.append(body)


def create_users():
    for _ in range(USER_COUNT):
        create_user()


def login(email, password):
    body = {"email": email, "password": password}

    response = requests.post(f"{BASE_URL}/login", json=body)

    if response.status_code != 200:
        return None

    token = response.json()["token"]
    return token


fd_requests = []


def send_friend_request(user, friend, token):
    body = {
        "email": friend["email"],
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{BASE_URL}/friends/request", json=body, headers=headers)

    if response.status_code != 200:
        log.write(
            f"{user['email']} couldn't send friend request to {friend['email']}\n"
        )
        return

    log.write(f"{user['email']} sent friend request to {friend['email']}\n")
    fd_requests.append({"sender": user, "recipient": friend})


friendships = []


def process_friend_request(request):
    sender = request["sender"]
    recipient = request["recipient"]

    token = login(recipient["email"], recipient["password"])

    if token is None:
        return

    response = fake.random_element(["accept", "reject"])

    body = {
        "email": sender["email"],
        "response": response,
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(f"{BASE_URL}/friends/respond", json=body, headers=headers)

    if response.status_code != 200:
        log.write(
            f"couldn't process request between {sender['email']} and {recipient['email']}\n"
        )
        return

    if response == "accept":
        friendships.append({"user1": sender, "user2": recipient})
        log.write(
            f"Friend request between {sender['email']} and {recipient['email']} accepted\n"
        )
        return

    log.write(
        f"Friend request between {sender['email']} and {recipient['email']} rejected\n"
    )


def create_frienships():
    for user in users:
        token = login(user["email"], user["password"])
        if token is None:
            continue

        for _ in range(USER_COUNT // 4):
            friend = fake.random_element(users)
            send_friend_request(user, friend, token)

    for request in fd_requests:
        process_friend_request(request)


def add_movie_to_list(token, movie):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/watchlist/movie/add/{movie["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add movie {movie['title']} to watchlist\n")
        return

    log.write(f"Movie {movie['title']} added to watchlist\n")


def add_tv_show_to_list(token, tv_show):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/watchlist/tv/add/{tv_show["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add tv show {tv_show['name']} to watchlist\n")
        return

    log.write(f"Tv show {tv_show['name']} added to watchlist\n")


def add_person_to_list(token, person):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/favourite/people/add/{person["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add person {person['name']} to favourites\n")
        return

    log.write(f"Person {person['name']} added to favourites\n")


def add_movie_to_finished_list(token, movie):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/finished/movie/add/{movie["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add movie {movie['title']} to finished list\n")
        return

    rating = float(fake.random_int(0, 10))

    response = requests.post(
        f"{BASE_URL}/finished/movie/{movie['id']}/rate/{rating}",
        headers=headers,
    )

    if response.status_code != 200:
        log.write(f"Couldn't rate movie {movie['title']}, {response.json}\n")

    body = {
        "review": fake.text(),
    }

    response = requests.post(
        f"{BASE_URL}/finished/movie/{movie['id']}/review", json=body, headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't review movie {movie['title']}\n")
        return

    log.write(f"Movie {movie['title']} added to finished list\n")


def add_tv_show_to_finished_list(token, tv_show):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{BASE_URL}/finished/tv/add/{tv_show["id"]}", headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't add tv show {tv_show['name']} to finished list\n")
        return

    rating = float(fake.random_int(0, 10))

    response = requests.post(
        f"{BASE_URL}/finished/show/{tv_show['id']}/rate/{rating}",
        headers=headers,
    )

    if response.status_code != 200:
        log.write(f"Couldn't rate tv show {tv_show['name']}\n")
        return

    body = {
        "review": fake.text(),
    }

    response = requests.post(
        f"{BASE_URL}/finished/show/{tv_show['id']}/review", json=body, headers=headers
    )

    if response.status_code != 200:
        log.write(f"Couldn't review tv show {tv_show['name']}\n")
        return

    log.write(f"Tv show {tv_show['name']} added to finished list\n")


def populate_users_lists():
    movies = (
        requests.get(f"{BASE_URL}/movie/popular/{fake.random_int(1, 10)}")
        .json()
        .get("results")
    )
    tv_shows = (
        requests.get(f"{BASE_URL}/tv/popular/{fake.random_int(1, 10)}")
        .json()
        .get("results")
    )
    people = requests.get(f"{BASE_URL}/person/popular").json().get("results")

    for user in users:
        token = login(user["email"], user["password"])
        if token is None:
            continue

        for _ in range(5):
            movie = fake.random_element(movies)
            tv_show = fake.random_element(tv_shows)
            person = fake.random_element(people)

            add_movie_to_list(token, movie)
            add_tv_show_to_list(token, tv_show)
            add_person_to_list(token, person)

            if fake.boolean(10):
                add_movie_to_finished_list(token, movie)
            if fake.boolean(10):
                add_tv_show_to_finished_list(token, tv_show)


def populate_database():
    create_users()
    create_frienships()
    populate_users_lists()
    pass


def wait_for_backend():
    retries = 0
    while retries < WAIT_FOR_BACKEND_RETRIES:
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                log.write("Backend is online.\n")
                return
        except requests.ConnectionError:
            log.write("Backend is not reachable. Retrying...\n")
        time.sleep(BACKEND_WAIT_TIME)
        retries += 1

    raise Exception("Backend did not become available in time.")


if __name__ == "__main__":
    wait_for_backend()
    populate_database()
