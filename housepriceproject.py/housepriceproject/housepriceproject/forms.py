from django import forms

EMPTY_CHOICES = (
    ('', '-'*10),
)


STATION_CHOICES = (
    ('MG1', '日吉'),
    ('MG2', '武蔵小杉'),
    ('MG3', '多摩川'),
    ('MG4', '田園調布'),
    ('MG5', '大岡山'),
    ('MG6', '武蔵小山'),
    ('MG7', '目黒'),

)


class SampleForm(forms.Form):
    station = forms.ChoiceField(
        label='駅名選択',
        widget=forms.CheckboxSelectMultiple,
        choices=STATION_CHOICES,
        required=True,
    )

    time = forms.IntegerField(
        label='徒歩',
        min_value=0,
        max_value=100,
        required=True,
    )

    age = forms.IntegerField(
        label='築年数',
        min_value=0,
        max_value=200,
        required=True,
    )

    send_message = forms.BooleanField(
        label='送信する',
        required=False,
    )
