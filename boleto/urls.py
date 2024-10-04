from django.urls import path
from boleto.views import boleto_pagamento

urlpatterns = [
    path('boleto_pagamento/', boleto_pagamento, name='boleto_pagamento'),
]