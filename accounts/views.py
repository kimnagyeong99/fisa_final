from django.shortcuts import render, redirect  # 페이지 렌더링 및 리디렉션
from django.contrib.auth.hashers import check_password  # 비밀번호 확인
from blog.models import UserProfile
from blog.forms import UserProfileForm  # UserProfileForm 폼 클래스


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.sex = 'M' if user_profile.SerialNum in ['1', '3'] else 'F'
            print(form.cleaned_data)  # 로그 출력
            user_profile.save()  # 데이터베이스에 저장
            return redirect('accounts/login.html')
        else:
            print(form.errors)  # 폼 에러 출력
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = UserProfileForm()
    return render(request, 'accounts/signup.html', {'form': form})

def agree(request):
    return render(request, 'accounts/join_agree.html')

def login_view(request):  # 이름을 login_view로 변경
    if request.method == 'POST':
        customer_id = request.POST['CustomerID']
        password = request.POST['Pw']

        try:
            # UserProfile에서 CustomerID를 이용하여 사용자 객체 가져오기
            user = UserProfile.objects.get(CustomerID=customer_id)
            
            # 비밀번호 확인
            if check_password(password, user.Pw):
                # 세션에 사용자 정보 저장하기
                request.session['user_id'] = user.CustomerID
                return redirect('loginmain')  # main.html로 리디렉션
            else:
                # 비밀번호가 틀린 경우
                return render(request, 'accounts/login.html', {'error': 'Invalid ID or password.'})
        
        except UserProfile.DoesNotExist:
            # 사용자 ID가 없는 경우
            return render(request, 'accounts/login.html', {'error': 'Invalid ID or password.'})
    
    return render(request, 'accounts/login.html')


def terms_content2(request):
    return render(request, 'accounts/mydata_form2.html')

def terms_content3(request):
    return render(request, 'accounts/mydata_form3.html')

def terms_content4(request):
    return render(request, 'accounts/logdata_form.html')

def terms_content5(request):
    return render(request, 'accounts/marketing.html')

