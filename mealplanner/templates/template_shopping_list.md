# Shopping List
{% for day in plan %}
{% for meal in day %}
## {{meal.name}}
{% for ingredient in meal.ingredients %}
- {{ingredient}}
{% endfor %}
{% endfor %}
{% endfor %}