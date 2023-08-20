from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
from config import USER, PASSWORD, HOST, BD

db_url = f"mysql://{USER}:{PASSWORD}@{HOST}/{BD}"


# Crea una fábrica de sesiones

"""
def query_table_desnormalizada_orders_filters():
    
    create table table_denormalized_orders as 
    select ofi.city as Ciudad_Oficina,
        CONCAT(e.lastName,' ',e.firstName)as Empleado, e.jobTitle as Rol_Empleado,
        c.customerName as Cliente, c.city as Ciudad_Cliente,c.country as Pais_Cliente,
        o.orderDate as Fecha_Pedido,YEAR(o.orderDate) as Año_Pedido, MONTH(o.orderDate) as Mes_Pedido, DAY(o.orderDate) as Dia_Pedido,
        o.requiredDate as Fecha_Requerida ,o.shippedDate as Fecha_Envio,o.status as Estado_Pedido, 
        od.quantityOrdered as Cantidad_pedido, od.priceEach as Precio_Unitario,
        pro.productName as Producto, pro.productLine as Linea_Producto, pro.buyPrice as Precio_Compra_Producto
    from customers as c inner join employees as e on c.salesRepEmployeeNumber = e.employeeNumber 
                        inner join offices as ofi on e.officeCode = ofi.officeCode
                        inner join orders as o on c.customerNumber = o.customerNumber
                        inner join orderdetails as od on o.orderNumber = od.orderNumber
                        inner join products as pro on od.productCode = pro.productCode 
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text("select Año_Pedido, from table_denormalized_orders")
    results = session.execute(query)
    df = pd.DataFrame(results)
    df = df[['Año_Pedido',]]
    session.close()
    return results
"""
def sp_filtros():
    """
    SELECT DISTINCT Año_Pedido, Estado_Pedido FROM table_denormalized_orders;
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text(f"call filtros()")
    results = session.execute(query)
    df = pd.DataFrame(results)
    session.close()
    
    return [sorted(df['Año_Pedido'].unique()), 
            sorted(df['Estado_Pedido'].unique()),
            
        ]

def sp_empleado_cliente_totales( year = '2003', estado_pedido = 'Shipped'):
    """
    SELECT  Ciudad_Oficina,Empleado,Cliente,Ciudad_Cliente,
            SUM(Cantidad_pedido) as 'Número de Pedidos', 
            SUM(Cantidad_pedido + Precio_Unitario) as 'Importe Pedido'
    FROM table_denormalized_orders
    WHERE Año_Pedido = '2003' and Estado_Pedido != 'Shipped'
    GROUP BY Ciudad_Oficina,Empleado,Cliente,Ciudad_Cliente;
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text(f"call empleado_cliente_totales('{year}','{estado_pedido}')")
    results = session.execute(query)
    df = pd.DataFrame(results)
    session.close()
    return df

def sp_producto_total_pedido_importe( year = '2003', estado_pedido = 'Shipped'):
    """
    SELECT  Linea_Producto,Producto,
            SUM(Cantidad_pedido + Precio_Unitario) as 'Importe Pedido',
            SUM(Cantidad_pedido) as 'Número de Pedidos'
    FROM table_denormalized_orders
    WHERE Año_Pedido = '2003' and Estado_Pedido != 'Shipped'
    GROUP BY Linea_Producto,Producto
    ORDER BY SUM(Cantidad_pedido + Precio_Unitario) asc;
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text(f"call producto_total_pedido_importe('{year}','{estado_pedido}')")
    results = session.execute(query)
    df = pd.DataFrame(results)
    session.close()
    return df

def sp_pedidos_st_totales( year = '2003', estado_pedido = 'Shipped'):
    """
    SELECT  Fecha_Pedido, 
            SUM(Cantidad_pedido + Precio_Unitario) as 'Importe Pedido',
            SUM(Cantidad_pedido) as 'Número de Pedidos'
    FROM table_denormalized_orders
    WHERE Año_Pedido = '2004' and Estado_Pedido != 'Shipped'
    GROUP BY Fecha_Pedido
    ORDER BY Fecha_Pedido asc;
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text(f"call pedidos_st_totales('{year}','{estado_pedido}')")
    results = session.execute(query)
    df = pd.DataFrame(results)
    # Modifico el tipo de dato de Fecha_Pedido y creo la columna Mes_Pedido con Pandas
    df['Fecha_Pedido'] = pd.to_datetime(df['Fecha_Pedido'], format="%Y-%m-%d")
    df['Mes_num'] = df['Fecha_Pedido'].dt.month
    df['Mes_Pedido'] = pd.to_datetime(df['Fecha_Pedido'], format='%Y.%m.%d', errors="coerce").dt.month_name(locale='es_ES.utf8')
    session.close()
    return df

def sp_productos_precios( year = '2003', estado_pedido = 'Shipped'):
    """
    SELECT  Producto,Precio_Compra_Producto, Precio_Unitario, 
            (Precio_Unitario-Precio_Compra_Producto) as Ganancia
    FROM table_denormalized_orders
    WHERE Año_Pedido = '2004' and Estado_Pedido != 'Shipped'
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text(f"call productos_precios('{year}','{estado_pedido}')")
    results = session.execute(query)
    df = pd.DataFrame(results)
    session.close()
    return df
#def sp_linea_producto_empleado(campo_empleado = '', campo_linea_producto = ''):
#    query = text(f"call linea_producto_empleado('{campo_empleado}','{campo_linea_producto}')")
#    results = session.execute(query)
#    return results

