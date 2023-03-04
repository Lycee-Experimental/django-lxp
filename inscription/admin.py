from django.contrib import admin
from .models import BaseEleve, MEE, Allergie, Spe, TroubleCognitif, LV

# Register your models here.
admin.site.register(BaseEleve)
admin.site.register(MEE)
admin.site.register(Allergie)
admin.site.register(TroubleCognitif)
admin.site.register(Spe)
admin.site.register(LV)

