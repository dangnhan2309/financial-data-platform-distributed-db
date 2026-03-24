class DeliveryOrder(Base):
    __tablename__ = "delivery_order"
    do_id = Column(String(50), primary_key=True)
    sale_order_id = Column(String(50), ForeignKey("sale_order.sale_order_id"))
    shipment_id = Column(String(50), ForeignKey("shipment.shipment_id"))
    warehouse_id = Column(String(50)) # Tham chiếu đến kho bãi
    shipping_address = Column(String(500))
    total_weight = Column(Float)
    total_volume = Column(Float)
    status = Column(String(20))
    actual_delivery_date = Column(DateTime)