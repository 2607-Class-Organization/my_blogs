from django import forms
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Row, Column, Submit, Button
INPUT_CLASSES = (
    'mt-2 block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 '
    'text-slate-900 shadow-sm outline-none transition focus:border-indigo-500 '
    'focus:ring-4 focus:ring-indigo-100'
)




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "excerpt",
            "content",
            "image",
            "category",
            "status",
            "published_at",
            "featured"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = (
            'mt-2 block w-full rounded-xl border border-gray-300 bg-white px-4 py-3 '
            'text-gray-900 shadow-sm transition focus:border-gold-500 '
            'focus:ring-4 focus:ring-yellow-100'
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', input_classes)

        self.fields['excerpt'].widget.attrs.update(rows=3)
        self.fields['content'].widget.attrs.update(rows=12)
        self.fields['published_at'].widget.attrs.update(type='datetime-local')
        self.fields['featured'].widget.attrs['class'] = (
            'h-4 w-4 rounded border-gray-300 text-gold-600 focus:ring-gold-500'
        )

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Blog Information',
                Row(
                    Column(Field('title'), css_class='col-md-6'),
                    Column(Field('category'), css_class='col-md-6'),
                ),
                'excerpt',
                'content',
                'image',
                Row(
                    Column('status', css_class='col-md-6'),
                    Column('published_at', css_class='col-md-6'),
                ),
                'featured',
            ),
            Submit(
                'submit',
                'Update Post' if self.instance.pk else 'Create Post',
                css_class='rounded-xl bg-gold-600 px-5 py-3 font-semibold text-white shadow-sm hover:bg-gold-700',
            ),
            Button('cancel', 'Cancel', css_class='ml-2 rounded-xl border border-gray-300 px-5 py-3 font-semibold text-gray-700 hover:bg-gray-50',
                   onclick="window.history.back();")
        )
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
        
#         fields = [
#             "title",
#             "excerpt",
#             "content",
#             "image",
#             "category",
#             "status",
#             "published_at",
#             "featured"
#         ]
        
#         widgets = {
#            "title": forms.TextInput(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "placeholder": "Enter post title",
#                 }
#             ),

#             "excerpt": forms.Textarea(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "rows": 3,
#                     "placeholder": "Write a short summary of your post...",
#                 }
#             ),

#             "content": forms.Textarea(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "rows": 15,
#                     "placeholder": "Write your article here...",
#                 }
#             ),

#             "category": forms.Select(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                 }
#             ),

#             "status": forms.Select(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                 }
#             ),

#             "published_at": forms.DateTimeInput(
#                 attrs={
#                     "class": "w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-gold-500 focus:ring-gold-500",
#                     "type": "datetime-local",
#                 }
#             ),

#             "featured": forms.CheckboxInput(
#                 attrs={
#                     "class": "h-4 w-4 rounded border-gray-300 text-gold-600 focus:ring-gold-500",
#                 }
#             ),
#         }
class SubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
           "autocomplete": 'email',
           "placeholder": "email@example.com",
           "class": INPUT_CLASSES, 
        }
    ))