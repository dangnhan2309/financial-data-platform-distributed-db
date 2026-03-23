import random
import uuid
import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import (
    Farm, FarmPlot, FarmBed,
    IotSensor, SensorData,
    Ingredient, Product, CultivationLog,
    WeighingTicket,
    Supplier, PurchaseContract, PurchaseBatch, PurchaseTicket,
    ProductionLot, QcRecord,
    Warehouse, Inventory, TransportTicket
)

def generate_id(prefix):
    return f"{prefix}-{str(uuid.uuid4())[:8]}"

def seed_data():
    db = SessionLocal()
    
    # Re-create tables to clean up old data
    print("Recreating database schema (Clean Start)...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("Seeding database with EXTENDED dataset (v2)...")

    # --- 1. FARM STRUCTURE (4 Zones, 20 Beds) ---
    print("- Creating Farm Structure...")
    farm = Farm(
        farm_id=generate_id("FARM"),
        farm_name="Green Valley Eco Farm",
        location="Dalat, Vietnam",
        created_at=datetime.datetime.now()
    )
    db.add(farm)
    db.commit()

    plots = []
    zones = [("Zone A", "Hydroponic"), ("Zone B", "Soil"), ("Zone C", "Greenhouse"), ("Zone D", "Outdoor")]
    
    all_beds = []

    for i, (name, type_) in enumerate(zones):
        plot = FarmPlot(
            plot_id=generate_id(f"PLOT-{chr(65+i)}"),
            farm_id=farm.farm_id,
            plot_name=name,
            crop_type=type_,
            area_m2=random.choice([500.0, 1000.0, 1500.0])
        )
        db.add(plot)
        plots.append(plot)
        
        # Create 5 Beds per Plot
        for bed_num in range(1, 6):
            bed = FarmBed(
                bed_id=generate_id(f"BED-{chr(65+i)}{bed_num}"),
                plot_id=plot.plot_id,
                bed_number=bed_num,
                planting_date=datetime.date.today() - datetime.timedelta(days=random.randint(1, 60)),
                status=random.choice(["Empty", "Planted", "Growing", "Harvestable"])
            )
            db.add(bed)
            all_beds.append(bed)
            
            # --- Random Cultivation Logs for each bed ---
            if bed.status != "Empty":
                for _ in range(random.randint(1, 4)):
                    log = CultivationLog(
                        log_id=generate_id("LOG"),
                        bed_id=bed.bed_id,
                        action=random.choice(["Watering", "Fertilizing", "Pruning", "Pest Control"]),
                        performed_by=random.choice(["Farmer John", "Worker Alice", "Tech Bob"]),
                        notes="Periodic Maintenance",
                        timestamp=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
                    )
                    db.add(log)
        
        # --- IoT Sensor per Plot ---
        sensor = IotSensor(
            sensor_id=generate_id(f"SENS-{chr(65+i)}"),
            plot_id=plot.plot_id,
            sensor_type="Multi-Environment",
            manufacturer="Xiaomi",
            status="Online",
            installed_at=datetime.datetime.now() - datetime.timedelta(days=100)
        )
        db.add(sensor)
        
        # Random Sensor Data (Last 24h)
        for h in range(10):
            data = SensorData(
                data_id=generate_id("DATA"),
                sensor_id=sensor.sensor_id,
                temperature=round(random.uniform(20.0, 35.0), 1),
                humidity=round(random.uniform(50.0, 90.0), 1),
                soil_moisture=round(random.uniform(30.0, 80.0), 1),
                light_intensity=round(random.uniform(1000.0, 5000.0), 1),
                recorded_at=datetime.datetime.now() - datetime.timedelta(hours=h*2)
            )
            db.add(data)

    db.commit()

    # --- 2. CATALOG & PARTNERS & WAREHOUSE ---
    print("- Creating Catalog, Products, Suppliers, and Warehouses...")
    ingredients = [
        Ingredient(ingredient_id=generate_id("ING"), name="Romaine Lettuce Seeds"),
        Ingredient(ingredient_id=generate_id("ING"), name="Strawberry Runner"),
        Ingredient(ingredient_id=generate_id("ING"), name="Organic Fertilizer NPK"),
        Ingredient(ingredient_id=generate_id("ING"), name="Pest Control Bio-Mix"),
        Ingredient(ingredient_id=generate_id("ING"), name="Tomato Seeds"),
        Ingredient(ingredient_id=generate_id("ING"), name="Coco Peat Substrate"),
    ]
    db.add_all(ingredients)
    
    products = [
        Product(product_id=generate_id("PROD"), product_name="Premium Romaine Lettuce", ingredient_id=ingredients[0].ingredient_id),
        Product(product_id=generate_id("PROD"), product_name="Sweet Dalat Strawberry", ingredient_id=ingredients[1].ingredient_id),
        Product(product_id=generate_id("PROD"), product_name="Organic Tomato Pack", ingredient_id=ingredients[4].ingredient_id),
    ]
    db.add_all(products)

    warehouses = [
        Warehouse(warehouse_id=generate_id("WH"), warehouse_name="Central Cold Storage", location="Zone A Entrance", capacity_ton=50.0),
        Warehouse(warehouse_id=generate_id("WH"), warehouse_name="Dry Materials Depot", location="Zone B Rear", capacity_ton=100.0),
    ]
    db.add_all(warehouses)
    
    suppliers = [
        Supplier(supplier_id=generate_id("SUP"), supplier_name="AgriTech Inputs Co.", supplier_type="Materials", phone="0909000111", address="Hanoi"),
        Supplier(supplier_id=generate_id("SUP"), supplier_name="Green Seeds Ltd.", supplier_type="Seeds", phone="0909000222", address="Dalat"),
        Supplier(supplier_id=generate_id("SUP"), supplier_name="BioChem Solutions", supplier_type="Chemicals", phone="0909000333", address="HCM City"),
        Supplier(supplier_id=generate_id("SUP"), supplier_name="FarmTools Global", supplier_type="Equipment", phone="0909000444", address="Da Nang"),
    ]
    db.add_all(suppliers)
    db.commit()

    # --- 3. PROCUREMENT (10 Contracts, Multiple Batches) ---
    print("- Creating 10 Purchase Contracts with random Batches (1-4)...")
    
    for i in range(10):
        supplier = random.choice(suppliers)
        ingredient = random.choice(ingredients)
        start_date = datetime.date.today() - datetime.timedelta(days=random.randint(10, 200))
        
        contract = PurchaseContract(
            contract_id=generate_id(f"CTR-{i+1}"),
            supplier_id=supplier.supplier_id,
            ingredient_id=ingredient.ingredient_id,
            committed_quantity=random.choice([500.0, 1000.0, 2000.0, 5000.0]),
            contract_price=random.randint(10, 100) * 1000000.0,
            quality_commitment="Grade A Standard",
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=365),
            status="Active"
        )
        db.add(contract)
        db.commit() # Commit to get ID for relationship

        # ** Generate 1 to 4 Batches per Contract **
        num_batches = random.randint(1, 4)
        print(f"  > Contract {contract.contract_id}: Creating {num_batches} batches.")

        for b in range(num_batches):
            # Batches arrive at different times
            batch_date = contract.start_date + datetime.timedelta(days=random.randint(5, 100))
            expected_qty = contract.committed_quantity / num_batches
            
            batch = PurchaseBatch(
                batch_id=generate_id(f"BATCH-{i+1}-{b+1}"),
                contract_id=contract.contract_id,
                purchase_date=batch_date,
                expected_quantity=expected_qty,
                unit_price=contract.contract_price / contract.committed_quantity,
                status=random.choice(["Received", "Pending", "Inspecting"])
            )
            db.add(batch)
            db.commit()

            # Purchase Ticket (Only if Received or Inspecting)
            if batch.status in ["Received", "Inspecting"]:
                ticket = PurchaseTicket(
                    ticket_id=generate_id(f"PTICK-{i+1}-{b+1}"),
                    batch_id=batch.batch_id,
                    supplier_id=supplier.supplier_id,
                    ingredient_id=ingredient.ingredient_id,
                    raw_weight=expected_qty * random.uniform(0.98, 1.02), # Slight variance
                    received_at=datetime.datetime.combine(batch_date, datetime.datetime.min.time())
                )
                db.add(ticket)
                db.commit()

                # QC for Purchase Ticket
                qc_id = generate_id("QC")
                qc = QcRecord(
                    qc_id=qc_id,
                    ticket_id=ticket.ticket_id,
                    ticket_source="PURCHASE",
                    weighing_ticket_id=None,
                    purchase_ticket_id=ticket.ticket_id, # Strict FK
                    production_lot_id=None,
                    length_cm=None,
                    weight_g=None,
                    freshness="N/A",
                    status=random.choice(["Passed", "Passed", "Warning", "Rejected"]),
                    qc_date=ticket.received_at + datetime.timedelta(hours=2)
                )
                db.add(qc)
                
                # --- LOGISTICS: Transport to Warehouse (If QC Passed/Warning) ---
                if qc.status in ["Passed", "Warning"]:
                    transport = TransportTicket(
                        transport_id=generate_id("TRANS"),
                        source_type="PURCHASE",
                        source_ticket_id=ticket.ticket_id,
                        destination_warehouse_id=warehouses[1].warehouse_id, # Dry Depot for inputs
                        driver="Driver Mike",
                        vehicle=f"Truck-{random.randint(10, 99)}",
                        depart_time=qc.qc_date + datetime.timedelta(hours=1),
                        arrive_time=qc.qc_date + datetime.timedelta(hours=2),
                        status="Delivered"
                    )
                    db.add(transport)
                    
                    # Add to Inventory
                    inv = Inventory(
                        inventory_id=generate_id("INV"),
                        warehouse_id=warehouses[1].warehouse_id,
                        ingredient_id=ingredient.ingredient_id,
                        quantity_kg=ticket.raw_weight,
                        last_updated=transport.arrive_time
                    )
                    db.add(inv)

    # --- 4. HARVEST ---
    print("- Creating Harvest Weighing Tickets...")
    
    # Filter only Harvestable or Growing beds simulating partial harvest
    harvest_beds = [b for b in all_beds if b.status in ["Harvestable", "Growing"]]
    
    for bed in harvest_beds:
        # Determine crop based on Plot ID prefix (Zone A = Lettuce, Zone B = Strawberry)
        # Using startswith is safer than 'in' to avoid partial matches with UUIDs
        if bed.plot_id.startswith("PLOT-A"):
            crop = ingredients[0] # Lettuce
        else:
            crop = ingredients[1] # Strawberry keys
        
        ticket = WeighingTicket(
            ticket_id=generate_id("WTICK"),
            bed_id=bed.bed_id,
            ingredient_id=crop.ingredient_id,
            raw_weight=random.uniform(5.0, 50.0), # kg
            harvested_by=random.choice(["Team 1", "Team 2"]),
            timestamp=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 5))
        )
        db.add(ticket)
        db.commit()
        
        # QC for Harvest
        qc = QcRecord(
            qc_id=generate_id("QC"),
            ticket_id=ticket.ticket_id,
            ticket_source="HARVEST",
            weighing_ticket_id=ticket.ticket_id, # Strict FK
            purchase_ticket_id=None,
            production_lot_id=None,
            length_cm=random.uniform(10.0, 30.0),
            weight_g=random.uniform(100.0, 500.0),
            freshness=random.choice(["Excellent", "Good", "Fair"]),
            status="Passed",
            qc_date=ticket.timestamp + datetime.timedelta(minutes=30)
        )
        db.add(qc)
        
        # --- LOGISTICS: Transport to Warehouse (Cold Storage) ---
        transport = TransportTicket(
            transport_id=generate_id("TRANS"),
            source_type="HARVEST",
            source_ticket_id=ticket.ticket_id,
            destination_warehouse_id=warehouses[0].warehouse_id, # Cold Storage for Harvest
            driver="Driver John",
            vehicle=f"Van-{random.randint(10, 99)}",
            depart_time=qc.qc_date + datetime.timedelta(minutes=30),
            arrive_time=qc.qc_date + datetime.timedelta(minutes=60),
            status="Delivered"
        )
        db.add(transport)

    db.commit()

    # --- 5. HQ PRODUCTION ---
    print("- Creating Production Lots from Passed QC...")
    
    # Fetch passed QC records to generate Production Lots (Focusing on Harvest Source for Products)
    passed_qcs = db.query(QcRecord).filter(
        QcRecord.status == "Passed", 
        QcRecord.ticket_source == "HARVEST"
    ).all()
    
    if passed_qcs:
        chunk_size = 3
        current_chunk = []
        lot_counter = 1
        
        for qc in passed_qcs:
            current_chunk.append(qc)
            
            if len(current_chunk) >= chunk_size:
                # Determine Product based on ingredient in ticket (via relationship if available, or heuristic)
                # For simplicity here, we map randomly to one of our products or based on a simple rule
                # In a real app, we'd look up QcRecord -> WeighingTicket -> Ingredient -> Product
                
                # Check crop type indirectly or simplify. 
                # Let's just pick a product based on the list we created
                product_to_make = products[0] # Default Lettuce
                # If we could access qc.weighing_ticket.ingredient... but let's assume simple logic
                
                lot = ProductionLot(
                    lot_id=generate_id(f"LOT-{lot_counter}"),
                    product_id=product_to_make.product_id,
                    mfg_date=datetime.datetime.now(),
                    exp_date=datetime.datetime.now() + datetime.timedelta(days=14)
                )
                db.add(lot)
                
                # Link QCs to this Lot
                for q in current_chunk:
                    q.production_lot = lot
                
                current_chunk = []
                lot_counter += 1
        
        # Handle remaining QCs
        if current_chunk:
            lot = ProductionLot(
                lot_id=generate_id(f"LOT-{lot_counter}"),
                product_id=products[0].product_id,
                mfg_date=datetime.datetime.now(),
                exp_date=datetime.datetime.now() + datetime.timedelta(days=14)
            )
            db.add(lot)
            for q in current_chunk:
                q.production_lot = lot

    db.commit()

    print("Seeding complete! Data Generated.")
    db.close()

if __name__ == "__main__":
    seed_data()
