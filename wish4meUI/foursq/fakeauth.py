from django.contrib.auth.models import User

class FakeAuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
