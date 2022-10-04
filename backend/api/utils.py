from django.db.models.aggregates import Sum
from django.http import HttpResponse

from recipes.models import Recipe


def get_shopping_list(request.user):
    """Качаем список с ингредиентами."""
    user = request.get.user
    recipes = Recipe.objects.filter(
        in_favourites__user=user,
        in_favourites__is_in_shopping_cart=True
    )
    ingredients = recipes.values(
        'ingredients__name',
        'ingredients__measurement_unit__name').order_by(
        'ingredients__name').annotate(
        ingredients_total=Sum('ingredient_amounts__amount')
    )
    shopping_list = {}
    for item in ingredients:
        title = item.get('ingredients__name')
        count = str(item.get('ingredients_total')) + ' ' + item[
            'ingredients__measurement_unit__name'
        ]
        shopping_list[title] = count
    data = ''
    for key, value in shopping_list.items():
        data += f'{key} - {value}\n'
    return HttpResponse(data, content_type='text/plain')
