from django.http import JsonResponse
from home.thread import CreateStudentsThread
import json


# Test API
def generate_student_data_test(request):
    return JsonResponse({
        'status': 'connected!'
    })



# API-method [GET] ****************************************************************************************************** [ A P I ]
"""
Whenever this api-view/ api-method gets called, it will
[
    01. "creating dummy-data-row in the DB".
    02. "also simultaneously sends that each data to the channel-consumer-group immedietly".
]
"""
async def generate_student_data(request):
    ### OK, but not using, requires a browser-tab to execute the API-call manually
    # print(json.loads(request.body))

    # total = request.GET.get('total')    # get the value of "GET" dict-variable ("total") from the browser-url
    # # since the number is fetchd from the browser-url, it's a string-type number, so it's need to be converted into int.
    # CreateStudentsThread(int(total)).start()
    
    # return JsonResponse({ 
    #     'trigger': 'To populate data using this page\'s url',
    #     'status': 200 
    # })
    ### OK, but not using, requires a browser-tab to execute the API-call manually


    try:
        if request.method == 'POST':
            print('Post with Axios!')
            total_num = request.POST.get('total')
            json_data = {
                'total': total_num,
            }
            print('Total Number: %s' % total_num)
            print('Type of: %s' % type(total_num))

            CreateStudentsThread(int(total_num)).start()
        
        return JsonResponse({ 'status': True, 
            'message': 'Success', 
            'Total_dummy_student_record': json_data })
    except:
        return JsonResponse({ 'status': False, 'error': 'Something went wrong' })