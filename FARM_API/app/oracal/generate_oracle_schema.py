import os

def main():
    ddl_statements = []

    # Helper to add drop and create
    def add_table(name, columns, constraints=[]):
        cols_str = ",\n    ".join(columns)
        if constraints:
            cols_str += ",\n    " + ",\n    ".join(constraints)
            
        ddl = f"CREATE TABLE {name} (\n    {cols_str}\n);"
        ddl_statements.append((name, ddl))

    # --- TABLES (Order matters for Foreign Keys!) ---
    
    # 1. INDEPENDENT TABLES
    add_table("farm", [
        "farm_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "farm_name VARCHAR2(255)",
        "location VARCHAR2(255)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ])

    add_table("warehouse", [
        "warehouse_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "warehouse_name VARCHAR2(255)",
        "location VARCHAR2(255)",
        "capacity_ton NUMBER",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ])

    add_table("supplier", [
        "supplier_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "supplier_name VARCHAR2(255)",
        "supplier_type VARCHAR2(100)",
        "phone VARCHAR2(50)",
        "address VARCHAR2(255)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ])

    add_table("ingredient", [
        "ingredient_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "name VARCHAR2(255)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ])

    # 2. DEPENDENT LEVEL 1
    add_table("product", [
        "product_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "product_name VARCHAR2(255)",
        "ingredient_id VARCHAR2(50)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)",
    ], constraints=[
        "CONSTRAINT fk_prod_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)"
    ])

    add_table("farm_plot", [
        "plot_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "farm_id VARCHAR2(50)",
        "plot_name VARCHAR2(255)",
        "crop_type VARCHAR2(100)",
        "area_m2 NUMBER",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_plot_farm FOREIGN KEY (farm_id) REFERENCES farm(farm_id)"
    ])

    add_table("purchase_contract", [
        "contract_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "supplier_id VARCHAR2(50)",
        "ingredient_id VARCHAR2(50)",
        "committed_quantity NUMBER",
        "contract_price NUMBER",
        "quality_commitment VARCHAR2(255)",
        "start_date DATE",
        "end_date DATE",
        "status VARCHAR2(50)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_cont_sup FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)",
        "CONSTRAINT fk_cont_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)"
    ])

    # 3. DEPENDENT LEVEL 2
    add_table("farm_bed", [
        "bed_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "plot_id VARCHAR2(50)",
        "bed_number NUMBER",
        "planting_date DATE",
        "status VARCHAR2(50)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_bed_plot FOREIGN KEY (plot_id) REFERENCES farm_plot(plot_id)"
    ])

    add_table("iot_sensor", [
        "sensor_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "plot_id VARCHAR2(50)",
        "sensor_type VARCHAR2(100)",
        "manufacturer VARCHAR2(100)",
        "status VARCHAR2(50)",
        "installed_at TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_sens_plot FOREIGN KEY (plot_id) REFERENCES farm_plot(plot_id)"
    ])

    add_table("purchase_batch", [
        "batch_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "contract_id VARCHAR2(50)",
        "purchase_date DATE",
        "expected_quantity NUMBER",
        "unit_price NUMBER",
        "status VARCHAR2(50)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_batch_cont FOREIGN KEY (contract_id) REFERENCES purchase_contract(contract_id)"
    ])

    add_table("production_lot", [
        "lot_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "product_id VARCHAR2(50)",
        "mfg_date TIMESTAMP",
        "exp_date TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_lot_prod FOREIGN KEY (product_id) REFERENCES product(product_id)"
    ])

    # Inventory with Batch Source Tracking
    add_table("inventory", [
        "inventory_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "warehouse_id VARCHAR2(50)",
        "inventory_type VARCHAR2(20)",   # 'INGREDIENT' or 'PRODUCT'
        "item_id VARCHAR2(50)",          # Generic ID, can be ingredient_id or product_id
        "lot_number VARCHAR2(50)",       # Traceability Key
        "origin_source VARCHAR2(50)",    # 'PURCHASE' or 'PRODUCTION'
        "origin_ref_id VARCHAR2(50)",    # purchase_batch_id or production_lot_id
        "quantity_kg NUMBER",
        "updated_at TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_inv_wh FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id)"
    ])

    # 4. DEPENDENT LEVEL 3
    add_table("cultivation_log", [
        "log_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "bed_id VARCHAR2(50)",
        "action VARCHAR2(100)",
        "performed_by VARCHAR2(100)",
        "notes VARCHAR2(4000)",
        "timestamp TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_log_bed FOREIGN KEY (bed_id) REFERENCES farm_bed(bed_id)"
    ])

    add_table("sensor_data", [
        "data_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "sensor_id VARCHAR2(50)",
        "temperature NUMBER",
        "humidity NUMBER",
        "soil_moisture NUMBER",
        "light_intensity NUMBER",
        "recorded_at TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_data_sens FOREIGN KEY (sensor_id) REFERENCES iot_sensor(sensor_id)"
    ])

    add_table("purchase_ticket", [
        "ticket_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "batch_id VARCHAR2(50)",
        "supplier_id VARCHAR2(50)",
        "ingredient_id VARCHAR2(50)",
        "raw_weight NUMBER",
        "received_at TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_ptick_batch FOREIGN KEY (batch_id) REFERENCES purchase_batch(batch_id)",
        "CONSTRAINT fk_ptick_sup FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)",
        "CONSTRAINT fk_ptick_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)"
    ])

    add_table("weighing_ticket", [
        "ticket_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "bed_id VARCHAR2(50)",
        "ingredient_id VARCHAR2(50)",
        "raw_weight NUMBER",
        "harvested_by VARCHAR2(100)",
        "timestamp TIMESTAMP",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_wtick_bed FOREIGN KEY (bed_id) REFERENCES farm_bed(bed_id)",
        "CONSTRAINT fk_wtick_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)"
    ])

    # 5. DEPENDENT LEVEL 4 & COMPLEX

    # Combined QC System
    add_table("qc_record", [
        "qc_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "source_type VARCHAR2(50)",     # 'RECEIVING', 'HARVEST', 'PRODUCT'
        "reference_id VARCHAR2(50)",    # ID of the source ticket/lot
        "inspector_name VARCHAR2(100)",
        "pass_status VARCHAR2(20)",     # 'PASS', 'FAIL', 'CONDITIONAL'
        "checked_at TIMESTAMP",
        "notes VARCHAR2(4000)",         # Unified notes
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)",
        
        # Type specific columns
        "sample_size NUMBER",           # Receiving
        "defects_found NUMBER",         # Receiving
        "quality_score NUMBER",         # Receiving
        "appearance_grade VARCHAR2(50)",# Harvest
        "brix_level NUMBER",            # Product
        "ph_level NUMBER",              # Product
        "pesticide_residue_check VARCHAR2(20)", # Product
        "final_grade VARCHAR2(20)"      # Product
    ])

    add_table("transport_ticket", [
        "transport_id VARCHAR2(50) NOT NULL PRIMARY KEY",
        "source_type VARCHAR2(50)",
        "source_ticket_id VARCHAR2(50)",
        "destination_warehouse_id VARCHAR2(50)",
        "driver VARCHAR2(100)",
        "vehicle VARCHAR2(100)",
        "depart_time TIMESTAMP",
        "arrive_time TIMESTAMP",
        "status VARCHAR2(50)",
        "region VARCHAR2(50)",
        "site_id VARCHAR2(50)"
    ], constraints=[
        "CONSTRAINT fk_trans_wh FOREIGN KEY (destination_warehouse_id) REFERENCES warehouse(warehouse_id)"
    ])

    # --- Write to file ---
    output_file = "oracle_create_schema.sql"
    print(f"Writing DDL to {os.path.abspath(output_file)}...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("-- Oracle Schema Generation\n")
        f.write("-- Auto-generated matches FastAPI SQLAlchemy Models\n\n")
        
        # Drop block
        f.write("-- DROP TABLES (Safely)\n")
        for name, _ in reversed(ddl_statements):
            f.write("BEGIN\n")
            f.write(f"    EXECUTE IMMEDIATE 'DROP TABLE {name} CASCADE CONSTRAINTS';\n")
            f.write("EXCEPTION\n")
            f.write("    WHEN OTHERS THEN NULL;\n")
            f.write("END;\n/\n")

        # Create
        f.write("\n-- CREATE TABLES\n")
        for name, ddl in ddl_statements:
            f.write(f"-- Table: {name}\n")
            f.write(ddl + "\n\n")

    print("Schema Generation Complete.")

if __name__ == "__main__":
    main()
