from nose.tools import ok_, eq_, raises, assert_raises
from . import BaseTest, Car
from dstore.Error import InstanceNotFound


class Cars( BaseTest ):
    def test_car_add( self ):
        print( Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add() )

    def test_car_all( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        for car in Car.all():
            print( "\t%s" % car )

    def test_car_all_dict( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        for car in Car.all( to_dict = True ):
            print( "\t%s" % car )

    def test_update( self ):
        car = Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()

        car.year = 2016
        car.update()

    def test_get( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        car = Car.get( 3 )

        eq_( car.manufacturer, "Holden",    "Car.manufacturer != 'Holden'" )
        eq_( car.make,         "Commodore", "Car.make != 'Commodore'" )
        eq_( car.year,         2007,        "Car.year  %d != 2007" % car.year )

    def test_get_none( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()

        with assert_raises( InstanceNotFound ):
            Car.get( 3 )

    def test_delete( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        car = Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()

        car.delete()

    def test_filter( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        cars = Car.filter( make = "Commodore", year = None )

        num_cars = len( cars )
        eq_( num_cars, 3, "Number of cars %d != 3" % num_cars )

    def test_filter_1( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        car = Car.filter( make = "Rodeo" )[0]

        eq_( isinstance( car, Car ), True, "Didn't return a single instance" )

    def test_filter_none( self ):
        Car( manufacturer = "Holden", make = "Commodore", year =2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year =2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year =2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year =2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year =2009 ).add()

        with assert_raises( InstanceNotFound ):
            Car.filter( make = "Gummy" )

    def test_filter_like( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        cars = Car.filter( make = "Co%" )

        num_cars = len( cars )
        eq_( num_cars, 4, "Number of cars %d != 4" % num_cars )

