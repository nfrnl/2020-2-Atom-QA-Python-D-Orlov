from locust import HttpUser, TaskSet, task, between

AUTH_LOGIN = 'user_1'
AUTH_PASS = 'password_1'


class NonLoggedBehaviour(TaskSet):
    @task
    def main_page(self):
        self.client.get('/')

    @task
    def posts_page(self):
        self.client.get('/posts')


class LoggedBehaviour(TaskSet):
    def on_start(self):
        resp = self.client.get('/', auth=(AUTH_LOGIN, AUTH_PASS))
        self.client.headers.update({'Authorization': resp.request.headers['Authorization']})

    def on_stop(self):
        self.client.get('/logout')

    @task
    def profile(self):
        self.client.get('/profile')

    @task
    def new_post(self):
        self.client.get('/posts/new')


class ReadingPostsBehaviour(TaskSet):
    wait_time = between(10, 180)

    @task
    def read_10_posts(self):
        for i in range(10):
            self.client.get(f'/posts/{i}', name='/posts/[id]')
            self.wait()


class AppUser(HttpUser):
    tasks = [NonLoggedBehaviour, LoggedBehaviour, ReadingPostsBehaviour]
    wait_time = between(1, 4)
