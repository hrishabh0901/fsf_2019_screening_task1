from django.test import TestCase,Client,SimpleTestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User
from .views import createteam,teamdetail
from accounts.views import login
from .models import Team

# Create your tests here.
class TestUrls(SimpleTestCase):

    def test_createteam_url(self):
        url = reverse(createteam)
        self.assertEqual(resolve(url).func,createteam)

    def test_taskdetail_url(self):
        url = reverse(teamdetail,args=[1])
        self.assertEqual(resolve(url).func,teamdetail)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.createteam_url = reverse(createteam)
        self.teamdetail_url = reverse(teamdetail,args=[1])
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        self.testuser = User.objects.create_user(**self.credentials)
        self.team_credential = {
            'team_name':'testteam',
            'creator':self.testuser,
            'members':['testuser']
        }
        self.testteam = Team.objects.create(**self.team_credential)






    def test_createteam_view_GET(self):


        #When no User is Loggedin , it redirects to LoginPage
        response = self.client.get(self.createteam_url,follow=True)
        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')

        #When a Loggedin User fetches the Createteam and it is not part of any team,
        # createteam.html is rendered
        # user logs in
        self.client.login(**self.credentials)
        response = self.client.get(self.createteam_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'team/createteam.html')
        self.client.logout()

        # # When a Loggedin User fetches the Createteam and it is  part of a team,
        # # It is redirected to it's userdetail page
        # self.client.login(**self.credentials)
        # response = self.client.get(self.createteam_url)
        # self.assertEqual(response.status_code,200)
        # self.assertTemplateUsed(response,'accounts/userdetail.html')
        # self.client.logout()


    def test_createteam_view_POST(self):

        # creating a another testuser
        credentials = {
            'username': 'anothertestuser',
            'password': 'secret'
        }
        anothertestuser = User.objects.create_user(**credentials)

        #creating a another team
        anotherteam_credential = {
            'team_name': 'testteam',
            'members': []
        }


        #Creating a team with Existing TeamName,
        # again renders you with createteam.html
        #the user must be loggedin
        self.client.login(**self.credentials)
        response = self.client.post(self.createteam_url,**anotherteam_credential)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/createteam.html')
        self.client.logout()

        # Creating a team with a new TeamName,
        # renders you with teamdetail.html
        # the user must be loggedin
        self.client.login(**credentials)
        anotherteam_credential['team_name'] = 'anothertestteam'
        response = self.client.post(self.createteam_url, **anotherteam_credential)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/createteam.html')
        self.client.logout()

    def test_teamdetail_view_GET(self):

        # When no User is Loggedin , it redirects to LoginPage
        response = self.client.get(self.teamdetail_url, follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # When User is Loggedin ,
        # it redirects to 404 not found team does not exist
        self.client.login(**self.credentials)
        response = self.client.get(reverse(teamdetail,args=[10]), follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 404)
        self.client.logout()


        # When User is Loggedin ,
        # it redirects to teamdetail if team.id exists
        self.client.login(**self.credentials)
        response = self.client.get(reverse(teamdetail,args=[self.testteam.id]))
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/teamdetail.html')
        self.client.logout()

















