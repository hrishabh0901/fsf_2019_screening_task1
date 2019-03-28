from django.test import TestCase,Client,SimpleTestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User
from accounts.views import login,signup,logout,userdetail
from .models import Profile

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_signup_url(self):
        url = reverse(signup)
        self.assertEqual(resolve(url).func,signup)

    def test_login_url(self):
        url = reverse(login)
        self.assertEqual(resolve(url).func,login)

    def test_logout_url(self):
        url = reverse(logout)
        self.assertEqual(resolve(url).func,logout)

    def test_userdetail_url(self):
        url = reverse(userdetail,args=[100000,'None'])
        self.assertEqual(resolve(url).func,userdetail)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse(signup)
        self.login_url = reverse(login)
        self.logout_url = reverse(logout)
        self.userdetail_url = reverse(userdetail,args=[1,'None'])

    def test_signup_view_GET(self):

        response = self.client.get(self.signup_url)

        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/signup.html')

    def test_signup_view_POST(self):


        # Checking when the user gives both password same and username is unique
        # so userdetail page is rendered on successful signup
        response = self.client.post(self.signup_url,{
            'username':'user1',
            'password1':'pass1',
            'password2':'pass1'
        },follow=True)

        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/userdetail.html')
        self.assertTrue(response.context['user'].is_authenticated)



        # Checking when the user gives does not give both password same
        # thus again the signup page is rendered with error message
        response = self.client.post(self.signup_url, {
            'username': 'user1',
            'password1': 'pass1',
            'password2': 'pass2'
        })

        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'accounts/signup.html')


        # Checking when the user gives does  give both password
        # same but not a unique username again the signup page is
        # rendered with error message
        response = self.client.post(self.signup_url, {
            'username': 'user1',
            'password1': 'pass1',
            'password2': 'pass1'
        })

        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')




    def test_login_view_GET(self):

        response = self.client.get(self.login_url)

        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')

    def test_login_view_POST(self):

        # Create User
        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        p = User.objects.create_user(**credentials)


        # When wrong username and password is given, user is
        # again rendered to login page and error message is shown
        credentials = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, credentials, follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(response.context['user'].is_authenticated)


        # When correct username and password is given,
        # userdetail page is rendered on successful login
        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        response = self.client.post(self.login_url, credentials,follow=True)
        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/userdetail.html')
        self.assertTrue(response.context['user'].is_authenticated)

        del p

    def test_userdetail_view(self):

        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }

        #Creating User for testing
        p = User.objects.create_user(**credentials)

        #Extracting the url of userdetail
        url = reverse(userdetail, args=[p.id, 'None'])

        #First Test-Case when user is not logged in it is redirected internally to the login page
        response = self.client.post(url, credentials,follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')


        #Second Test-Case when the user logs in tries to fetch UserDetail
        self.client.post(self.login_url, credentials, follow=True)
        response  = self.client.post(url,credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/userdetail.html')

        #Third Test-Case when logged in user tries to fetch other user's detail fetch ;
        # it is redirected to its own page userdetailpage
        #Create another user
        q = User.objects.create_user({'username':'anotheruser','password':'pass1'})
        url = reverse(userdetail, args=[45, 'None'])
        response = self.client.post(url, credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/userdetail.html')
        self.assertTrue(response.context['user'].id == p.id)

        del p
        del q



    def test_logout_view(self):
        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }

        # Creating User for testing
        p = User.objects.create_user(**credentials)

        # First Test-Case when user is not logged in it is redirected internally to the login page
        response = self.client.post(self.logout_url, credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Second Test-Case when the user logs in tries to logout it is redirected to homepage
        self.client.post(self.login_url, credentials, follow=True)
        response = self.client.post(self.logout_url, credentials,follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')

        del p







