from django.test import TestCase

from .forms import InstrumentoForm


class InstrumentoFormTests(TestCase):
	"""Comprueba que el formulario rechace datos incompletos o fuera de rango."""

	def datos_validos(self, **cambios):
		datos = {
			'nombre': 'Guitarra electrica',
			'tipo': 'cuerda',
			'marca': 'fender',
			'cantidad': 100,
			'precio': 60000,
		}
		datos.update(cambios)
		return datos

	def test_acepta_limites_maximos(self):
		form = InstrumentoForm(data=self.datos_validos())

		self.assertTrue(form.is_valid())

	def test_rechaza_tipo_y_marca_vacios(self):
		form = InstrumentoForm(data=self.datos_validos(tipo='', marca=''))

		self.assertFalse(form.is_valid())
		self.assertIn('tipo', form.errors)
		self.assertIn('marca', form.errors)

	def test_rechaza_nombre_mayor_de_50_caracteres(self):
		form = InstrumentoForm(data=self.datos_validos(nombre='a' * 26))

		self.assertFalse(form.is_valid())
		self.assertIn('nombre', form.errors)

	def test_rechaza_cantidad_mayor_de_2000(self):
		form = InstrumentoForm(data=self.datos_validos(cantidad=101))

		self.assertFalse(form.is_valid())
		self.assertIn('cantidad', form.errors)

	def test_rechaza_cantidad_cero(self):
		form = InstrumentoForm(data=self.datos_validos(cantidad=0))

		self.assertFalse(form.is_valid())
		self.assertIn('cantidad', form.errors)

	def test_rechaza_precio_mayor_de_sesentamil(self):
		form = InstrumentoForm(data=self.datos_validos(precio=60000))

		self.assertFalse(form.is_valid())
		self.assertIn('precio', form.errors)
