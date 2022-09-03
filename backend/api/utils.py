import io

from django.db.models.aggregates import Sum
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..foodgram.settings import FILENAME


@action(
    detail=False,
    methods=['get'],
    permission_classes=(IsAuthenticated,))
def download_shopping_cart(self, request):
    """Качаем список с ингредиентами."""
    A_POS = 50
    B_POS = 800
    C_POS = 14
    D_POS = 20
    I_POS = 15
    F_POS = 24
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    shopping_cart = (
        request.user.shopping_cart.recipe.
        values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__amount')).order_by())
    page.setFont('Vera', C_POS)
    if shopping_cart:
        indent = D_POS
        page.drawString(A_POS, B_POS, 'Cписок покупок:')
        for index, recipe in enumerate(shopping_cart, start=1):
            page.drawString(
                A_POS, B_POS - indent,
                f'{index}. {recipe["ingredients__name"]} - '
                f'{recipe["amount"]} '
                f'{recipe["ingredients__measurement_unit"]}.')
            A_POS -= I_POS
            if A_POS <= A_POS:
                page.showPage()
                A_POS = B_POS
        page.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename=FILENAME)
