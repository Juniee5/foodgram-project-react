import io

from django.db.models.aggregates import Sum
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from backend.foodgram.settings import FILENAME


def download_shopping_cart(get):
    """Качаем список с ингредиентами."""
    A_POS = 50
    B_POS = 800
    C_POS = 14
    D_POS = 20
    E_POS = 15
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    shopping_cart = (
        get.user.shopping_cart.recipe.
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
            A_POS -= E_POS
            if A_POS <= A_POS:
                page.showPage()
                A_POS = B_POS
        page.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename=FILENAME)
