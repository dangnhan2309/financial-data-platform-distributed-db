class Shipment(Base):
    __tablename__ = "shipment"
    shipment_id = Column(String(50), primary_key=True)
    transport_route_id = Column(String(50), ForeignKey("transport_route.route_id"))
    carrier_id = Column(String(50)) # Có thể tạo thêm bảng Carrier nếu cần
    vehicle_id = Column(String(50))
    departure_time = Column(DateTime)
    estimated_arrival_time = Column(DateTime)
    actual_arrival_time = Column(DateTime)
    status = Column(String(20))