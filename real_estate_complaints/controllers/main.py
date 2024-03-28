# Asegúrate de importar las dependencias necesarias al inicio de tu archivo de controlador.
from odoo import http
from odoo.http import request

class ComplaintController(http.Controller):
    # @http.route('/complaint', type='http', auth="public", website=True)
    # def complaint(self, **post):
    #     if post:
    #         request.env['real.estate.complaint'].sudo().create(post)
    #         return request.redirect('/complaint/thank_you')
    #     return request.render("real_estate_complaints.complaint_form_template")

    @http.route('/complaint/thank_you', type='http', auth="public", website=True)
    def thank_you(self, **post):
        return request.render("real_estate_complaints.thank_you_template")

    @http.route('/complaint', type='http', auth="public", website=True)
    def complaint(self, **post):
        if post:
            # Ejemplo de validación básica
            if not post.get('name') or not post.get('email'):
                # Redirige a una página de error o muestra un mensaje de validación
                return request.render("real_estate_complaints.error_template", {'error': 'Datos inválidos'})

            # Sanitizar los datos aquí si es necesario

            # Crear la queja
            request.env['real.estate.complaint'].sudo().create(post)
            return request.redirect('/complaint/thank_you')
        return request.render("real_estate_complaints.complaint_form_template")
