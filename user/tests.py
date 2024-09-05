import email
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from insertion.models import Insertion
from user.models import CustomUser


#Unit Test on UserSignup.validate_phone
#Test if the phone number is valid only if starts with '+' or '0'
class UserSignupTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_valid(self):
        response = self.client.post('/signup', {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testemail@test.com',
            'birth_date': '2000-01-01',
            'phone': '+393331234567',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'role': 'GUEST'
        })

        # Controllo se l'utente è stato creato
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
    
    def test_signup_invalid(self):
        response = self.client.post('/signup', {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testemail@test.com',
            'birth_date': '2000-01-01',
            'phone': '3331234567',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'role': 'GUEST'
        })

        # Controllo se l'utente è stato creato
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

class UserInsertionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.utente = CustomUser.objects.create_user(username='testuser', 
                                                first_name='Test', 
                                                last_name='User', 
                                                email='testemail@test.com', 
                                                birth_date='2000-01-01', 
                                                phone='+393331234567', 
                                                password='TestPassword123!', 
                                                role='HOST')
        
        self.insertion = Insertion.objects.create(host=self.utente, 
                                                  title='Test', 
                                                  description='Test', 
                                                  latitude=0,
                                                  longitude=0,
                                                  max_guests=1,
                                                  services=[1, 2, 3],
                                                  bathrooms=1,
                                                  bedrooms=1,
                                                  king_beds=1,
                                                  single_beds=1,
                                                  is_active=True,
                                                  rules='Test',
                                                  cover_image='covers/default.jpg',
                                                  metadata={})
        
        self.insertions = Insertion.objects.filter(host=self.utente)
        

    def test_insertion_valid(self):
        # Login utente
        self.client.login(username='testuser', password='TestPassword123!')
        # Visita della pagina con tutte le inserzioni
        response = self.client.get(reverse_lazy('user:myinsertions'))
        # Controllo se la pagina restituisce 200 e se l'inserzione è presente
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.insertion, response.context['insertions'])