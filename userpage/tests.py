from django.test import TestCase,Client
from django.utils import timezone
from adminpage.views import activityCheckin,activityCreate,activityDelete,activityDetail,activityList,activityMenu,adminLogin,adminLogout
from codex.baseerror import ValidateError
import json
from wechat.models import Activity,Ticket,User
import datetime
from userpage.views import UserBind, UserActivityDetail, TicketDetail


# Create your tests here.

#学号绑定
class bindTest(TestCase):
    #初始化
    def setUp(self):
        User.objects.create(open_id='id1', student_id='2016012072')
        User.objects.create(open_id='id2',student_id='')
        User.objects.create(open_id='id3',student_id='')
    
    #获取当前用户的学号绑定状态
    def test_usertest_get(self):
        c = Client()
        response = c.get('/api/u/user/bind/?',{"openid":"id1"})
        self.assertEqual(response.json()['data'],"2016012072")

    #未绑定用户的测试
    def test_usertest_get_none(self):
        c = Client()
        response = c.get('/api/u/user/bind/?',{"openid":"id2"})
        self.assertEqual(response.json()['data'],"")


    #将当前用户绑定至指定学号
    def test_usertest_post(self):
        User_bind = UserBind()
        User_bind.input = {
            'openid':'id2',
            'student_id':'2016010000',
            'password':'123456test'
        }
        User_bind.post()
        self.assertEqual(User.get_by_openid('id2').student_id, '2016010000')

    #对已绑定的用户进行重复绑定
    def test_usertest_post_wrong_studentid(self):
        User_bind = UserBind()
        User_bind.input = {
            'openid':'id2',
            'student_id':'2016010002',
            'password':'123456test'
        }
        User_bind.post()
        self.assertEqual(User.get_by_openid('id2').student_id, '2016010002')


#活动详情
class activityTest(TestCase):

    #初始化
    def setUp(self):
        Activity.objects.create(id=1, name='act_deleted', key='key1', place='place',
                                description='description', start_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 8, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 18, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.make_aware(datetime.datetime(2018, 10, 27, 18, 0, 0, 0)),
                                total_tickets=1000, status=Activity.STATUS_PUBLISHED, remain_tickets=1000)
        Activity.objects.create(id=2, name='act_saved', key='key2', place='place',
                                description='description', start_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 8, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 18, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.make_aware(datetime.datetime(2018, 10, 27, 18, 0, 0, 0)),
                                total_tickets=1000, status=Activity.STATUS_SAVED, remain_tickets=1000)

    #获取活动的详情
    def test_usertest1(self):
        Activity_Detail = UserActivityDetail()
        Activity_Detail.input = {
            'id':1
        }
        activity_test = Activity_Detail.get()
        self.assertEqual(activity_test['name'],"act_deleted")

    #获取未发布的活动信息
    def test_usertest2(self):
        Activity_Detail = UserActivityDetail()
        Activity_Detail.input = {
            'id':2
        }
        self.assertRaises(ValidateError, Activity_Detail.get)


#电子票详情
class detailTest(TestCase):

    #初始化
    def setUp(self):
        act = Activity.objects.create(id=1, name='act_saved', key='key1', place='place',
                                description='description', start_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 8, 0, 0, 0)), pic_url="url",
                                end_time=timezone.make_aware(datetime.datetime(2018, 10, 28, 18, 0, 0, 0)), book_start=timezone.now(), book_end=timezone.make_aware(datetime.datetime(2018, 10, 27, 18, 0, 0, 0)),
                                total_tickets=1000, status=1, remain_tickets=1000)
        User.objects.create(open_id='id1',student_id='2016012072')
        User.objects.create(open_id='id2',student_id='2016012000')
        User.objects.create(open_id='id3',student_id='2016012001')
        Ticket.objects.create(student_id="2016012072",unique_id='1',activity=act, status=1)

    #获取电子票的详情
    def test_usertest1(self):
        Ticket_Detail = TicketDetail()
        Ticket_Detail.input = {
            'openid':'id1',
            'ticket':'1'
        }
        ticket_test = Ticket_Detail.get()
        self.assertEqual(ticket_test['activityName'],"act_saved")

