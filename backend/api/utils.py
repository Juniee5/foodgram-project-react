from django.http import HttpResponse

from recipes.models import ShoppingCart


def download_shopping_cart(request):
    """Качаем список с ингредиентами."""
    shopping_cart = ShoppingCart.objects.filter(user=request.user).all()
    shopping_list = {}
    for item in shopping_cart:
        for recipe_ingredient in item.recipe.recipe_ingredients.all():
            ingredients__name = recipe_ingredient.ingredient.name
            measuring_unit = recipe_ingredient.ingredient.measurement_unit
            amount = recipe_ingredient.amount
            if ingredients__name not in shopping_list:
                shopping_list[ingredients__name] = {
                    'ingredients__name': ingredients__name,
                    'measurement_unit': measuring_unit,
                    'amount': amount
                }
            else:
                shopping_list[ingredients__name]['amount'] += amount
    content = (
        [f'{item["ingredients__name"]} ({item["measurement_unit"]}) '
         f'- {item["amount"]}\n'
         for item in shopping_list.values()]
    )
    filename = 'shoppingcart.pdf'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )
    return response
