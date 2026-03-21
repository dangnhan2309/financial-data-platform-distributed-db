import random
import uuid
import datetime
import os

# Partition metadata
REGION = "north"
SITE_ID = "farm-1"

# Multi-site configuration (horizontal fragments by region)
SITES = [
    {
        "region": "BAC",
        "site_id": "farm-bac",
        "farm_name": "FARM_SITE_BAC",
        "location": "Mien Bac",
    },
    {
        "region": "TRUNG",
        "site_id": "farm-trung",
        "farm_name": "FARM_SITE_TRUNG",
        "location": "Mien Trung",
    },
    {
        "region": "NAM",
        "site_id": "farm-nam",
        "farm_name": "FARM_SITE_NAM",
        "location": "Mien Nam",
    },
]

# Region-specific catalogs to make each shard distinct
SITE_CONFIG = {
    "BAC": {
        "ingredients": [
            "Aloe Vera Seedlings", "Organic NPK Fertilizer",
            "Biological Pesticide", "Coco Peat Substrate",
            "Trace Mineral Mix"
        ],
        "products": [
            ("Fresh Aloe Vera - Bac", 0),
            ("Aloe Vera Gel - Bac", 0),
        ],
        "warehouses": [
            ("Cold Hub Bac", "Noi Bai Logistics", 60.0),
            ("Dry Hub Bac", "Gia Lam ICD", 120.0),
        ],
        "suppliers": [
            ("AgriTech Bac", "Materials", "0909111001", "Ha Noi"),
            ("Green Seeds Bac", "Seeds", "0909111002", "Bac Ninh"),
            ("BioChem Bac", "Chemicals", "0909111003", "Hai Phong"),
        ],
    },
    "TRUNG": {
        "ingredients": [
            "Dragon Fruit Seedlings", "Organic Compost",
            "Bio Pesticide Central", "Drip Irrigation Kit"
        ],
        "products": [
            ("Fresh Dragon Fruit - Trung", 0),
            ("Dried Dragon Fruit - Trung", 0),
        ],
        "warehouses": [
            ("Cold Hub Trung", "Da Nang Port", 55.0),
            ("Dry Hub Trung", "Lien Chieu ICD", 110.0),
        ],
        "suppliers": [
            ("AgriTech Trung", "Materials", "0909222001", "Da Nang"),
            ("Green Seeds Trung", "Seeds", "0909222002", "Quang Nam"),
            ("BioChem Trung", "Chemicals", "0909222003", "Hue"),
        ],
    },
    "NAM": {
        "ingredients": [
            "Coconut Husk Substrate", "Organic PK Booster",
            "Biological Fungicide", "Micro Sprinkler Set"
        ],
        "products": [
            ("Fresh Aloe Vera - Nam", 0),
            ("Aloe Vera Juice - Nam", 0),
        ],
        "warehouses": [
            ("Cold Hub Nam", "Cat Lai", 65.0),
            ("Dry Hub Nam", "Long Hau", 130.0),
        ],
        "suppliers": [
            ("AgriTech Nam", "Materials", "0909333001", "HCM"),
            ("Green Seeds Nam", "Seeds", "0909333002", "Dong Nai"),
            ("BioChem Nam", "Chemicals", "0909333003", "Can Tho"),
        ],
    },
}

# Helper to generate ID
def generate_id(prefix):
    return f"{prefix}-{str(uuid.uuid4())[:8]}"

# Helper to format value for Oracle SQL
def format_val(v):
    if v is None:
        return "NULL"
    if isinstance(v, str):
        # Escape single quotes
        return f"'{v.replace('\'', '\'\'')}'"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        # Oracle timestamps
        try:
            # Try full datetime format
            return f"TO_DATE('{v.strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS')"
        except:
             # Fallback if it's just a date object but treated as datetime
             return f"TO_DATE('{v.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')" 
    return f"'{str(v)}'"

def insert_sql(table_name, data):
    cols = ", ".join(data.keys())
    vals = ", ".join([format_val(v) for v in data.values()])
    return f"INSERT INTO {table_name} ({cols}) VALUES ({vals});\n"

# Defaults for qc_record to avoid NULLs in seed data
QC_DEFAULTS = {
    "appearance_grade": "UNKNOWN",
    "brix_level": 0,
    "ph_level": 0,
    "pesticide_residue_check": "UNKNOWN",
    "final_grade": "PENDING",
    "sample_size": 0,
    "defects_found": 0,
    "quality_score": 0,
}

