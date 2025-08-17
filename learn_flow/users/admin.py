from users.models import CustomUser
from core_admin.admin_site import custom_admin_site

custom_admin_site.register(CustomUser)
