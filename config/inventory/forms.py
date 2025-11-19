from django import forms
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['book', 'quantity', 'reason', 'source', 'note']

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        # Prevent stock-out below zero
        if qty < 0 and abs(qty) > self.cleaned_data['book'].stock:
            raise forms.ValidationError("Not enough stock available.")
        return qty
