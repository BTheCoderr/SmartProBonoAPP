"""
Payment Processing Service for SmartProBono
Handles payment processing with Stripe and PayPal integration.
"""
import stripe
import paypalrestsdk
from datetime import datetime
from flask import current_app
from backend.database import db
from backend.models import Payment, User, Case, BailBond
import logging

logger = logging.getLogger(__name__)

class PaymentProcessingService:
    """Service for processing payments through various providers."""
    
    def __init__(self):
        # Stripe configuration
        self.stripe_public_key = current_app.config.get('STRIPE_PUBLIC_KEY')
        self.stripe_secret_key = current_app.config.get('STRIPE_SECRET_KEY')
        self.stripe_webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
        
        # PayPal configuration
        self.paypal_client_id = current_app.config.get('PAYPAL_CLIENT_ID')
        self.paypal_client_secret = current_app.config.get('PAYPAL_CLIENT_SECRET')
        self.paypal_mode = current_app.config.get('PAYPAL_MODE', 'sandbox')  # sandbox or live
        
        # Initialize Stripe
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
        
        # Initialize PayPal
        if self.paypal_client_id and self.paypal_client_secret:
            paypalrestsdk.configure({
                "mode": self.paypal_mode,
                "client_id": self.paypal_client_id,
                "client_secret": self.paypal_client_secret
            })
    
    def create_stripe_payment_intent(self, amount: float, currency: str = 'usd', 
                                   client_id: int = None, case_id: int = None, 
                                   bond_id: int = None, description: str = None):
        """Create a Stripe payment intent."""
        try:
            if not self.stripe_secret_key:
                raise ValueError("Stripe not configured")
            
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                description=description or f"Payment for case {case_id or 'general'}",
                metadata={
                    'client_id': str(client_id) if client_id else '',
                    'case_id': str(case_id) if case_id else '',
                    'bond_id': str(bond_id) if bond_id else '',
                    'service': 'SmartProBono'
                }
            )
            
            # Create payment record
            payment = Payment(
                client_id=client_id,
                case_id=case_id,
                bond_id=bond_id,
                amount=amount,
                currency=currency,
                payment_method='stripe',
                payment_type='online',
                status='pending',
                transaction_id=intent.id,
                reference_number=intent.id,
                payment_date=datetime.utcnow(),
                metadata={
                    'stripe_payment_intent_id': intent.id,
                    'stripe_client_secret': intent.client_secret
                }
            )
            
            db.session.add(payment)
            db.session.commit()
            
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'payment_id': payment.id
            }
            
        except Exception as e:
            logger.error(f"Error creating Stripe payment intent: {e}")
            return {'success': False, 'error': str(e)}
    
    def confirm_stripe_payment(self, payment_intent_id: str):
        """Confirm a Stripe payment intent."""
        try:
            if not self.stripe_secret_key:
                raise ValueError("Stripe not configured")
            
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                # Update payment record
                payment = Payment.query.filter_by(transaction_id=payment_intent_id).first()
                if payment:
                    payment.status = 'completed'
                    payment.payment_date = datetime.utcnow()
                    db.session.commit()
                    
                    # Send confirmation email
                    self._send_payment_confirmation_email(payment)
                    
                    return {'success': True, 'payment': payment.to_dict()}
                else:
                    return {'success': False, 'error': 'Payment record not found'}
            else:
                return {'success': False, 'error': f'Payment not successful: {intent.status}'}
                
        except Exception as e:
            logger.error(f"Error confirming Stripe payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_paypal_payment(self, amount: float, currency: str = 'USD',
                            client_id: int = None, case_id: int = None,
                            bond_id: int = None, description: str = None,
                            return_url: str = None, cancel_url: str = None):
        """Create a PayPal payment."""
        try:
            if not self.paypal_client_id:
                raise ValueError("PayPal not configured")
            
            # Create PayPal payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": return_url or f"{current_app.config.get('BASE_URL', 'http://localhost:3002')}/payment/success",
                    "cancel_url": cancel_url or f"{current_app.config.get('BASE_URL', 'http://localhost:3002')}/payment/cancel"
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description or f"Payment for case {case_id or 'general'}",
                    "custom": f"client_id:{client_id},case_id:{case_id},bond_id:{bond_id}"
                }]
            })
            
            if payment.create():
                # Create payment record
                db_payment = Payment(
                    client_id=client_id,
                    case_id=case_id,
                    bond_id=bond_id,
                    amount=amount,
                    currency=currency,
                    payment_method='paypal',
                    payment_type='online',
                    status='pending',
                    transaction_id=payment.id,
                    reference_number=payment.id,
                    payment_date=datetime.utcnow(),
                    metadata={
                        'paypal_payment_id': payment.id,
                        'approval_url': payment.links[1].href if payment.links else None
                    }
                )
                
                db.session.add(db_payment)
                db.session.commit()
                
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'approval_url': payment.links[1].href if payment.links else None,
                    'db_payment_id': db_payment.id
                }
            else:
                return {'success': False, 'error': payment.error}
                
        except Exception as e:
            logger.error(f"Error creating PayPal payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute_paypal_payment(self, payment_id: str, payer_id: str):
        """Execute a PayPal payment after approval."""
        try:
            if not self.paypal_client_id:
                raise ValueError("PayPal not configured")
            
            # Execute payment
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                # Update payment record
                db_payment = Payment.query.filter_by(transaction_id=payment_id).first()
                if db_payment:
                    db_payment.status = 'completed'
                    db_payment.payment_date = datetime.utcnow()
                    db.session.commit()
                    
                    # Send confirmation email
                    self._send_payment_confirmation_email(db_payment)
                    
                    return {'success': True, 'payment': db_payment.to_dict()}
                else:
                    return {'success': False, 'error': 'Payment record not found'}
            else:
                return {'success': False, 'error': payment.error}
                
        except Exception as e:
            logger.error(f"Error executing PayPal payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def process_manual_payment(self, amount: float, payment_method: str, 
                             client_id: int = None, case_id: int = None,
                             bond_id: int = None, reference_number: str = None,
                             notes: str = None):
        """Process a manual payment (cash, check, bank transfer)."""
        try:
            # Create payment record
            payment = Payment(
                client_id=client_id,
                case_id=case_id,
                bond_id=bond_id,
                amount=amount,
                currency='USD',
                payment_method=payment_method,
                payment_type='manual',
                status='completed',
                reference_number=reference_number,
                payment_date=datetime.utcnow(),
                notes=notes
            )
            
            db.session.add(payment)
            db.session.commit()
            
            # Send confirmation email
            self._send_payment_confirmation_email(payment)
            
            return {'success': True, 'payment': payment.to_dict()}
            
        except Exception as e:
            logger.error(f"Error processing manual payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def refund_payment(self, payment_id: int, amount: float = None, reason: str = None):
        """Refund a payment."""
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return {'success': False, 'error': 'Payment not found'}
            
            refund_amount = amount or payment.amount
            
            if payment.payment_method == 'stripe':
                return self._refund_stripe_payment(payment, refund_amount, reason)
            elif payment.payment_method == 'paypal':
                return self._refund_paypal_payment(payment, refund_amount, reason)
            else:
                # Manual refund
                return self._refund_manual_payment(payment, refund_amount, reason)
                
        except Exception as e:
            logger.error(f"Error refunding payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def _refund_stripe_payment(self, payment: Payment, amount: float, reason: str = None):
        """Refund a Stripe payment."""
        try:
            if not self.stripe_secret_key:
                raise ValueError("Stripe not configured")
            
            # Create refund
            refund = stripe.Refund.create(
                payment_intent=payment.transaction_id,
                amount=int(amount * 100),  # Convert to cents
                reason='requested_by_customer' if not reason else 'other',
                metadata={'reason': reason or 'Refund requested'}
            )
            
            # Update payment record
            payment.status = 'refunded'
            payment.metadata = payment.metadata or {}
            payment.metadata['refund_id'] = refund.id
            payment.metadata['refund_amount'] = amount
            payment.metadata['refund_reason'] = reason
            db.session.commit()
            
            return {'success': True, 'refund_id': refund.id}
            
        except Exception as e:
            logger.error(f"Error refunding Stripe payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def _refund_paypal_payment(self, payment: Payment, amount: float, reason: str = None):
        """Refund a PayPal payment."""
        try:
            if not self.paypal_client_id:
                raise ValueError("PayPal not configured")
            
            # Find the sale transaction
            sale_id = payment.metadata.get('sale_id') if payment.metadata else None
            if not sale_id:
                return {'success': False, 'error': 'Sale ID not found'}
            
            # Create refund
            refund = paypalrestsdk.Sale({
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "reason": reason or "Refund requested"
            })
            
            if refund.refund(sale_id):
                # Update payment record
                payment.status = 'refunded'
                payment.metadata = payment.metadata or {}
                payment.metadata['refund_id'] = refund.id
                payment.metadata['refund_amount'] = amount
                payment.metadata['refund_reason'] = reason
                db.session.commit()
                
                return {'success': True, 'refund_id': refund.id}
            else:
                return {'success': False, 'error': refund.error}
                
        except Exception as e:
            logger.error(f"Error refunding PayPal payment: {e}")
            return {'success': False, 'error': str(e)}
    
    def _refund_manual_payment(self, payment: Payment, amount: float, reason: str = None):
        """Process a manual refund."""
        try:
            # Update payment record
            payment.status = 'refunded'
            payment.metadata = payment.metadata or {}
            payment.metadata['refund_amount'] = amount
            payment.metadata['refund_reason'] = reason
            payment.metadata['refund_date'] = datetime.utcnow().isoformat()
            db.session.commit()
            
            return {'success': True, 'message': 'Manual refund processed'}
            
        except Exception as e:
            logger.error(f"Error processing manual refund: {e}")
            return {'success': False, 'error': str(e)}
    
    def _send_payment_confirmation_email(self, payment: Payment):
        """Send payment confirmation email."""
        try:
            from backend.services.email_notification_service import email_notification_service
            
            client = User.query.get(payment.client_id)
            if not client or not client.email:
                return
            
            subject = f"Payment Confirmation - ${payment.amount}"
            body = f"""
Dear {client.first_name or 'Client'},

Your payment has been successfully processed.

Payment Details:
- Amount: ${payment.amount}
- Payment Method: {payment.payment_method}
- Transaction ID: {payment.transaction_id}
- Date: {payment.payment_date.strftime('%B %d, %Y at %I:%M %p')}

Thank you for your payment.

Best regards,
SmartProBono Team
            """
            
            email_notification_service.send_email(
                to_email=client.email,
                subject=subject,
                body=body
            )
            
        except Exception as e:
            logger.error(f"Error sending payment confirmation email: {e}")
    
    def get_payment_methods(self):
        """Get available payment methods."""
        methods = ['cash', 'check', 'bank_transfer']
        
        if self.stripe_secret_key:
            methods.append('stripe')
        
        if self.paypal_client_id:
            methods.append('paypal')
        
        return methods
    
    def get_payment_statistics(self, client_id: int = None, case_id: int = None):
        """Get payment statistics."""
        try:
            query = Payment.query
            
            if client_id:
                query = query.filter_by(client_id=client_id)
            if case_id:
                query = query.filter_by(case_id=case_id)
            
            total_payments = query.count()
            total_amount = query.with_entities(db.func.sum(Payment.amount)).scalar() or 0
            completed_payments = query.filter_by(status='completed').count()
            pending_payments = query.filter_by(status='pending').count()
            
            # Payment method breakdown
            method_counts = {}
            for method in ['cash', 'check', 'bank_transfer', 'stripe', 'paypal']:
                count = query.filter_by(payment_method=method).count()
                if count > 0:
                    method_counts[method] = count
            
            return {
                'total_payments': total_payments,
                'total_amount': float(total_amount),
                'completed_payments': completed_payments,
                'pending_payments': pending_payments,
                'method_counts': method_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting payment statistics: {e}")
            return {}

# Create singleton instance
payment_processing_service = PaymentProcessingService()
