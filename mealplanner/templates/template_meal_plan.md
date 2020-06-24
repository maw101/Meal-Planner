# Meal Plan

{% for meal in meals %}
- [{{meal.name}}]({{meal.fileloc}})
{% endfor %}