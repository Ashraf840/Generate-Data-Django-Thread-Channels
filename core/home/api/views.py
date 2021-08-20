from django.http import JsonResponse


def generate_student_data_test(request):
    return JsonResponse({
        'status': 'connected!'
    })