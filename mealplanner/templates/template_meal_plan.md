# Meal Plan
{% for day in plan %}
## Day {{loop.index}}
{% for meal in day %}
- {{meal.category}} - [{{meal.name}}]({{meal.fileloc}})
{% endfor %}
{% endfor %}