def apply_qc_defaults(qc_record):
    """Fill None fields in qc_record with consistent defaults."""
    for key, default_val in QC_DEFAULTS.items():
        if qc_record.get(key) is None:
            qc_record[key] = default_val
    return qc_record

def main():
    global REGION, SITE_ID
    # Per-site data containers (collect all, then split per site when writing)
    farms = []
    plots = []
    beds = []
    logs = []
    sensors = []
    sensor_datas = []
    ingredients = []
    products = []
    warehouses = []
    suppliers = []
    contracts = []
    batches = []
    ptickets = [] # Purchase Tickets
    qc_records = []
    transports = []
    inventories = []
    wtickets = []
    lots = []
    
    print("Generating Data in Memory...")

    for site in SITES:
        REGION = site["region"]
        SITE_ID = site["site_id"]
        farm_name = site["farm_name"]
        location = site["location"]

        # --- 1. FARM STRUCTURE ---
        farm_id = generate_id("FARM")
        farm = {
            "farm_id": farm_id,
            "farm_name": farm_name,
            "location": location,
            "region": REGION,
            "site_id": SITE_ID
        }
        farms.append(farm)

        zones = [("Zone A", "Hydroponic"), ("Zone B", "Soil"), ("Zone C", "Greenhouse"), ("Zone D", "Outdoor")]
        
        for i, (name, type_) in enumerate(zones):
            plot_id = generate_id(f"PLOT-{chr(65+i)}")
            plot = {
                "plot_id": plot_id,
                "farm_id": farm_id,
                "plot_name": name,
                "crop_type": type_,
                "area_m2": random.choice([500.0, 1000.0, 1500.0]),
                "region": REGION,
                "site_id": SITE_ID
            }
            plots.append(plot)
            
            # Create 5 Beds per Plot
            for bed_num in range(1, 6):
                bed_id = generate_id(f"BED-{chr(65+i)}{bed_num}")
                status = random.choice(["Empty", "Planted", "Growing", "Harvestable"])
                bed = {
                    "bed_id": bed_id,
                    "plot_id": plot_id,
                    "bed_number": bed_num,
                    "planting_date": datetime.date.today() - datetime.timedelta(days=random.randint(1, 60)),
                    "status": status,
                    "region": REGION,
                    "site_id": SITE_ID
                }
                beds.append(bed)
                
                # --- Random Cultivation Logs ---
                if status != "Empty":
                    for _ in range(random.randint(1, 4)):
                        log = {
                            "log_id": generate_id("LOG"),
                            "bed_id": bed_id,
                            "action": random.choice(["Watering", "Fertilizing", "Pruning", "Pest Control"]),
                            "performed_by": random.choice(["Nguyen Van A", "Le Thi B", "Tran Van C", "Pham Thi D", "Hoang Van E"]),
                            "notes": "Periodic Maintenance",
                            "timestamp": datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30)),
                            "region": REGION,
                            "site_id": SITE_ID
                        }
                        logs.append(log)
            
            # --- IoT Sensor per Plot ---
            sensor_id = generate_id(f"SENS-{chr(65+i)}")
            sensor = {
                "sensor_id": sensor_id,
                "plot_id": plot_id,
                "sensor_type": "Multi-Environment",
                "manufacturer": "Xiaomi",
                "status": "Online",
                "installed_at": datetime.datetime.now() - datetime.timedelta(days=100),
                "region": REGION,
                "site_id": SITE_ID
            }
            sensors.append(sensor)
            
            # Random Sensor Data
            for h in range(10):
                data = {
                    "data_id": generate_id("DATA"),
                    "sensor_id": sensor_id,
                    "temperature": round(random.uniform(20.0, 35.0), 1),
                    "humidity": round(random.uniform(50.0, 90.0), 1),
                    "soil_moisture": round(random.uniform(30.0, 80.0), 1),
                    "light_intensity": round(random.uniform(1000.0, 5000.0), 1),
                    "recorded_at": datetime.datetime.now() - datetime.timedelta(hours=h*2),
                    "region": REGION,
                    "site_id": SITE_ID
                }
                sensor_datas.append(data)

        # --- 2. CATALOG & PARTNERS & WAREHOUSE (region-specific) ---
        cfg = SITE_CONFIG.get(REGION, {})

        ing_names = cfg.get("ingredients", []) or [
            "Generic Seed", "Generic Fertilizer"
        ]
        ing_objs = []
        for name in ing_names:
            ing_id = generate_id("ING")
            ing = {"ingredient_id": ing_id, "name": name}
            ing["region"] = REGION
            ing["site_id"] = SITE_ID
            ingredients.append(ing)
            ing_objs.append(ing)

        prod_defs = cfg.get("products", []) or [("Generic Product", 0)]

        prod_objs = []
        for pname, ing_idx in prod_defs:
            src_ing = ing_objs[min(ing_idx, len(ing_objs)-1)]
            pid = generate_id("PROD")
            prod = {
                "product_id": pid,
                "product_name": pname,
                "ingredient_id": src_ing["ingredient_id"],
                "region": REGION,
                "site_id": SITE_ID
            }
            products.append(prod)
            prod_objs.append(prod)

        wh_defs = cfg.get("warehouses", []) or [
            ("Generic Cold Storage", "Gate A", 40.0),
            ("Generic Dry Depot", "Gate B", 80.0)
        ]
        wh_objs = []
        for i, (wname, loc, cap) in enumerate(wh_defs):
            wid = generate_id("WH")
            wh = {
                "warehouse_id": wid,
                "warehouse_name": wname,
                "location": loc,
                "capacity_ton": cap,
                "region": REGION,
                "site_id": SITE_ID
            }
            warehouses.append(wh)
            wh_objs.append(wh) # 0: Cold, 1: Dry

        sup_defs = cfg.get("suppliers", []) or [
            ("Generic Supplier A", "Materials", "0909000001", "City A"),
            ("Generic Supplier B", "Seeds", "0909000002", "City B"),
        ]
        sup_objs = []
        for sname, stype, sms, saddr in sup_defs:
            sid = generate_id("SUP")
            sup = {
                "supplier_id": sid,
                "supplier_name": sname,
                "supplier_type": stype,
                "phone": sms,
                "address": saddr,
                "region": REGION,
                "site_id": SITE_ID
            }
            suppliers.append(sup)
            sup_objs.append(sup)

        # --- 3. PROCUREMENT & INBOUND ---
        # (Ingredients coming in)
        for i in range(10):
            supplier = random.choice(sup_objs)
            ingredient = random.choice(ing_objs)
            start_date = datetime.date.today() - datetime.timedelta(days=random.randint(10, 200))
            
            contract_id = generate_id(f"CTR-{i+1}")
            committed_qty = random.choice([500.0, 1000.0, 2000.0, 5000.0])
            price = random.randint(10, 100) * 1000000.0
            
            contract = {
                "contract_id": contract_id,
                "supplier_id": supplier["supplier_id"],
                "ingredient_id": ingredient["ingredient_id"],
                "committed_quantity": committed_qty,
                "contract_price": price,
                "quality_commitment": "Grade A Standard",
                "start_date": start_date,
                "end_date": start_date + datetime.timedelta(days=365),
                "status": "Active",
                "region": REGION,
                "site_id": SITE_ID
            }
            contracts.append(contract)

            # Batches
            num_batches = random.randint(1, 4)
            for b in range(num_batches):
                batch_date = start_date + datetime.timedelta(days=random.randint(5, 100))
                expected_qty = committed_qty / num_batches
                bid = generate_id(f"BATCH-{i+1}-{b+1}")
                status = random.choice(["Received", "Pending", "Inspecting"])
                
                batch = {
                    "batch_id": bid,
                    "contract_id": contract_id,
                    "purchase_date": batch_date,
                    "expected_quantity": expected_qty,
                    "unit_price": price / committed_qty,
                    "status": status,
                    "region": REGION,
                    "site_id": SITE_ID
                }
                batches.append(batch)

                if status in ["Received", "Inspecting"]:
                    # Prefix P_ to clearly mark purchase ticket IDs
                    tid = generate_id("P_TICKET")
                    raw_w = expected_qty * random.uniform(0.98, 1.02)
                    received_at = datetime.datetime.combine(batch_date, datetime.datetime.min.time())
                    
                    ticket = {
                        "ticket_id": tid,
                        "batch_id": bid,
                        "supplier_id": supplier["supplier_id"],
                        "ingredient_id": ingredient["ingredient_id"],
                        "raw_weight": raw_w,
                        "received_at": received_at,
                        "region": REGION,
                        "site_id": SITE_ID
                    }
                    ptickets.append(ticket)

                    # QC Receiving
                    qc_id = generate_id("QCRCV")
                    qc_outcome = random.choice(["PASS", "PASS", "CONDITIONAL", "FAIL"])
                    qc_date = received_at + datetime.timedelta(hours=2)
                    
                    qc = {
                        "qc_id": qc_id,
                        "source_type": "RECEIVING",
                        "reference_id": tid, # purchase_ticket_id
                        "inspector_name": "QC Staff A",
                        "sample_size": 10,
                        "defects_found": random.randint(0, 3) if qc_outcome == "PASS" else random.randint(5, 10),
                        "quality_score": random.randint(80, 100) if qc_outcome == "PASS" else random.randint(50, 70), 
                        "pass_status": qc_outcome,
                        "notes": "Standard Check",
                        "checked_at": qc_date,
                        "appearance_grade": None,
                        "brix_level": None,
                        "ph_level": None,
                        "pesticide_residue_check": None,
                        "final_grade": None,
                        "region": REGION,
                        "site_id": SITE_ID
                    }
                    qc_records.append(apply_qc_defaults(qc))
                    
                    # Transport & Inventory if Passed
                    if qc_outcome in ["PASS", "CONDITIONAL"]:
                        arrive_time = qc_date + datetime.timedelta(hours=2)
                        tr = {
                            "transport_id": generate_id("TRANS"),
                            "source_type": "PURCHASE",
                            "source_ticket_id": tid,
                            "destination_warehouse_id": wh_objs[1]["warehouse_id"], # Dry Depot
                            "driver": random.choice(["Ngo Gia T", "Le Hong P"]),
                            "vehicle": f"Truck-{random.randint(10, 99)}",
                            "depart_time": qc_date + datetime.timedelta(hours=1),
                            "arrive_time": arrive_time,
                            "status": "Delivered",
                            "region": REGION,
                            "site_id": SITE_ID
                        }
                        transports.append(tr)
                        
                        # INVENTORY WITH LOT TRACING
                        inv = {
                            "inventory_id": generate_id("INV"),
                            "warehouse_id": wh_objs[1]["warehouse_id"],
                            "inventory_type": "INGREDIENT",
                            "item_id": ingredient["ingredient_id"],
                            "lot_number": bid, # Using Purchase Batch ID as Lot Number
                            "origin_source": "PURCHASE",
                            "origin_ref_id": bid,
                            "quantity_kg": raw_w,
                            "updated_at": arrive_time,
                            "region": REGION,
                            "site_id": SITE_ID
                        }
                        inventories.append(inv)

        # --- 4. HARVEST & PRODUCTION ---
        harvest_beds = [b for b in beds if b["status"] in ["Harvestable", "Growing"] and b["site_id"] == SITE_ID]
        
        for bed in harvest_beds:
            # 1. Harvest Ticket (prefix W_ to distinguish from purchase tickets)
            wid = generate_id("W_TICKET")
            harvest_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 5))
            product = random.choice(prod_objs) # Assuming bed grows one of these
            
            wticket = {
                "ticket_id": wid,
                "bed_id": bed["bed_id"],
                "ingredient_id": product["ingredient_id"], # Link to seed used (simplified)
                "raw_weight": random.uniform(50.0, 200.0),
                "harvested_by": "Worker Alice",
                "timestamp": harvest_date,
                "region": REGION,
                "site_id": SITE_ID
            }
            wtickets.append(wticket)

            # 2. QC Harvest
            qc_har_id = generate_id("QCHAR")
            qc_har = {
                "qc_id": qc_har_id,
                "source_type": "HARVEST",
                "reference_id": wid, # weighing_ticket_id
                "inspector_name": "Field Supervisor",
                "appearance_grade": random.choice(["A", "A", "B", "C"]),
                "notes": "None",
                "pass_status": "PASS",
                "checked_at": harvest_date + datetime.timedelta(minutes=30),
                "sample_size": None,
                "defects_found": None,
                "quality_score": None,
                "brix_level": None,
                "ph_level": None,
                "pesticide_residue_check": None,
                "final_grade": None,
                "region": REGION,
                "site_id": SITE_ID
            }
            qc_records.append(apply_qc_defaults(qc_har))

            # 3. Production / Processing -> Finished Product Lot
            lot_id = generate_id("LOT")
            mfg_date = harvest_date + datetime.timedelta(hours=4)
            
            lot = {
                "lot_id": lot_id,
                "product_id": product["product_id"],
                "mfg_date": mfg_date,
                "exp_date": mfg_date + datetime.timedelta(days=14), # Fresh produce expiration
                "region": REGION,
                "site_id": SITE_ID
            }
            lots.append(lot)
            
            # 4. QC Product Lot
            qc_prod_id = generate_id("QCPROD") 
            grade = random.choice(["PREMIUM", "STANDARD"])
            qc_prod = {
                "qc_id": qc_prod_id,
                "source_type": "PRODUCT",
                "reference_id": lot_id, # production_lot_id
                "inspector_name": "QC Lab",
                "brix_level": round(random.uniform(5.0, 15.0), 1),
                "ph_level": round(random.uniform(3.5, 7.0), 1),
                "pesticide_residue_check": "PASS",
                "final_grade": grade,
                "checked_at": mfg_date + datetime.timedelta(minutes=30),
                "pass_status": "PASS",
                "notes": "None",
                "sample_size": None,
                "defects_found": None,
                "quality_score": None,
                "appearance_grade": None,
                "region": REGION,
                "site_id": SITE_ID
            }
            qc_records.append(apply_qc_defaults(qc_prod))

            # 5. Inventory (Finished Goods)
            final_weight = wticket["raw_weight"] * 0.9 # Weight loss in processing
            
            inv = {
                "inventory_id": generate_id("INV-FG"),
                "warehouse_id": wh_objs[0]["warehouse_id"], # Cold Storage
                "inventory_type": "PRODUCT",
                "item_id": product["product_id"],
                "lot_number": lot_id, # Using Production Lot ID
                "origin_source": "PRODUCTION",
                "origin_ref_id": lot_id,
                "quantity_kg": final_weight,
                "updated_at": mfg_date + datetime.timedelta(hours=1),
                "region": REGION,
                "site_id": SITE_ID
            }
            inventories.append(inv)

    # --- WRITE TO FILES PER SITE ---
    def write_seed_for_site(site):
        site_id = site["site_id"]
        region = site["region"]
        suffix = region.lower()
        output_file = os.path.join(os.path.dirname(__file__), f"oracle_seed_data_{suffix}.sql")
        print(f"Writing SQL for {region} to {os.path.abspath(output_file)}...")

        def filter_by_site(dataset):
            return [d for d in dataset if d.get("site_id") == site_id]

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"-- Oracle Seed Data Generation for {region}\n")
            f.write("SET DEFINE OFF;\n")
            f.write("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';\n\n")

            tables = [
                "qc_record",
                "transport_ticket", "purchase_ticket", "weighing_ticket",
                "cultivation_log", "sensor_data",
                "inventory",
                "production_lot", "purchase_batch", "iot_sensor", "farm_bed",
                "purchase_contract", "farm_plot", "product", "ingredient",
                "supplier", "warehouse", "farm"
            ]
            f.write("-- CLEANUP\n")
            for t in tables:
                f.write(f"DELETE FROM {t};\n")
            f.write("\n")

            def write_group(name, dataset):
                f.write(f"-- Data for {name}\n")
                for d in filter_by_site(dataset):
                    f.write(insert_sql(name, d))
                f.write("\n")

            write_group("farm", farms)
            write_group("warehouse", warehouses)
            write_group("supplier", suppliers)
            write_group("ingredient", ingredients)
            write_group("product", products)
            write_group("farm_plot", plots)
            write_group("farm_bed", beds)
            write_group("iot_sensor", sensors)
            write_group("cultivation_log", logs)
            write_group("sensor_data", sensor_datas)
            write_group("purchase_contract", contracts)
            write_group("purchase_batch", batches)
            write_group("purchase_ticket", ptickets)
            write_group("weighing_ticket", wtickets)
            write_group("production_lot", lots)
            write_group("qc_record", qc_records)
            write_group("transport_ticket", transports)
            write_group("inventory", inventories)

            f.write("\nCOMMIT;\n")

    for site in SITES:
        write_seed_for_site(site)

    print("Seed Data Generation Complete (per-site files).")

if __name__ == "__main__":
    main()
