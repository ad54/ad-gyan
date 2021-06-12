from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q

from.utils import gen_sql_search_q, gen_search_string

import csv
from .models import IndexItem
import pandas as pd
import logging


@login_required
def index(request):
    return render(request, 'idx_search/index.html')

@login_required
def search(request):
    try:
        if request.method == 'GET':
            search_string = request.GET.get('search_string','')
        else:
            search_string = request.POST.get('search_string','')
        search_q = gen_sql_search_q(search_string)

        items = IndexItem.objects.raw(search_q)

        limit = int(request.GET.get('limit', 20))
        paginator = Paginator(items, limit)
        page_request_var = 'page'
        if request.method == 'GET':
            page = request.GET.get(page_request_var)
        else:
            page = '1'
        try:
            paginated_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except InvalidPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        total_objects = paginator.count
        context = {'items': paginated_queryset, 'page_request_var': page_request_var ,
                   'total_objects':total_objects, 'search_string':search_string}
        return render(request, 'idx_search/list_item.html', context=context)
    except Exception as e:
        logging.error(e)
        messages.error(request, 'Internal server error , Please report the same.')
        return redirect(reverse("index"))

@login_required
def import_data(request):
    # declaring template
    current_user = ''
    template = 'idx_search/import_items.html'
    prompt = {
        'order': 'Order of the CSV should be book_num,book_name, index_string, page_num, gatha_num, path',
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']


    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    else:
        for df in pd.read_csv(csv_file, chunksize=10):
            old_columns = list(df.columns)
            new_columns = ['book_num', 'book_name', 'index_string', 'page_num', 'gatha_num', 'path']
            columns = {}
            for col, new_col in zip(old_columns, new_columns):
                columns[col] = new_col

            df.rename(columns=columns, inplace=True)
            df['search_string'] = df['index_string'].apply(lambda x: gen_search_string(x))

            objs = [IndexItem(
                index_string=row['index_string'],
                search_string=row['search_string'],
                path=row['path'],
                gatha_num=row['gatha_num'],
                page_num=row['page_num'],
                book_num=row['book_num'],
                book_name=row['book_name'],
                last_update_by=current_user,
                created_by=current_user
            )
                for idx, row in df.iterrows()
            ]
            IndexItem.objects.bulk_create(objs)
        messages.success(request, 'File Uploaded Successfully')
    return render(request, template)


def search_old(request):
    search_string = request.GET.get('q', '')
    my_model = IndexItem.objects.filter(search_string__contains=search_string)
    # number of items on each page
    number_of_item = 3
    # Paginator
    paginatorr = Paginator(my_model, number_of_item)
    # query_set for first page
    first_page = paginatorr.page(1).object_list
    # range of page ex range(1, 3)
    page_range = paginatorr.page_range

    context = {
        'paginatorr': paginatorr,
        'first_page': first_page,
        'page_range': page_range
    }
    #
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)  # getting page number
        results = list(paginatorr.page(page_n).object_list.values('id', 'search_string'))
        return JsonResponse({"results": results})

    return render(request, 'idx_search/list_items.html', context)

@login_required
def get_analytics(request):
    try:
        num_of_books = IndexItem.objects.values('book_num').distinct().count()
        num_of_indexes = IndexItem.objects.values('search_string').count()

        analytics_dict = {'num_of_books':num_of_books,
         'num_of_indexes': num_of_indexes}

        keys = analytics_dict.keys()
        values = analytics_dict.values()
        mylist = zip(keys, values)
    except Exception as e:
        mylist = zip([],[])
        logging.error(e)
        messages.error(request, 'Internal server error , Please report the same.')
    return render(request, 'idx_search/analytics.html', {'mylist': mylist})


def export_data(request):
    try:
        search_string = request.POST.get('search_string', '')
        search_q = gen_sql_search_q(search_string)
        items = IndexItem.objects.raw(search_q)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'
        writer = csv.writer(response)
        writer.writerow(['index_string', 'book_num', 'book_name', 'path','page_num','gatha_num'])
        for item in items:
            writer.writerow([item.index_string, item.book_num, item.book_name, item.path, item.page_num, item.gatha_num])
        messages.success(request, 'File Created Successfully')
        return response
    except Exception as e:
        logging.error(e)
        messages.error(request, 'Internal server error , Please report the same.')
        return redirect(reverse("index"))





