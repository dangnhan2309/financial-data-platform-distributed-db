

-- Xóa toàn bộ bảng trong Schema hiện tại (Bao gồm cả ràng buộc khóa ngoại)
-- 1. Xóa Materialized Views trước để tránh lỗi ORA-12083 khi loop qua user_tables
BEGIN
   FOR mv IN (SELECT mview_name FROM user_mviews) LOOP
      EXECUTE IMMEDIATE 'DROP MATERIALIZED VIEW ' || mv.mview_name;
   END LOOP;
END;
/


-- 2. Xóa dữ liệu cũ (Dùng DELETE thay vì DROP để giữ cấu trúc bảng cho lệnh INSERT bên dưới)
BEGIN
    DELETE FROM transport_ticket;
    DELETE FROM qc_record;
    DELETE FROM weighing_ticket;
    DELETE FROM purchase_ticket;
    DELETE FROM sensor_data;
    DELETE FROM cultivation_log;
    DELETE FROM inventory;
    DELETE FROM production_lot;
    DELETE FROM purchase_batch;
    DELETE FROM iot_sensor;
    DELETE FROM farm_bed;
    DELETE FROM purchase_contract;
    DELETE FROM farm_plot;
    DELETE FROM product;
    DELETE FROM ingredient;
    DELETE FROM supplier;
    DELETE FROM warehouse;
    DELETE FROM farm;
    COMMIT;
END;
/



PROMPT Inserting aggregated data from BAC, TRUNG, and NAM sites...


PROMPT Inserting into FARM...
INSERT INTO farm SELECT * FROM farm@dblink_bac UNION ALL SELECT * FROM farm@dblink_trung UNION ALL SELECT * FROM farm@dblink_nam;

PROMPT Inserting into WAREHOUSE...
INSERT INTO warehouse SELECT * FROM warehouse@dblink_bac UNION ALL SELECT * FROM warehouse@dblink_trung UNION ALL SELECT * FROM warehouse@dblink_nam;

PROMPT Inserting into SUPPLIER...
INSERT INTO supplier SELECT * FROM supplier@dblink_bac UNION ALL SELECT * FROM supplier@dblink_trung UNION ALL SELECT * FROM supplier@dblink_nam;

PROMPT Inserting into INGREDIENT...
INSERT INTO ingredient SELECT * FROM ingredient@dblink_bac UNION ALL SELECT * FROM ingredient@dblink_trung UNION ALL SELECT * FROM ingredient@dblink_nam;


PROMPT Inserting into PRODUCT...
INSERT INTO product SELECT * FROM product@dblink_bac UNION ALL SELECT * FROM product@dblink_trung UNION ALL SELECT * FROM product@dblink_nam;

PROMPT Inserting into FARM_PLOT...
INSERT INTO farm_plot SELECT * FROM farm_plot@dblink_bac UNION ALL SELECT * FROM farm_plot@dblink_trung UNION ALL SELECT * FROM farm_plot@dblink_nam;

PROMPT Inserting into PURCHASE_CONTRACT...
INSERT INTO purchase_contract SELECT * FROM purchase_contract@dblink_bac UNION ALL SELECT * FROM purchase_contract@dblink_trung UNION ALL SELECT * FROM purchase_contract@dblink_nam;


PROMPT Inserting into FARM_BED...
INSERT INTO farm_bed SELECT * FROM farm_bed@dblink_bac UNION ALL SELECT * FROM farm_bed@dblink_trung UNION ALL SELECT * FROM farm_bed@dblink_nam;

PROMPT Inserting into IOT_SENSOR...
INSERT INTO iot_sensor SELECT * FROM iot_sensor@dblink_bac UNION ALL SELECT * FROM iot_sensor@dblink_trung UNION ALL SELECT * FROM iot_sensor@dblink_nam;

PROMPT Inserting into PURCHASE_BATCH...
INSERT INTO purchase_batch SELECT * FROM purchase_batch@dblink_bac UNION ALL SELECT * FROM purchase_batch@dblink_trung UNION ALL SELECT * FROM purchase_batch@dblink_nam;

PROMPT Inserting into PRODUCTION_LOT...
INSERT INTO production_lot SELECT * FROM production_lot@dblink_bac UNION ALL SELECT * FROM production_lot@dblink_trung UNION ALL SELECT * FROM production_lot@dblink_nam;


PROMPT Inserting into INVENTORY...
INSERT INTO inventory SELECT * FROM inventory@dblink_bac UNION ALL SELECT * FROM inventory@dblink_trung UNION ALL SELECT * FROM inventory@dblink_nam;

PROMPT Inserting into CULTIVATION_LOG...
INSERT INTO cultivation_log SELECT * FROM cultivation_log@dblink_bac UNION ALL SELECT * FROM cultivation_log@dblink_trung UNION ALL SELECT * FROM cultivation_log@dblink_nam;

PROMPT Inserting into SENSOR_DATA...
INSERT INTO sensor_data SELECT * FROM sensor_data@dblink_bac UNION ALL SELECT * FROM sensor_data@dblink_trung UNION ALL SELECT * FROM sensor_data@dblink_nam;

PROMPT Inserting into PURCHASE_TICKET...
INSERT INTO purchase_ticket SELECT * FROM purchase_ticket@dblink_bac UNION ALL SELECT * FROM purchase_ticket@dblink_trung UNION ALL SELECT * FROM purchase_ticket@dblink_nam;

PROMPT Inserting into WEIGHING_TICKET...
INSERT INTO weighing_ticket SELECT * FROM weighing_ticket@dblink_bac UNION ALL SELECT * FROM weighing_ticket@dblink_trung UNION ALL SELECT * FROM weighing_ticket@dblink_nam;

PROMPT Inserting into TRANSPORT_TICKET...
INSERT INTO transport_ticket SELECT * FROM transport_ticket@dblink_bac UNION ALL SELECT * FROM transport_ticket@dblink_trung UNION ALL SELECT * FROM transport_ticket@dblink_nam;


PROMPT Inserting into QC_RECORD...
INSERT INTO qc_record SELECT * FROM qc_record@dblink_bac UNION ALL SELECT * FROM qc_record@dblink_trung UNION ALL SELECT * FROM qc_record@dblink_nam;

COMMIT;

PROMPT Data aggregation complete.
