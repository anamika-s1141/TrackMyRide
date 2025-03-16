import stripe
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, RefundRequest
from .serializers import (
    PaymentSerializer, RefundRequestSerializer,
    PaymentCreateSerializer, RefundRequestCreateSerializer
)
from apps.notifications.models import Notification, NotificationType

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Payment.objects.all()
        return Payment.objects.filter(ticket__student__user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    @action(detail=True, methods=['post'])
    def create_payment_intent(self, request, pk=None):
        payment = self.get_object()
        
        try:
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),  # Convert to cents
                currency=payment.currency.lower(),
                metadata={
                    'payment_id': payment.id,
                    'ticket_id': payment.ticket.id,
                    'user_id': request.user.id
                }
            )
            
            # Update payment with Stripe ID
            payment.stripe_payment_intent_id = intent.id
            payment.save()
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_id': payment.id
            })
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        payment = self.get_object()
        
        try:
            # Retrieve PaymentIntent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)
            
            if intent.status == 'succeeded':
                # Update payment status
                payment.status = Payment.PaymentStatus.COMPLETED
                payment.paid_at = timezone.now()
                payment.receipt_url = intent.charges.data[0].receipt_url
                payment.save()
                
                # Update ticket status
                ticket = payment.ticket
                ticket.status = ticket.Status.APPROVED
                ticket.save()
                
                # Create notification
                Notification.objects.create(
                    title='Payment Successful',
                    message=f'Your payment of {payment.amount} {payment.currency} has been processed successfully.',
                    notification_type=NotificationType.PAYMENT,
                    user=request.user,
                    data={'payment_id': payment.id, 'ticket_id': ticket.id}
                )
                
                return Response(PaymentSerializer(payment).data)
            
            return Response(
                {'error': 'Payment not successful'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class RefundRequestViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all()
    serializer_class = RefundRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return RefundRequest.objects.all()
        return RefundRequest.objects.filter(requested_by=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RefundRequestCreateSerializer
        return RefundRequestSerializer

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve_refund(self, request, pk=None):
        refund_request = self.get_object()
        
        if request.user.role != 'ADMIN':
            return Response(
                {'error': 'Only admins can approve refunds'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            payment = refund_request.payment
            
            # Create refund in Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.stripe_payment_intent_id,
                amount=int(payment.amount * 100)  # Convert to cents
            )
            
            # Update refund request
            refund_request.status = RefundRequest.RefundStatus.COMPLETED
            refund_request.approved_by = request.user
            refund_request.stripe_refund_id = refund.id
            refund_request.refunded_amount = payment.amount
            refund_request.save()
            
            # Update payment status
            payment.status = Payment.PaymentStatus.REFUNDED
            payment.save()
            
            # Create notification
            Notification.objects.create(
                title='Refund Approved',
                message=f'Your refund request for {payment.amount} {payment.currency} has been approved.',
                notification_type=NotificationType.PAYMENT,
                user=refund_request.requested_by,
                data={'refund_request_id': refund_request.id, 'payment_id': payment.id}
            )
            
            return Response(RefundRequestSerializer(refund_request).data)
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 