
from django.core.paginator import Paginator

def data_paginator(request,query, num_pages):
    paginator = Paginator(query, num_pages)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj