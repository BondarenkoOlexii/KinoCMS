# import django_filters
# from django import forms
# from src.cinema.models import Session, Film, Cinema
#
#
# class SessionFilter(django_filters.FilterSet):
#
#     film_name = django_filters.CharFilter(
#         field_name='film__name',
#         lookup_expr='icontains',
#         label='Назва Фільму',
#         #widget
#     )
#
#     cinema = django_filters.ModelChoiceFilter(
#         film_name='hall__cinema',
#         queryset=Cinema.objects.all(),
#         label='Кінотеатр',
#         #widget
#     )
#
#     day = django_filters.DateFilter(
#         field_name='day',
#         label='Дата',
#         #widget
#     )
#
#     class Meta:
#         model = Session
#
#         fields = ['hall']