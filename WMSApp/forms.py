# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import VAPProductionData, ProductData, SourceData, ProductionDescription
import datetime

class VAPProductionDataForm(forms.ModelForm):

    class Meta:
        model = VAPProductionData
        fields = '__all__'
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'TimeStart': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'TimeEnd': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'PlantLoc': forms.Select(attrs={'class': 'form-control'}),
            'Shift': forms.Select(attrs={'class': 'form-control'}),
            'Product': forms.Select(attrs={'class': 'form-control'}),
            'Source': forms.Select(attrs={'class': 'form-control'}),
            'ProdMinDescrip': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Date'].initial = datetime.date.today()
        self.fields['PlantLoc'].initial = 'PULILAN'
        self.fields['Shift'].initial = 'DAY SHIFT'
        
        # Ensure proper querysets for foreign keys
        self.fields['Product'].queryset = ProductData.objects.all()
        self.fields['Source'].queryset = SourceData.objects.all()
        self.fields['ProdMinDescrip'].queryset = ProductionDescription.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        time_start = cleaned_data.get('TimeStart')
        time_end = cleaned_data.get('TimeEnd')

        if time_start is not None and time_end is not None:
            if time_start == time_end:
                raise ValidationError("Start time and end time cannot be the same")
            
            # Calculate total time
            start_min = time_start.hour * 60 + time_start.minute
            end_min = time_end.hour * 60 + time_end.minute
            total_min = end_min - start_min
            if total_min < 0:
                total_min += 24 * 60
            
            hours = total_min // 60
            minutes = total_min % 60
            # Set the value to the instance and cleaned_data if the model has a Total field
            total_str = f"{hours} hr {minutes:02d} min"
            if hasattr(self.instance, 'Total'):
                self.instance.Total = total_str
            if 'Total' in self.fields:
                cleaned_data['Total'] = total_str

        return cleaned_data

class ImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Select Excel file to import',
        help_text='The Excel file should match the export format'
    )