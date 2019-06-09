#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms


class DateTimePickerInput(forms.TextInput):
    template_name = 'stark/datetime_picker.html'
