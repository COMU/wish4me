from django.contrib.auth.models import User

from foursq.models import FoursqProfile
import settings


class FoursqAuthBackend(object):

    def authenticate(self, request, credentials):

        if credentials is None:
            return None

        foursq_id = credentials['id']
        foursq_acces_token = credentials['access_token']
        foursq_username = credentials['username']
        foursq_firstname = credentials['first_name']
        foursq_lastname = credentials['last_name']

        try:
            foursq_profile = FoursqProfile.objects.get(foursq_id=foursq_id)
        except FoursqProfile.DoesNotExist:
            foursq_profile = FoursqProfile(
                foursq_id = foursq_id,
                access_token = foursq_acces_token,
                username = foursq_username,
                firstname = foursq_firstname,
                lastname = foursq_lastname)

        foursq_profile.save()

        backend = foursq_profile.getLoginBackend(request)
        user = backend.login(
            foursq_profile, related_name='foursq_profile',
            username=foursq_username, email=settings.DEFAULT_EMAIL)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
