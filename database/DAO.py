from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStore():

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris=[]

        query=""" select *
                  from stores s """

        cursor.execute(query)
        for row in cursor:
            ris.append( Store(**row) )

        cursor.close()
        conn.close()
        return ris

    @staticmethod
    def getAllNodes(storeId):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris = []

        query = """ select *
                    from orders o 
                    where o.store_id = %s"""

        cursor.execute(query, (storeId, ))
        for row in cursor:
            ris.append(Order(**row))

        cursor.close()
        conn.close()
        return ris

    @staticmethod
    def getAllWeight( nodo1, nodo2):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris = []

        query = """ select sum(oi.quantity + oi2.quantity ) as totPeso
                    from order_items oi, order_items oi2 ,
                         (select *
                         from orders o 
                         where o.order_id = %s) as a ,
                         (select *
                         from orders o 
                         where o.order_id = %s) as b 
                         where oi.order_id = a.order_id
                         and oi2.order_id = b.order_id"""

        cursor.execute(query, (nodo1, nodo2))
        for row in cursor:
            ris.append( row["totPeso"] )

        cursor.close()
        conn.close()
        return ris
