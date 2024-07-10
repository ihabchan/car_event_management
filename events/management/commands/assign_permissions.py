from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Assigns permissions to groups'

    def handle(self, *args, **kwargs):

        admin_gro4p, created = Group.objects.get_or_create(name='Admin')
        staff_group, created = Group.objects.get_or_create(name='Staff')
        user_group, created = Group.objects.get_or_create(name='User')

        all_permissions = Permission.objects.all()

        admin_group.permissions.set(all_permissions)

        staff_permissions = [
            'add_post', 'change_post', 'delete_post',
            'add_merch', 'change_merch', 'delete_merch',
            'add_event', 'change_event', 'delete_event'
        ]
        staff_group.permissions.set(Permission.objects.filter(codename__in=staff_permissions))

        user_permissions = [

        ]
        user_group.permissions.set(Permission.objects.filter(codename__in=user_permissions))

        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to groups'))
