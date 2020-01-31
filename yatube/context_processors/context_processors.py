import datetime as dt


def custom_context_processors(request):
    now = dt.datetime.now()
    
    return {
        'year' : now.year
    }