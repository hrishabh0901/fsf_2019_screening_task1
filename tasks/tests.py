from django.test import TestCase,Client,SimpleTestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User
from .views import createtask,taskdetail,task_edit,add_comment_to_task
from accounts.views import login
from .models import Task,Comment
from .forms import TaskForm,TaskForm1,CommentForm

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_createtask_url(self):
        url = reverse(createtask)
        self.assertEqual(resolve(url).func,createtask)

    def test_taskdetail_url(self):
        url = reverse(taskdetail,args=[1])
        self.assertEqual(resolve(url).func,taskdetail)

    def test_task_edit_url(self):
        url = reverse(task_edit, args=[1])
        self.assertEqual(resolve(url).func, task_edit)

    def test_add_comment_to_task_url(self):
        url = reverse(add_comment_to_task, args=[1])
        self.assertEqual(resolve(url).func, add_comment_to_task)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.createtask_url = reverse(createtask)
        self.taskdetail_url = reverse(taskdetail,args=[1])
        self.task_edit_url = reverse(task_edit,args=[1])
        self.add_comment_to_task_url = reverse(add_comment_to_task, args=[1])
        self.test_credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        self.testuser = User.objects.create_user(**self.test_credentials)

        # creating task
        self.task_credentials = {
            'title': 'testtask',
            'body': 'testbody',
            'status': 'Done',
            'assignee': self.testuser
        }
        self.test_task = Task.objects.create(**self.task_credentials)
        self.test_task.user_assgined.set([self.testuser])

    def test_createtask_view_GET(self):


        #When no User is Loggedin , it redirects to LoginPage
        response = self.client.get(self.createtask_url,follow=True)
        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')

        #When a Loggedin User fetches the Createtask
        # createtask.html is rendered
        # user logs in
        self.client.login(**self.test_credentials)
        response = self.client.get(self.createtask_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'tasks/createtask.html')
        self.client.logout()



    def test_createtask_view_POST(self):

        # Creating a Task by passing correct data redirects to
        # tasks/taskdetail.html after validation

        task_credentials = {
            'title':'testtask1',
            'body':'testbody',
            'status':'Done',
            'members':[self.testuser]
        }

        self.client.login(**self.test_credentials)
        response = self.client.post(self.createtask_url,data=task_credentials,follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/taskdetail.html')
        self.client.logout()



        # Creating a Task by passing incorrect data redirects to
        # tasks/createtask.html after validation of the data

        # changing to 'status' type which does not exist
        task_credentials['status']  = 'NoSuchStatusExist'
        self.client.login(**self.test_credentials)
        response = self.client.post(self.createtask_url, data=task_credentials)
        self.assertTemplateUsed(response, 'tasks/createtask.html')
        self.client.logout()

    def test_taskdetail(self):

        # If no such task exist it returns status code 404 not found
        # and the user should be loggedin
        self.client.login(**self.test_credentials)
        response = self.client.get(reverse(taskdetail,args=[12]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()


        # If the user is not assigned to view task , redirected to userdetail page
        # creating another user
        credential = {'username': 'testuser2', 'password': 'secret'}
        anothertestuser = User.objects.create_user(**credential)

        self.client.login(**credential)
        response = self.client.get(reverse(taskdetail, args=[self.test_task.id]),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/userdetail.html')
        self.client.logout()


        # If the user is assigned to view task , rendered to taskdetail page
        self.client.login(**self.test_credentials)
        response = self.client.get(reverse(taskdetail, args=[self.test_task.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/taskdetail.html')
        self.client.logout()






    def test_task_edit_GET(self):

        # If no user is loggedin , redirects to the loginpage
        response = self.client.get(self.task_edit_url,follow=True)
        #Asserrtions
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')


        # A loggedin user fetches tast_edit but the user is not the creator
        # of the task so the user will be rendered to the taskdetail.html

        #creating another user
        credential =  {'username': 'testuser1','password': 'secret'}
        anothertestuser = User.objects.create_user(**credential)


        self.client.login(**credential)
        response = self.client.get(reverse(task_edit,args=[self.test_task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/taskdetail.html')
        self.client.logout()


        # A loggedin user fetches task_edit and the user is  the creator
        # of the task so the user will be redirected to the edittask.html

        self.client.login(**self.test_credentials)
        response = self.client.get(reverse(task_edit, args=[self.test_task.id]),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/edittask.html')
        self.client.logout()

    def test_task_edit_POST(self):

        # After editing the user is redirected to taskdetail page

        self.client.login(**self.test_credentials)
        response = self.client.post(reverse(task_edit, args=[self.test_task.id]),
                                    data= self.task_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/taskdetail.html')
        self.client.logout()


    def test_add_comment_GET(self):

        # If no user is loggedin , redirects to the loginpage
        response = self.client.get(self.add_comment_to_task_url, follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')


        # If no task exist , status code 404 is returned
        self.client.login(**self.test_credentials)
        response = self.client.get(reverse(add_comment_to_task,args=[11]), follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 404)
        self.client.logout()


        # If the user is not assigned to view/comment on the
        # task so the user is redirected to user detail page

        # creating another user
        credential = {'username': 'testuser1', 'password': 'secret'}
        anothertestuser = User.objects.create_user(**credential)

        self.client.login(**credential)
        response = self.client.get(reverse(add_comment_to_task, args=[self.test_task.id]), follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/userdetail.html')
        self.client.logout()



        # If the user is  assigned to view/comment on the
        # task so the user is rendered the add_comment page

        self.client.login(**self.test_credentials)
        response = self.client.get(reverse(add_comment_to_task, args=[self.test_task.id]), follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/add_comment_to_task.html')
        self.client.logout()


    def test_add_comment_POST(self):

        # User login and membership test is already done above
        # now if commentform is valid then the user is redirected
        # to taskdetail page

        self.client.login(**self.test_credentials)
        response = self.client.post(reverse(add_comment_to_task, args=[self.test_task.id]),
                                    data={'text':'added comment'},follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/taskdetail.html')
        self.client.logout()



        # User login and membership test is already done above
        # now if commentform is not valid then the user is redirected
        # to add_comment_to_task page

        self.client.login(**self.test_credentials)
        response = self.client.post(reverse(add_comment_to_task, args=[self.test_task.id]),
                                    data={}, follow=True)
        # Asserrtions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'tasks/add_comment_to_task.html')
        self.client.logout()



class TestForms(TestCase):

    def setUp(self):
        self.client = Client()
        self.createtask_url = reverse(createtask)
        self.taskdetail_url = reverse(taskdetail,args=[1])
        self.task_edit_url = reverse(task_edit,args=[1])
        self.add_comment_to_task_url = reverse(add_comment_to_task, args=[1])
        self.test_credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        self.testuser = User.objects.create_user(**self.test_credentials)

    def test_TaskForm_form(self):
        form_data = {
            'title':'testtask1',
            'body':'testbody',
            'status':'Done',
            'members':[self.testuser]
        }
        form = TaskForm(self.testuser, data=form_data)
        self.assertTrue(form.is_valid())

    def test_TaskForm1_form(self):
        form_data = {
            'body':'testbody',
            'status':'Done',
        }
        form = TaskForm1(self.testuser, data=form_data)
        self.assertTrue(form.is_valid())

    def test_CommentForm_form(self):
        form_data = {
            'text':'text',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
