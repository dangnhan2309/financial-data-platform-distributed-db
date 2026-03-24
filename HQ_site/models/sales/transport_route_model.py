class TransportRoute(Base):
    __tablename__ = "transport_route"
    route_id = Column(String(50), primary_key=True)
    route_name = Column(String(255))
    origin_location = Column(String(255))
    destination_location = Column(String(255))
    distance_km = Column(Float)
    estimated_duration_hours = Column(Float)
    transit_points = Column(Text)
    status = Column(String(20))