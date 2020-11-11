from saleapp import admin, db
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product
from flask_admin import BaseView, expose


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ContactView(name='Liên hệ'))