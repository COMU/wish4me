from django.contrib.auth.models import User

from foursq.models import FoursqProfile
import settings


class FoursqAuthBackend(object):

    def authenticate(self, request, credentials, backend="foursq"):

        if credentials is None:
            return None

        foursq_id = credentials['foursq_id']
        foursq_acces_token = credentials['access_token']
        foursq_email = credentials['email']
        foursq_firstname = credentials['firstname']
        foursq_lastname = credentials['lastname']

        try:
            foursq_profile = FoursqProfile.objects.get(foursq_id=foursq_id)
        except FoursqProfile.DoesNotExist:
            foursq_profile = FoursqProfile(
                foursq_id = foursq_id,
                access_token = foursq_acces_token,
                email = foursq_email,
                firstname = foursq_firstname,
                lastname = foursq_lastname)

        foursq_profile.save()

        backend = foursq_profile.getLoginBackend(request)
        user = backend.login(
            foursq_profile, related_name='foursq_profile',
            first_name=foursq_firstname, last_name=foursq_lastname,
            email=foursq_email)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
