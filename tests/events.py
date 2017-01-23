# from nose.tools import ok_, eq_, raises, assert_raises
# from . import BaseTest, Car, Model, var, mod#, AllVars
# from dstore import MemoryStore
# from dstore.Error import EventNotFound, EventListenerNotFound, InstanceNotFound
#
#
# class EventTest( BaseTest ):
#     auto_create = False
#     auto_init   = False
#
#     def before_action( self, event ):
#         self.before = True
#
#     def after_action( self, event ):
#         self.after = True
#
#
# class UnknownEvent( EventTest ):
#     def test( self ):
#         self.store = MemoryStore(self.models)
#
#         with assert_raises( EventNotFound ):
#             self.store.events.before_something += self.before_action
#
#
# class UnknownListener( BaseTest ):
#     def listener( self, event ):
#         pass
#
#     def test( self ):
#         with assert_raises( EventListenerNotFound ):
#             Car.events.before_add -= self.listener
#
#
# class RemoveListener( EventTest ):
#     def listener( self, event ):
#         self.action = True
#
#     def test( self ):
#         self.action = False
#         self.store = MemoryStore( self.models )
#
#         self.store.events.before_init_app += self.listener
#         self.store.events.before_init_app -= self.listener
#
#         self.store.init_app()
#
#         eq_( self.action, False, "before_init_app was executed" )
#
#
# class InitApp( EventTest ):
#     def test( self ):
#         self.store = MemoryStore( self.models )
#         self.store.events.before_init_app += self.before_action
#         self.store.events.after_init_app  += self.after_action
#
#         self.store.init_app()
#
#         eq_( self.before, True, "before_init_app was not executed" )
#         eq_( self.after, True, "after_init_app was not executed" )
#
#
# class DestroyApp( EventTest ):
#     def test( self ):
#         self.store = MemoryStore( self.models )
#         self.store.events.before_destroy_app += self.before_action
#         self.store.events.after_destroy_app  += self.after_action
#
#         self.store.init_app()
#         self.store.destroy_app()
#
#         eq_( self.before, True, "before_destroy_app was not executed" )
#         eq_( self.after, True, "after_destroy_app was not executed" )
#
#
# class RegisterModels(EventTest):
#     def test(self):
#         self.store = MemoryStore(self.models)
#         self.store.events.before_register_models += self.before_action
#         self.store.events.after_register_models  += self.after_action
#
#         self.store.init_app()
#         self.store.destroy_app()
#
#         eq_(self.before, True, "before_register_models was not executed")
#         eq_(self.after, True, "after_register_models was not executed")
#
#
# class RegisterModel( EventTest ):
#     def before_action( self, event, model ):
#         self.before = model
#
#     def after_action( self, event, model ):
#         self.after = model
#
#     def test(self):
#         self.store = MemoryStore(self.models)
#         self.store.events.before_register_model += self.before_action
#         self.store.events.after_register_model += self.after_action
#
#         self.store.init_app()
#         self.store.destroy_app()
#
#         eq_( issubclass( self.before, Model ), True, "before_register_model was not executed")
#         eq_( issubclass( self.after, Model ), True, "after_register_model was not executed")
#
#
# class CancelAdd( BaseTest ):
#     def before_addd( self, event, model, instance ):
#         self.action = True
#         event.cancel()
#
#     def test( self ):
#         Car.events.before_add += self.before_addd
#         Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
#         Car.events.before_add -= self.before_addd
#
#         with assert_raises( InstanceNotFound ):
#             Car.get( 1 )
#
#         eq_( self.action, True, "before_add was not executed" )
#
#
# class Add( BaseTest ):
#     def before_action( self, event, model, instance ):
#         self.before = ( model, instance )
#
#     def after_action( self, event, model, instance ):
#         self.after = ( model, instance )
#
#     def test(self):
#         Car.events.before_add += self.before_action
#         Car.events.after_add += self.after_action
#
#         Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
#
#         eq_( issubclass( self.before[0], Car ), True, "before_add was not executed (Model != Car)")
#         eq_( isinstance( self.before[1], Car ), True, "before_add was not executed (Instance not a Car)")
#         eq_( issubclass( self.after[0], Car ), True, "after_add was not executed (Model != Car)")
#         eq_( isinstance( self.after[1], Car ), True, "after_add was not executed (Instance not a Car)")
#
#
# class Delete( BaseTest ):
#     def before_action( self, event, model, instance ):
#         self.before = ( model, instance )
#
#     def after_action( self, event, model, instance ):
#         self.after = ( model, instance )
#
#     def test(self):
#         Car.events.before_delete += self.before_action
#         Car.events.after_delete  += self.after_action
#
#         car = Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
#         car.delete()
#
#         eq_( issubclass( self.before[0], Car ), True, "before_delete was not executed (Model != Car)")
#         eq_( isinstance( self.before[1], Car ), True, "before_delete was not executed (Instance not a Car)")
#         eq_( issubclass( self.after[0], Car ), True, "after_delete was not executed (Model != Car)")
#         eq_( isinstance( self.after[1], Car ), True, "after_delete was not executed (Instance not a Car)")
#
#
# class Update( BaseTest ):
#     def before_action( self, event, model, instance ):
#         self.before = ( model, instance )
#
#     def after_action( self, event, model, instance ):
#         self.after = ( model, instance )
#
#     def test(self):
#         Car.events.before_update += self.before_action
#         Car.events.after_update  += self.after_action
#
#         car = Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
#         car.year = 2016
#         car.update()
#
#         eq_( issubclass( self.before[0], Car ), True, "before_update was not executed (Model != Car)")
#         eq_( isinstance( self.before[1], Car ), True, "before_update was not executed (Instance not a Car)")
#         eq_( issubclass( self.after[0], Car ), True, "after_update was not executed (Model != Car)")
#         eq_( isinstance( self.after[1], Car ), True, "after_update was not executed (Instance not a Car)")
#
#
# class All( BaseTest ):
#     def before_action( self, event, model ):
#         self.before = model
#
#     def after_action( self, event, model, instances ):
#         self.after = ( model, instances )
#
#     def test( self ):
#         Car.events.before_all += self.before_action
#         Car.events.after_all += self.after_action
#
#         Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
#         Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
#         Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
#         Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
#
#         Car.all()
#
#         eq_( issubclass( self.before, Car ), True, "before_all was not executed (Model != Car)" )
#         eq_( issubclass( self.after[0], Car ), True, "after_all was not execute (Model != Car)" )
#         eq_( isinstance( self.after[1], list ), True, "after_all was not execute (Instance != List)" )
#         eq_( isinstance( self.after[1][0], Car), True, "after_all was not execute (Instance[0] != Car)" )
#
#
# class Get( BaseTest ):
#     def before_action( self, event, model, row_id ):
#         self.before = ( model, row_id )
#
#     def after_action( self, event, model, instance ):
#         self.after = ( model, instance )
#
#     def test( self ):
#         Car.events.before_get += self.before_action
#         Car.events.after_get += self.after_action
#
#         Car(manufacturer="Holden", make="Commodore", year=2005).add()
#         Car(manufacturer="Holden", make="Commodore", year=2006).add()
#
#         Car.get( 1 )
#
#         eq_( issubclass( self.before[0], Car ), True, "before_get was not execute (Model != Car)" )
#         eq_( self.before[1], 1, "before_get was not execute (row_id != 1)" )
#         eq_( issubclass( self.after[0], Car ), True, "after_get was not executed (Model != Car)" )
#         eq_( isinstance( self.after[1], Car ), True, "after_get was not execute (Instance != Car)" )
#         eq_( self.after[1].year, 2005, "after_get was not execute (Instance.year  %d != 2005)" % self.after[1].year )
#
#
# class Empty( BaseTest ):
#     def before_action( self, event, model ):
#         self.before = model
#
#     def after_action( self, event, model ):
#         self.after = model
#
#     def test( self ):
#         Car.events.before_empty += self.before_action
#         Car.events.after_empty += self.after_action
#
#         Car(manufacturer="Holden", make="Commodore", year=2005).add()
#         Car(manufacturer="Holden", make="Commodore", year=2006).add()
#
#         Car.empty()
#
#         eq_( issubclass( self.before, Car ), True, "before_empty was not executed (Model != Car)" )
#         eq_( issubclass( self.after, Car ), True, "after_empty was not execute (Model != Car)" )
#
#
# class Create( BaseTest ):
#     auto_create = False
#
#     def before_action( self, event, model ):
#         self.before = model
#
#     def after_action( self, event, model ):
#         self.after = model
#
#     def test( self ):
#         Car.events.before_create += self.before_action
#         Car.events.after_create += self.after_action
#
#         Car.create()
#         Car.destroy()
#
#         eq_( issubclass( self.before, Car), True, "before_create was not execute (Model != Car)" )
#         eq_( issubclass( self.after, Car ), True, "after_create was not execute (Model != Car" )
#
#
# class Destroy( BaseTest ):
#     auto_create = False
#
#     def before_action( self, event, model ):
#         self.before = model
#
#     def after_action( self, event, model ):
#         self.after = model
#
#     def test( self ):
#         Car.events.before_destroy += self.before_action
#         Car.events.after_destroy += self.after_action
#
#         Car.create()
#         Car.destroy()
#
#         eq_( issubclass( self.before, Car ), True, "before_destroy was not execute (Model != Car)" )
#         eq_( issubclass( self.after, Car ), True, "after_destroy was not execute (Model != Car" )
#
#
# class Filter( BaseTest ):
#     def before_action( self, event, model, params ):
#         self.before = ( model, params )
#
#     def after_action( self, event, model, instances, params ):
#         self.after = ( model, instances, params )
#
#     def test( self ):
#         Car.events.before_filter += self.before_action
#         Car.events.after_filter += self.after_action
#
#         Car(manufacturer="Holden", make="Commodore", year=2005).add()
#         Car(manufacturer="Holden", make="Commodore", year=2006).add()
#         Car(manufacturer="Holden", make="Rodeo", year=2007).add()
#         Car(manufacturer="Holden", make="Colorado", year=2008).add()
#
#         cars = Car.filter( make = "Commodore" )
#
#         eq_( issubclass( self.before[0], Car ), True, "before_filter was not executed (Model != Car)" )
#         eq_( isinstance( self.before[1], dict ), True, "before_filter was not executed (Params != Dict)" )
#         eq_( self.before[1][ "make" ], "Commodore", "before_filter was not executed (Params['make'] != 'Commodore'" )
#         eq_( issubclass( self.after[0], Car ), True, "after_filter was not executed (Model != Car)" )
#         eq_( isinstance( self.after[1], list ), True, "after_filter was not executed (Instances != List)" )
#         eq_( isinstance( self.after[1][0], Car ), True, "after_filter was not executed (Instances[0] != Car)" )
#         eq_( isinstance( self.after[2], dict ), True, "after_filter was not executed (Params != Dict)" )
#         eq_( self.after[2][ "make" ], "Commodore", "after_filter was not executed (Params['make'] != 'Commodore'" )
#
#
# class CreateAll( BaseTest ):
#     auto_create = False
#
#     def before_action( self, event ):
#         self.before = True
#
#     def after_action( self, event ):
#         self.after = True
#
#     def test( self ):
#         self.store.events.before_create_all += self.before_action
#         self.store.events.after_create_all += self.after_action
#
#         self.store.create_all()
#         self.store.destroy_all()
#
#         eq_( self.before, True, "before_create_all was not executed" )
#         eq_( self.after, True, "after_create_all was not executed" )
#
#
# class DestroyAll( BaseTest ):
#     auto_create = False
#
#     def before_action( self, event ):
#         self.before = True
#
#     def after_action( self, event ):
#         self.after = True
#
#     def test( self ):
#         self.store.events.before_destroy_all += self.before_action
#         self.store.events.after_destroy_all += self.after_action
#
#         self.store.create_all()
#         self.store.destroy_all()
#
#         eq_( self.before, True, "before_destroy_all was not executed" )
#         eq_( self.after, True, "after_destroy_all was not executed" )
#
#
# class EmptyAll( BaseTest ):
#     def before_action( self, event ):
#         self.before = True
#
#     def after_action( self, event ):
#         self.after = True
#
#     def test( self ):
#         self.store.events.before_empty_all += self.before_action
#         self.store.events.after_empty_all += self.after_action
#
#         Car(manufacturer="Holden", make="Commodore", year=2005).add()
#         Car(manufacturer="Holden", make="Commodore", year=2006).add()
#         Car(manufacturer="Holden", make="Rodeo", year=2007).add()
#         Car(manufacturer="Holden", make="Colorado", year=2008).add()
#
#         self.store.empty_all()
#
#         eq_( self.before, True, "before_empty_all was not executed" )
#         eq_( self.after, True, "after_empty_all was not executed" )
#
#
# class Validate( BaseTest ):
#     def before_action( self, event, model, instance ):
#         self.before = ( model, instance )
#
#     def after_action( self, event, model, instance ):
#         self.after = ( model, instance )
#
#     def test( self ):
#         Car.events.before_validate += self.before_action
#         Car.events.after_validate += self.after_action
#
#         Car(manufacturer="Holden", make="Commodore", year=2005).add()
#
#         eq_( issubclass( self.before[0], Car ), True, "before_validate was not executed (Model != Car)" )
#         eq_( isinstance( self.before[1], Car ), True, "before_validate was not executed (Instance != Car)" )
#         eq_( issubclass( self.after[0], Car ), True, "after_validate was not executed (Model != Car)" )
#         eq_( isinstance( self.after[1], Car ), True, "after_validate was not executed (Instance != Car)" )
#
#
# class Connect( BaseTest ):
#     auto_init = False
#     auto_create = False
#
#     def before_action( self, event, store ):
#         self.before = store
#
#     def after_action( self, event, store ):
#         self.after = store
#
#     def test( self ):
#         self.store = MemoryStore(self.models)
#         self.store.events.before_connect = self.before_action
#         self.store.events.after_connect = self.after_action
#
#         self.store.init_app()
#         self.store.connect()
#
#         eq_( self.before, self.store, "before_connect was not executed" )
#         eq_( self.after, self.store, "after_connect was not executed" )
#
#
# class Disconnect( BaseTest ):
#     auto_init = False
#     auto_create = False
#
#     def before_action( self, event, store ):
#         self.before = store
#
#     def after_action( self, event, store ):
#         self.after = store
#
#     def test( self ):
#         self.store = MemoryStore( self.models )
#         self.store.events.before_disconnect = self.before_action
#         self.store.events.after_disconnect = self.after_action
#
#         self.store.init_app()
#         self.store.connect()
#         self.store.disconnect()
#
#         eq_(self.before, self.store, "before_disconnect was not executed")
#         eq_(self.after, self.store, "after_disconnect was not executed")
