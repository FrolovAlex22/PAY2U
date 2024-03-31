import datetime
from django.db import transaction
from django.utils import timezone

from rest_framework import status
from .serializers import (
    SubscriptionSerializer,
)
from services.models import Subscription
from rest_framework.response import Response


def handle_subscribe_post(request, user, service, terms, bank_card):
    start_date_input = request.data.get('start_date')
    if start_date_input:
        try:
            start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return Response({'errors': 'Неверный формат даты.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        start_date = timezone.now()

    with transaction.atomic():
        duration_mapping = {
            "one_month": 30,
            "three_months": 90,
            "six_months": 180,
            "one_year": 360,
        }
        duration_days = duration_mapping.get(terms.duration, 30)
        amount_to_pay = terms.price * (duration_days / 30)
        
        if bank_card.balance < amount_to_pay:
            return Response({'errors': 'На банковской карте недостаточно средств для оформления подписки.'}, status=status.HTTP_400_BAD_REQUEST)

        end_date = start_date + datetime.timedelta(days=duration_days)

        if Subscription.objects.filter(service=service, user=user, terms=terms).exists():
            return Response({'errors': 'Вы уже подписаны на этот сервис.'}, status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription.objects.create(
            service=service, 
            user=user, 
            terms=terms, 
            start_date=start_date, 
            end_date=end_date, 
            bank_card=bank_card
        )
        bank_card.balance -= amount_to_pay
        bank_card.save()
        serializer = SubscriptionSerializer(subscription, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def handle_subscribe_delete(user, service, terms):
    subscription = user.subscriptions.filter(service=service, terms=terms).first()
    if not subscription:
        return Response({'errors': 'Вы не подписаны на этот сервис с указанными условиями подписки.'}, status=status.HTTP_400_BAD_REQUEST)

    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
