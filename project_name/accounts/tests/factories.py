import factory
import uuid
import factory.django

from django.contrib.auth import get_user_model
import accounts.models


class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = accounts.models.Profile
    slug = factory.LazyAttribute(lambda u: "{{ project_name }}-%s" % str(uuid.uuid4())[0:12])


class ProfileTypeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = accounts.models.ProfileType

    profile = factory.SubFactory(ProfileFactory)
    profile_type = accounts.models.Choices.Profiles.OTHER


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()
    username = factory.Sequence(lambda n: "{{ project_name }}-%s" % n)
    password = "{{ project_name }}"
    email = factory.LazyAttribute(lambda u: "%s@{{ project_name }}.example.com" % u.username)

    profile = factory.RelatedFactory(ProfileFactory, name='user')

    @classmethod
    def _prepare(cls, create, **kwargs):
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        password = kwargs.pop('password', None)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user