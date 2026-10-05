from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from .forms import InstrumentoForm
from .models import Instrumentos


class InstrumentoFormTests(TestCase):
	"""Comprueba que el formulario rechace datos incompletos o fuera de rango."""

	def datos_validos(self, **cambios):
		# Prepara datos válidos y permite cambiar un campo para cada prueba.
		datos = {
			'nombre': 'Guitarra electrica',
			'tipo': 'cuerda',
			'marca': 'fender',
			'cantidad': 100,
			'precio': 99999,
		}
		datos.update(cambios)
		return datos

	def test_acepta_limites_maximos(self):
		# Acepta la cantidad y el precio máximos permitidos.
		form = InstrumentoForm(data=self.datos_validos())

		self.assertTrue(form.is_valid())

	def test_rechaza_tipo_y_marca_vacios(self):
		# Exige seleccionar el tipo y la marca del instrumento.
		form = InstrumentoForm(data=self.datos_validos(tipo='', marca=''))

		self.assertFalse(form.is_valid())
		self.assertIn('tipo', form.errors)
		self.assertIn('marca', form.errors)

	def test_rechaza_nombre_mayor_de_25_caracteres(self):
		# Impide ingresar un nombre más largo que el permitido por el modelo.
		form = InstrumentoForm(data=self.datos_validos(nombre='a' * 26))

		self.assertFalse(form.is_valid())
		self.assertIn('nombre', form.errors)

	def test_rechaza_cantidad_mayor_de_100(self):
		# Rechaza cantidades superiores al máximo definido.
		form = InstrumentoForm(data=self.datos_validos(cantidad=101))

		self.assertFalse(form.is_valid())
		self.assertIn('cantidad', form.errors)

	def test_rechaza_cantidad_cero(self):
		# Impide guardar instrumentos sin unidades disponibles.
		form = InstrumentoForm(data=self.datos_validos(cantidad=0))

		self.assertFalse(form.is_valid())
		self.assertIn('cantidad', form.errors)

	def test_rechaza_precio_mayor_de_999999(self):
		# Rechaza precios que superan el máximo permitido.
		form = InstrumentoForm(data=self.datos_validos(precio=1000000))

		self.assertFalse(form.is_valid())
		self.assertIn('precio', form.errors)


class AuthenticationAndCrudTests(TestCase):
	def setUp(self):
		# Crea un usuario para probar las rutas que requieren autenticación.
		self.user = get_user_model().objects.create_user(
			username='musicuser',
			password='SafePassword123!',
		)

	def datos_instrumento(self, **cambios):
		# Devuelve datos válidos para enviar a las vistas del CRUD.
		datos = {
			'nombre': 'Guitarra electrica',
			'tipo': 'cuerda',
			'marca': 'fender',
			'cantidad': 10,
			'precio': 50000,
		}
		datos.update(cambios)
		return datos

	def test_catalogo_y_crud_requieren_sesion(self):
		# Comprueba que todas las rutas protegidas redirijan al login.
		for path in (
			'/inicio/',
			'/agregar/',
			'/editar/1/',
			'/eliminar/1/',
		):
			with self.subTest(path=path):
				self.assertRedirects(
					self.client.get(path),
					f'/?next={path}',
				)

	def test_login_api_inicia_sesion_y_entrega_token(self):
		# Verifica que el login abra una sesión y devuelva un token válido.
		response = self.client.post('/api/login/', {
			'username': 'musicuser',
			'password': 'SafePassword123!',
		})

		self.assertEqual(response.status_code, 200)
		self.assertIn('token', response.json())
		catalogo = self.client.get('/inicio/')
		self.assertEqual(catalogo.status_code, 200)
		self.assertContains(catalogo, 'Cerrar sesión')

	def test_logout_cierra_sesion_y_vuelve_a_proteger_catalogo(self):
		# Comprueba que el logout invalide sesión y token de API.
		self.client.force_login(self.user)
		Token.objects.get_or_create(user=self.user)

		response = self.client.post('/cerrar-sesion/')

		self.assertRedirects(response, '/')
		self.assertFalse(Token.objects.filter(user=self.user).exists())
		self.assertRedirects(self.client.get('/inicio/'), '/?next=/inicio/')

	def test_crud_persiste_creacion_edicion_y_eliminacion(self):
		# Verifica que crear, editar y eliminar persistan en la base de pruebas.
		self.client.force_login(self.user)

		create_response = self.client.post('/agregar/', self.datos_instrumento())
		instrumento = Instrumentos.objects.get(nombre='Guitarra electrica')
		self.assertRedirects(create_response, '/inicio/')

		update_response = self.client.post(
			f'/editar/{instrumento.id}/',
			self.datos_instrumento(nombre='Guitarra acustica'),
		)
		instrumento.refresh_from_db()
		self.assertEqual(instrumento.nombre, 'Guitarra acustica')
		self.assertRedirects(update_response, '/inicio/')

		delete_response = self.client.post(f'/eliminar/{instrumento.id}/')
		self.assertFalse(Instrumentos.objects.filter(id=instrumento.id).exists())
		self.assertRedirects(delete_response, '/inicio/')

	def test_login_api_informa_campos_obligatorios_en_espanol(self):
		# Informa en español cuando no se envían las credenciales requeridas.
		response = self.client.post('/api/login/', {})

		self.assertEqual(response.status_code, 400)
		self.assertEqual(
			response.json()['mensaje'],
			'Debes ingresar un nombre de usuario.',
		)

	def test_login_api_rechaza_credenciales_incorrectas(self):
		# Rechaza la contraseña incorrecta con un error de autenticación.
		response = self.client.post('/api/login/', {
			'username': 'musicuser',
			'password': 'wrong-password',
		})

		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.json()['mensaje'], 'Credenciales inválidas')
