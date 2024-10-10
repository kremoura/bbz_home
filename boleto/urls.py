from django.urls import path
from boleto.views import boleto_pagamento, envia_email_boleto

urlpatterns = [
    path('boleto_pagamento/', boleto_pagamento, name='boleto_pagamento'),
    path('envia_email_boleto/', envia_email_boleto, name='envia_email_boleto'),
]