from locust import HttpUser, task, constant

class UsuarioBusqueda(HttpUser):
    host = "http://localhost:5000" 

    @task(3)
    def busqueda_valida(self):
        self.client.get("/?q=cierre")

    @task(1)
    def busqueda_invalida(self):
        self.client.get("/?q=xyz_inexistente")
